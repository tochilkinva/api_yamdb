import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from media_content.models import Category, Genre, Title
from reviews.models import Review

from .filters import FilterTitle
from .permissions import AdminOrReadOnly, IsAuthorOrStaff, IsAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleCreateUpdateSerializer,
    TitleGetSerializer,
    TokenSerializer,
    UserSerializer,
)

User = get_user_model()


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("$author__username",)
    ordering_fields = ("score",)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.select_related("author").all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.select_related("author").all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
        .order_by("name")
    )
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    filterset_fields = ["name", "category", "genre", "year"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return TitleCreateUpdateSerializer
        return TitleGetSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            me = self.request.user
            serializer = self.get_serializer(me)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                content_type="application/json",
            )

        if request.method == "PATCH":
            me = self.request.user
            serializer = self.get_serializer(
                me, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=me.role)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        return None


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data.get("username")
        if User.objects.filter(username=username).exists():
            return Response(
                "Такой username уже зарегистрирован",
                status=status.HTTP_200_OK,
            )

        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            return Response(
                "Такой email уже зарегистрирован",
                status=status.HTTP_200_OK,
            )

        confirmation_code = uuid.uuid4()

        User.objects.create(
            email=email,
            username=str(username),
            confirmation_code=confirmation_code,
            is_active=False,
        )
        send_mail(
            "Account verification",
            "Your activation key {}".format(confirmation_code),
            DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )
        return Response(request.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if not User.objects.filter(
            username=serializer.data["username"]
        ).exists():
            return Response(
                "Такой username не существует",
                status=status.HTTP_404_NOT_FOUND,
            )

        if not len(serializer.data["confirmation_code"]) == 36:
            return Response(
                "Такой confirmation_code не существует",
                status=status.HTTP_400_BAD_REQUEST,
            )

        confirmation_code = serializer.data["confirmation_code"]
        if not User.objects.filter(
            confirmation_code=confirmation_code
        ).exists():
            return Response(
                "Такой confirmation_code не существует",
                status=status.HTTP_404_NOT_FOUND,
            )

        user = get_object_or_404(User, confirmation_code=confirmation_code)

        user.is_active = True
        user.save()
        refresh_token = RefreshToken.for_user(user)
        return Response({"token": str(refresh_token.access_token)})

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUpView,
    TitleViewSet,
    TokenView,
    UserViewSet,
)

router_v1 = DefaultRouter()

router_v1.register("categories", CategoryViewSet)
router_v1.register("genres", GenreViewSet)
router_v1.register("titles", TitleViewSet)
router_v1.register(r"users", UserViewSet)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", SignUpView.as_view()),
    path(
        "v1/auth/token/",
        TokenView.as_view(),
        name="token_obtain_pair",
    ),
]

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from media_content.models import Category, Genre, Title
from reviews.models import Comment, Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        author = self.context["request"].user
        my_view = self.context["view"]
        title = my_view.kwargs.get("title_id")
        if author.reviews.filter(title=title):
            raise serializers.ValidationError()
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(read_only=True)

    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = "__all__"


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = "__all__"
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "bio",
        )
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("username", "email"),
                message="Поля email и username должны быть уникальными",
            )
        ]

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено"
            )
        return data

import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not username:
            raise ValueError("Укажите логин")

        if not email:
            raise ValueError("Укажите email")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USER_ROLES_CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class MyUser(AbstractUser):

    username = models.CharField(max_length=255, unique=True)

    class UserRole:
        USER = "user"
        ADMIN = "admin"
        MODERATOR = "moderator"
        choices = [
            (USER, "user"),
            (ADMIN, "admin"),
            (MODERATOR, "moderator"),
        ]

    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    email = models.EmailField(
        help_text="email address",
        unique=True,
    )

    role = models.CharField(
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

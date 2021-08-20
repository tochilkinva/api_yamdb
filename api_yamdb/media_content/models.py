import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

VALIDATOR = MaxValueValidator(datetime.date.today().year)


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
        unique=True,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Адресс категории"
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="Адресс жанра",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="Жанр", blank=True
    )
    name = models.CharField(
        max_length=256, null=False, blank=False, verbose_name="Название"
    )
    year = models.IntegerField(validators=[VALIDATOR], verbose_name="Год")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )

    class Meta:
        ordering = ("-name",)
        verbose_name = "Тайтл"
        verbose_name_plural = "Тайтлы"

    def __str__(self):
        return self.name

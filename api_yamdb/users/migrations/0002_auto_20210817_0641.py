# Generated by Django 2.2.16 on 2021-08-17 06:41

import django.contrib.auth.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="myuser",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="myuser",
            name="confirmation_code",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name="myuser",
            name="bio",
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name="myuser",
            name="email",
            field=models.EmailField(
                help_text="email address", max_length=254, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="myuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("user", "user"),
                    ("admin", "admin"),
                    ("moderator", "moderator"),
                ],
                default="user",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="myuser",
            name="username",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

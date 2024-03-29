# Generated by Django 4.1.7 on 2023-03-12 17:24

import django.core.validators
from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "contestId",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("index", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=200)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (main_app.models.TypeEnum["PROGRAMMING"], "PROGRAMMING"),
                            (main_app.models.TypeEnum["PROGRAMMING"], "QUESTION"),
                        ],
                        max_length=200,
                    ),
                ),
                (
                    "points",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "tags",
                    models.ManyToManyField(related_name="tags", to="main_app.tag"),
                ),
            ],
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-13 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="problem",
            old_name="contestId",
            new_name="contest_id",
        ),
        migrations.AddField(
            model_name="problem",
            name="solved_count",
            field=models.IntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(0)]
            ),
            preserve_default=False,
        ),
    ]
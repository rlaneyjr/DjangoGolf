# Generated by Django 4.2 on 2023-05-12 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0015_teetime_holes_to_play"),
    ]

    operations = [
        migrations.AddField(
            model_name="teetime",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]

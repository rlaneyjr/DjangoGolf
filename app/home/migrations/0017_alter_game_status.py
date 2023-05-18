# Generated by Django 4.2 on 2023-05-18 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0016_teetime_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="status",
            field=models.CharField(
                choices=[
                    ("setup", "Setup"),
                    ("active", "Active"),
                    ("completed", "Completed"),
                    ("not_finished", "Not Finished"),
                ],
                default="setup",
                max_length=64,
            ),
        ),
    ]

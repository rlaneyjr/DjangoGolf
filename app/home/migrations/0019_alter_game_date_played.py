# Generated by Django 4.2 on 2023-05-30 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0018_game_league_game"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="date_played",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

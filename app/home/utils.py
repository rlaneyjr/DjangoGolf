from home import models


def get_players_for_game(user, game):
    return models.Player.objects.filter(
        added_by=user
    ).exclude(
        game__in=[game.id]
    )

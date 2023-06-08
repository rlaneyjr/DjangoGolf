import pytest
from home import utils
from home import models


@pytest.mark.django_db
def test_get_available_players_works(normal_user, golf_game_with_player, player, player_two, second_player):
    # get players that we can add to a game
    available_players = utils.get_players_for_game(normal_user, golf_game_with_player)

    # the game currently has one player added
    # so we should only have one other player that we can add
    assert len(available_players) == 1

    # the available player should be our second player
    assert available_players[0] == player_two

    # check to be sure that we are looking at all three players
    # one of these players were added by a different user
    # it should be there, but not available for us to add to a game
    all_player_count = models.Player.objects.all().count()
    assert all_player_count == 3

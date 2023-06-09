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


@pytest.mark.django_db
def test_get_all_holes_for_18_hole_course(eighteen_hole_golf_course):
    hole_list = utils.get_holes_for_game(eighteen_hole_golf_course, "18")
    assert hole_list.count() == 18


@pytest.mark.django_db
def test_get_holes_for_front_9_on_18_hole_course(eighteen_hole_golf_course):
    hole_list = utils.get_holes_for_game(eighteen_hole_golf_course, "front-9")
    assert hole_list.count() == 9
    assert hole_list[0].order == 1
    assert hole_list.last().order == 9


@pytest.mark.django_db
def test_get_holes_for_back_9_on_18_hole_course(eighteen_hole_golf_course):
    hole_list = utils.get_holes_for_game(eighteen_hole_golf_course, "back-9")
    assert hole_list.count() == 9
    assert hole_list[0].order == 10
    assert hole_list.last().order == 18

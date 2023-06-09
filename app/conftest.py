import pytest
from django.contrib.auth import get_user_model
from home import models
from dashboard import utils as dashboard_utils


@pytest.fixture
def normal_user():
    user = get_user_model().objects.create_user("test@example.com", "testpass123")
    return user


@pytest.fixture
def second_user():
    user = get_user_model().objects.create_user("test2@example.com", "testpass123")
    return user


@pytest.fixture
def player(normal_user):
    player = models.Player.objects.create(
        name="Test Player",
        added_by=normal_user
    )
    return player


@pytest.fixture
def player_two(normal_user):
    player = models.Player.objects.create(
        name="Test Player 2",
        added_by=normal_user
    )
    return player


@pytest.fixture
def second_player(second_user):
    player = models.Player.objects.create(
        name="Test Player",
        added_by=second_user
    )
    return player


@pytest.fixture
def golf_course():
    course = models.GolfCourse.objects.create(
        name="Test Course",
        hole_count="9",
    )
    return course


@pytest.fixture
def eighteen_hole_golf_course():
    course = models.GolfCourse.objects.create(
        name="Test Big Course",
        hole_count="18",
    )

    dashboard_utils.create_holes_for_course(course)

    return course


@pytest.fixture
def golf_game(golf_course):
    game = models.Game.objects.create(
        course=golf_course,
        holes_played="9",
    )
    return game


@pytest.fixture
def golf_game_with_player(golf_game, player):
    golf_game.players.add(player)
    return golf_game

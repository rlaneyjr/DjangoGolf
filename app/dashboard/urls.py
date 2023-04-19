from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.course_list, name="courses"),
    path("courses/add/", views.create_course, name="create_course"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("holes/<int:pk>/", views.hole_detail, name="hole_detail"),
    path("tees/<int:hole_pk>/", views.create_tee, name="create_tee"),
    path("games/", views.game_list, name="games"),
    path("games/<int:pk>/", views.game_detail, name="game_detail"),
    path("players/", views.player_list, name="players"),
    path("players/<int:pk>/", views.player_detail, name="player_detail"),
    path("players/add/", views.create_player, name="create_player"),
    path("players/<int:pk>/edit/", views.edit_player, name="edit_player"),
    # ajax
    path(
        "ajax/add-player-to-game/",
        views.ajax_manage_players_for_game,
        name="ajax_manage_players_for_game",
    ),
    path("ajax/manage-game/", views.ajax_manage_game, name="ajax_manage_game"),
]

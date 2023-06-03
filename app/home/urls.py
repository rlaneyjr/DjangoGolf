from django.urls import path, include
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.course_list, name="course-list"),
    path("courses/<int:pk>/", views.course_detail, name="course-detail"),
    path("games/<int:pk>/", views.game_detail, name="game-detail"),
    path("games/mine/", views.view_my_games, name="my-game-list"),
    path("profile/", views.my_profile, name="profile"),
    path("player-list/", views.player_list, name="player-list"),
    path("tee-times/add/", views.create_tee_time, name="create-tee-time"),
    path("tee-times/<int:pk>/", views.tee_time_detail, name="tee-time-detail"),
    path("download-scorecard/<int:game_pk>/", views.download_scorecard, name="download-scorecard"),
    path(
        "ajax/record_hole_score/",
        views.ajax_record_hole_score,
        name="ajax-record-hole-score",
    ),
    path("ajax/create-game/", views.ajax_create_game, name="ajax-create-game"),
    path(
        "ajax/add-player-to-game",
        views.ajax_add_player_to_game,
        name="ajax-add-player-to-game",
    ),
    path("ajax/manage-game/", views.ajax_manage_game, name="ajax-manage-game"),
    path("ajax/manage-tee-time/", views.ajax_manage_tee_time, name="ajax-manage-tee-time"),
    path("home/api/", include("home.api.urls")),
]

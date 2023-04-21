from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.course_list, name="course-list"),
    path("courses/<int:pk>/", views.course_detail, name="course-detail"),
    path("games/<int:pk>/", views.game_detail, name="game-detail"),
    path("games/mine/", views.view_my_games, name="my-game-list"),
    path("profile/", views.my_profile, name="profile"),
]

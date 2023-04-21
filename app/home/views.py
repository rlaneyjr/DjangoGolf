from django.shortcuts import render, get_object_or_404
from home import models


def index(request):
    game_list = None
    if request.user.is_authenticated:
        game_list = models.Game.objects.filter(
            status="active", players__in=[request.user.player]
        )
    return render(request, "home/index.html", {"game_list": game_list})


def course_list(request):
    course_list = models.GolfCourse.objects.all().order_by("name")
    return render(request, "home/course_list.html", {"course_list": course_list})


def course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(request, "home/course_detail.html", {"course_data": course_data})


def view_my_games(request):
    game_list = models.Game.objects.filter(players__in=[request.user.player])
    return render(request, "home/view_my_games.html", {"game_list": game_list})


def my_profile(request):
    game_count = models.Game.objects.filter(players__in=[request.user.player]).count()
    return render(request, "home/profile.html", {"game_count": game_count})

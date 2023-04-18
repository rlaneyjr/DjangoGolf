from django.shortcuts import render, redirect, get_object_or_404
from home import models as home_models
from . import forms
from . import utils


def index(request):
    return render(request, "dashboard/index.html", {})


def course_list(request):
    course_list = home_models.GolfCourse.objects.all()
    return render(request, "dashboard/courses.html", {"course_list": course_list})


def create_course(request):
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            utils.create_holes_for_course(course)
            return redirect("dashboard:courses")
    else:
        form = forms.GolfCourseForm()
    return render(request, "dashboard/create_course.html", {"form": form})


def course_detail(request, pk):
    course_data = get_object_or_404(home_models.GolfCourse, pk=pk)
    course_location = None
    hole_list = home_models.Hole.objects.filter(course=course_data).order_by("name")
    if all([course_data.city, course_data.state, course_data.zip_code]):
        course_location = (
            f"{course_data.city}, {course_data.state}, {course_data.zip_code}"
        )
    return render(
        request,
        "dashboard/course_detail.html",
        {
            "course_data": course_data,
            "course_location": course_location,
            "hole_list": hole_list,
        },
    )


def hole_detail(request, pk):
    hole_data = get_object_or_404(home_models.Hole, pk=pk)
    tee_list = home_models.Tee.objects.filter(hole=hole_data)
    course_data = hole_data.course
    return render(
        request,
        "dashboard/hole_detail.html",
        {"hole_data": hole_data, "course_data": course_data, "tee_list": tee_list},
    )


def create_tee(request, hole_pk):
    if request.method == "POST":
        hole_data = get_object_or_404(home_models.Hole, pk=hole_pk)
        form = forms.TeeForm(request.POST)
        if form.is_valid():
            tee = form.save(commit=False)
            tee.hole = hole_data
            tee.save()
            return redirect("dashboard:hole_detail", hole_pk)
    form = forms.TeeForm()
    return render(request, "dashboard/create_tee.html", {"form": form})


def game_list(request):
    game_list = home_models.Game.objects.all()
    return render(request, "dashboard/games.html", {"game_list": game_list})


def game_detail(request, pk):
    game_data = get_object_or_404(home_models.Game, pk=pk)
    return render(request, "dashboard/game_detail.html", {"game_data": game_data})


def player_list(request):
    player_list = home_models.Player.objects.all()
    return render(request, "dashboard/players.html", {"player_list": player_list})

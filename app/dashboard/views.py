import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from home import models as home_models
from . import forms
from . import utils


@login_required
def index(request):
    return render(request, "dashboard/index.html", {})


@login_required
def course_list(request):
    course_list = home_models.GolfCourse.objects.all()
    return render(request, "dashboard/courses.html", {"course_list": course_list})


@login_required
def create_course(request):
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            utils.create_holes_for_course(course)
            messages.add_message(request, messages.INFO, "Course Created.")
            return redirect("dashboard:courses")
    else:
        form = forms.GolfCourseForm()
    return render(request, "dashboard/create_course.html", {"form": form})


@login_required
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


@login_required
def hole_detail(request, pk):
    hole_data = get_object_or_404(home_models.Hole, pk=pk)
    tee_list = home_models.Tee.objects.filter(hole=hole_data)
    course_data = hole_data.course
    return render(
        request,
        "dashboard/hole_detail.html",
        {"hole_data": hole_data, "course_data": course_data, "tee_list": tee_list},
    )


@login_required
def create_tee(request, hole_pk):
    if request.method == "POST":
        hole_data = get_object_or_404(home_models.Hole, pk=hole_pk)
        form = forms.TeeForm(request.POST)
        if form.is_valid():
            tee = form.save(commit=False)
            tee.hole = hole_data
            tee.save()
            messages.add_message(request, messages.INFO, "Tee Created.")
            return redirect("dashboard:hole_detail", hole_pk)
    form = forms.TeeForm()
    return render(request, "dashboard/create_tee.html", {"form": form})


@login_required
def game_list(request):
    game_list = home_models.Game.objects.all()
    return render(request, "dashboard/games.html", {"game_list": game_list})


@login_required
def game_detail(request, pk):
    game_data = get_object_or_404(home_models.Game, pk=pk)
    player_list = home_models.Player.objects.all().exclude(game__in=[game_data.id])
    return render(
        request,
        "dashboard/game_detail.html",
        {"game_data": game_data, "player_list": player_list},
    )


@login_required
def player_list(request):
    player_list = home_models.Player.objects.all()
    return render(request, "dashboard/players.html", {"player_list": player_list})


@login_required
def player_detail(request, pk):
    player_data = get_object_or_404(home_models.Player, pk=pk)
    return render(request, "dashboard/player_detail.html", {"player_data": player_data})


@login_required
def create_player(request):
    if request.method == "POST":
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Player Created.")
            return redirect("dashboard:players")
    else:
        form = forms.PlayerForm()
    return render(request, "dashboard/create_player.html", {"form": form})


@login_required
def edit_player(request, pk):
    player_data = get_object_or_404(home_models.Player, pk=pk)
    if request.method == "POST":
        form = forms.PlayerForm(request.POST, instance=player_data)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Player Saved.")
            return redirect("dashboard:player_detail", pk)
    else:
        form = forms.PlayerForm(instance=player_data)
    return render(request, "dashboard/create_player.html", {"form": form})


@login_required
def create_game(request):
    if request.method == "POST":
        form = forms.GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.date_played = timezone.now()
            game.save()
            return redirect("dashboard:game_detail", game.id)
    else:
        form = forms.GameForm()
    return render(request, "dashboard/create_game.html", {"form": form})


@login_required
def ajax_manage_players_for_game(request):
    data = json.loads(request.body)
    if not all([data["playerId"], data["game"], data["action"]]):
        return HttpResponseBadRequest("Missing Data")
    game_data = home_models.Game.objects.filter(pk=data["game"]).first()
    player_data = home_models.Player.objects.filter(pk=data["playerId"]).first()
    if not all([game_data, player_data]):
        return HttpResponseBadRequest("Unable to find either game or player")

    if data["action"] == "add-player":
        if player_data in game_data.players.all():
            return HttpResponseBadRequest("Player already part of game")
        game_data.players.add(player_data)
    elif data["action"] == "remove-player":
        game_data.players.remove(player_data)
    return JsonResponse({"status": "success"})


@login_required
def ajax_manage_game(request):
    data = json.loads(request.body)
    if data["action"] == "delete-game":
        game_id = data["gameId"]
        game_data = home_models.Game.objects.filter(pk=game_id).first()
        if game_data is None:
            return HttpResponseBadRequest("Cannot find game with that id")

        game_data.delete()
        messages.add_message(request, messages.INFO, "Game Deleted.")
        return JsonResponse({"status": "success"})
    return HttpResponseBadRequest("Unknown Action")

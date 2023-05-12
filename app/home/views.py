import json
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from home import models
from dashboard import forms as dashboard_forms


def index(request):
    game_list = None
    tee_time_list = None
    if request.user.is_authenticated:
        game_list = models.Game.objects.filter(
            status="active", players__in=[request.user.player]
        )
        tee_time_list = models.TeeTime.objects.filter(players__in=[request.user.player], is_active=True)

    return render(
        request,
        "home/index.html",
        {"game_list": game_list, "tee_time_list": tee_time_list},
    )


def course_list(request):
    course_list = models.GolfCourse.objects.all().order_by("name")
    return render(request, "home/course_list.html", {"course_list": course_list})


def course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(request, "home/course_detail.html", {"course_data": course_data})


@login_required
def game_detail(request, pk):
    hole_num = int(request.GET.get("hole", 1))
    game_data = get_object_or_404(models.Game, pk=pk)
    hole_data = None
    next_hole = None
    prev_hole = None
    hole_scores = []
    available_players = []
    player_scores = {}

    if game_data.status == "setup":
        available_players = models.Player.objects.all().exclude(game__in=[game_data.id])

        game_links = models.PlayerGameLink.objects.filter(
            player__in=game_data.players.all(), game=game_data
        )
        for game_link in game_links:
            if game_link.player.name not in player_scores.keys():
                player_scores[game_link.player.name] = 0

    if game_data.status in ["active", "completed"]:
        hole_data = models.Hole.objects.filter(
            course=game_data.course, order=hole_num
        ).first()
        game_links = models.PlayerGameLink.objects.filter(
            player__in=game_data.players.all(), game=game_data
        )
        next_hole = models.Hole.objects.filter(
            course=game_data.course, order=hole_num + 1
        ).first()
        prev_hole = models.Hole.objects.filter(
            course=game_data.course, order=hole_num - 1
        ).first()

        for game_link in game_links:
            hole_score = models.HoleScore.objects.filter(
                hole=hole_data, game=game_link
            ).first()
            hole_scores.append(
                {
                    "player": game_link.player.name,
                    "hole_score_id": hole_score.id,
                    "score": hole_score.score,
                }
            )
            hole_score_list = models.HoleScore.objects.filter(game=game_link)
            for hole_score_item in hole_score_list:
                if game_link.player.name not in player_scores.keys():
                    player_scores[game_link.player.name] = 0
                player_scores[game_link.player.name] += hole_score_item.score

    return render(
        request,
        "home/game_detail.html",
        {
            "game_data": game_data,
            "hole_scores": hole_scores,
            "current_hole": hole_data,
            "next_hole": next_hole,
            "prev_hole": prev_hole,
            "available_players": available_players,
            "player_scores": player_scores,
        },
    )


@login_required
def tee_time_detail(request, pk):
    tee_time_data = get_object_or_404(models.TeeTime, pk=pk)
    potential_player_list = models.Player.objects.all().exclude(teetime__in=[tee_time_data.id])
    return render(
        request,
        "home/tee-time-detail.html",
        {"tee_time_data": tee_time_data, "potential_player_list": potential_player_list}
    )


@login_required
def create_tee_time(request):
    if request.method == "POST":
        form = dashboard_forms.TeeTimeForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect("home:tee-time-detail", item.id)
    else:
        form = dashboard_forms.TeeTimeForm()
    return render(request, "home/create-tee-time.html", {"form": form})


@login_required
def view_my_games(request):
    game_list = models.Game.objects.filter(players__in=[request.user.player])
    return render(request, "home/view_my_games.html", {"game_list": game_list})


@login_required
def my_profile(request):
    game_count = models.Game.objects.filter(players__in=[request.user.player]).count()
    return render(request, "home/profile.html", {"game_count": game_count})


@login_required
def ajax_record_hole_score(request):
    data = json.loads(request.body)
    game_id = data["game_id"]
    game_data = models.Game.objects.filter(pk=game_id).first()
    if game_data is None:
        return JsonResponse({"status": "failed"})

    if game_data.status != "active":
        return JsonResponse({"status": "failed"})

    score_list = data["scores"]
    for score in score_list:
        hole_score = models.HoleScore.objects.filter(pk=score["score_id"]).first()
        if hole_score is None:
            return JsonResponse({"status": "failed"})
        hole_score.score = score["score"]
        hole_score.save()

    return JsonResponse({"status": "success"})


@login_required
def ajax_create_game(request):
    data = json.loads(request.body)
    course_data = models.GolfCourse.objects.filter(pk=data["course_id"]).first()
    if course_data is None:
        return JsonResponse({"status": "failed"})

    game = models.Game.objects.create(course=course_data, date_played=timezone.now())
    game.players.add(request.user.player)
    return JsonResponse(
        {
            "status": "success",
            "game_url": settings.BASE_URL + reverse("home:game-detail", args=[game.id]),
        }
    )


@login_required
def ajax_add_player_to_game(request):
    data = json.loads(request.body)
    game_id = data["game_id"]
    player_id = data["player_id"]

    game_data = models.Game.objects.filter(pk=game_id).first()
    player_data = models.Player.objects.filter(pk=player_id).first()

    game_data.players.add(player_data)

    return JsonResponse({"status": "success"})


@login_required
def ajax_manage_game(request):
    data = json.loads(request.body)
    game_id = data["game_id"]
    action = data["action"]

    game_data = models.Game.objects.filter(pk=game_id).first()
    if game_data is None:
        return JsonResponse({"status": "failed"})

    if action == "start-game":
        game_data.status = "active"
        game_data.save()

        hole_list = models.Hole.objects.filter(course=game_data.course)
        for hole in hole_list:
            for player in game_data.players.all():
                game_link = models.PlayerGameLink.objects.filter(
                    player=player, game=game_data
                ).first()
                hole_score = models.HoleScore(hole=hole, game=game_link)
                hole_score.save()

        return JsonResponse({"status": "success"})
    elif action == "complete-game":
        game_data.status = "completed"
        game_data.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})


@login_required
def ajax_manage_tee_time(request):
    data = json.loads(request.body)
    action = data["action"]

    if action == "add-player":
        tee_time_id = data["tee_time_id"]
        player_id = data["player_id"]
        tee_time = models.TeeTime.objects.filter(pk=tee_time_id).first()
        player_data = models.Player.objects.filter(pk=player_id).first()
        if tee_time is None or player_data is None:
            return JsonResponse({"status": "failed"})
        tee_time.players.add(player_data)
        return JsonResponse({"status": "success"})
    elif action == "start-game":
        tee_time_id = data.get("tee_time_id", None)
        if tee_time_id is None:
            return JsonResponse({"status": "failed"})
        tee_time = models.TeeTime.objects.filter(pk=tee_time_id).first()
        if tee_time is None:
            return JsonResponse({"status": "failed"})

        new_game = models.Game.objects.create(
            date_played=tee_time.tee_time,
            course=tee_time.course,
            holes_played=tee_time.holes_to_play,
        )

        # add players from tee time to game
        for player in tee_time.players.all():
            new_game.players.add(player)

        tee_time.is_active = False
        tee_time.save()

        return JsonResponse({
            "status": "success",
            "game_url": settings.BASE_URL + reverse("home:game-detail", args=[new_game.id])}
        )
    return JsonResponse({"status": "failed", "message": "Unknown Action"})

import json
from django.shortcuts import reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from home import models


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
        return JsonResponse({"status": "failed", "message": "Unable to find course"})

    game = models.Game.objects.create(
        course=course_data,
        date_played=timezone.now(),
        holes_played=course_data.hole_count
    )
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

    if game_data is None or player_data is None:
        return JsonResponse({"status": "failed", "message": "Unable to find player or game"})

    game_data.players.add(player_data)

    return JsonResponse({"status": "success"})


@login_required
def ajax_manage_game(request):
    data = json.loads(request.body)
    game_id = data["game_id"]
    action = data["action"]

    game_data = models.Game.objects.filter(pk=game_id).first()
    if game_data is None:
        return JsonResponse({
            "status": "failed",
            "message": f"Unable to find game with ID: {game_id}"
        })

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
    elif data["action"] == "toggle-league-game":
        game_data.league_game = not game_data.league_game
        game_data.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed", "message": "Unknown Error"})


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
            return JsonResponse({"status": "failed", "message": "Unable to find tee time or player"})
        tee_time.players.add(player_data)
        return JsonResponse({"status": "success"})
    elif action == "start-game":
        tee_time_id = data.get("tee_time_id", None)
        if tee_time_id is None:
            return JsonResponse({"status": "failed", "message": "Unable to find tee time id"})
        tee_time = models.TeeTime.objects.filter(pk=tee_time_id).first()
        if tee_time is None:
            return JsonResponse({"status": "failed", "message": "Unable to find tee time"})

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

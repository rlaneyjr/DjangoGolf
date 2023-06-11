from home import models


def get_players_for_game(user, game):
    return models.Player.objects.filter(
        added_by=user
    ).exclude(
        game__in=[game.id]
    )


def get_holes_for_game(course, holes_to_play):
    hole_list = models.Hole.objects.filter(course=course).order_by("order")

    if course.hole_count == holes_to_play:
        return hole_list

    if course.hole_count == "18" and holes_to_play == "front-9":
        return hole_list.filter(order__gte=1, order__lt=10)

    if course.hole_count == "18" and holes_to_play == "back-9":
        return hole_list.filter(order__gte=10)

    return None

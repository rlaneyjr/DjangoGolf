from django.shortcuts import get_object_or_404
from . import serializers
from home import models
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class GolfCourseViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.GolfCourse.objects.all()
        serializer = serializers.GolfCourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.GolfCourse.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = serializers.GolfCourseSerializer(course)
        return Response(serializer.data)


class GameViewSet(viewsets.ViewSet):
    """
        Note: Should only be able to list your own games
    """

    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = models.Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        serializer = serializers.GameSerializer(game, many=False)
        return Response(serializer.data)

    def list(self, request):
        queryset = models.Game.objects.all()
        serializer = serializers.GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_name="add_player")
    def add_player(self, request, pk=None):
        queryset = models.Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        player_id = request.data.get("player")
        player_data = get_object_or_404(models.Player, pk=player_id)
        game.players.add(player_data)
        serializer = serializers.GameSerializer(game, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_name="remove_player")
    def remove_player(self, request, pk=None):
        queryset = models.Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        player_id = request.data.get("player")
        player_data = get_object_or_404(models.Player, pk=player_id)
        game.players.remove(player_data)
        serializer = serializers.GameSerializer(game, many=False)
        return Response(serializer.data)


class PlayerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = models.Player.objects.filter(added_by=request.user)
        serializer = serializers.PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)
        return Response(serializer.data)


class TeeTimeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        player = request.user.player
        queryset = models.TeeTime.objects.filter(players__in=[player])
        serializer = serializers.TeeTimeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        player = request.user.player
        queryset = models.TeeTime.objects.filter(players__in=[player])
        tee_time = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TeeTimeSerializer(tee_time, many=False)
        return Response(serializer.data)


class TeeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = models.Tee.objects.all()
        tee = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TeeSerializer(tee, many=False)
        return Response(serializer.data)

    def list(self, request):
        queryset = models.Tee.objects.all()
        serializer = serializers.TeeSerializer(queryset, many=True)
        return Response(serializer.data)

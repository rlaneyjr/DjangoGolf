from django.shortcuts import get_object_or_404
from . import serializers
from home import models
from rest_framework import viewsets
from rest_framework.response import Response


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

    def list(self, request):
        queryset = models.Game.objects.all()
        serializer = serializers.GameSerializer(queryset, many=True)
        return Response(serializer.data)


class PlayerViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.Player.objects.filter(added_by=request.user)
        serializer = serializers.PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)
        return Response(serializer.data)

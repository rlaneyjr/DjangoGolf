from . import serializers
from home import models
from rest_framework import viewsets
from rest_framework.response import Response


class GolfCourseViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.GolfCourse.objects.all()
        serializer = serializers.GolfCourseSerializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework import serializers
from home import models
from core.api import serializers as core_serializers


class PlayerSerializer(serializers.ModelSerializer):
    added_by = core_serializers.UserSerializer(many=False, read_only=True)
    user_account = core_serializers.UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Player
        fields = [
            "id",
            "name",
            "added_by",
            "user_account"
        ]

    def create(self, validated_data):
        return models.Player.objects.create(**validated_data)


class GolfCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GolfCourse
        fields = [
            "id",
            "name",
            "hole_count",
            "tee_time_link",
            "website_link",
            "city",
            "state",
            "zip_code"
        ]


class GameSerializer(serializers.ModelSerializer):
    course = GolfCourseSerializer(many=False, read_only=True)

    class Meta:
        model = models.Game
        fields = [
            "id",
            "date_played",
            "course",
            "holes_played",
            "status",
            "league_game",
            "players"
        ]

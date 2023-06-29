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

    def create(self, validated_data):
        return models.Game.objects.create(**validated_data)

    def validate(self, attrs):
        course_id = attrs.pop("course_id", None)
        if course_id is None:
            raise serializers.ValidationError("Unable to find course id")
        attrs["course"] = models.GolfCourse.objects.filter(pk=course_id).first()
        return attrs


class TeeTimeSerializer(serializers.ModelSerializer):
    course = GolfCourseSerializer(many=False)
    players = PlayerSerializer(many=True)

    class Meta:
        model = models.TeeTime
        fields = [
            "id",
            "course",
            "tee_time",
            "holes_to_play",
            "is_active",
            "players"
        ]


class TeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tee
        fields = [
            "id",
            "name",
            "distance",
            "hole"
        ]

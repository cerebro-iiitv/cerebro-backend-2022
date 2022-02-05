from rest_framework import serializers

from accounts.models import Account
from registration.models import TeamMember


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "institute_name","address","degree","password","proof"]

class RegisteredEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.title")
    team_code = serializers.CharField(source="team.team_code")
    start_time = serializers.CharField(source="event.start_time")
    end_time = serializers.CharField(source="event.end_time")

    class Meta:
        model = TeamMember
        fields = ["event_name", "team_code", "start_time", "end_time", "id"]

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=64, min_length=7)

    class Meta:
        fields = "__all__"


class AccountDashboardSerializer(serializers.ModelSerializer):
    user_team = RegisteredEventSerializer(many=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "profile_pic", "user_team"]

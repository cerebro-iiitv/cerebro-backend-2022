from docs.models import ProofPDF
from registration.models import (IndividualParticipation, TeamMember,
                                 TeamParticipation)
from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    proof_id = serializers.PrimaryKeyRelatedField(queryset = ProofPDF.objects.all(), many = False)
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "institute_name","address","degree","password","proof", "proof_id"]
        read_only_fields = ("proof", )
        extra_kwargs = {
            'proof_id': {'write_only': True},
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=64, min_length=7)

    class Meta:
        fields = "__all__"


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        min_length=6, max_length=68)
    password2 = serializers.CharField(
        min_length=6, max_length=68)
    token = serializers.CharField(
        min_length=1)
    uidb64 = serializers.CharField(
        min_length=1)

    class Meta:
        fields = ['password1', 'password2', 'token', 'uidb64']

class ChangePasswordSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(
        min_length=6, max_length=68)
    new_password1 = serializers.CharField(
        min_length=6, max_length=68)
    new_password2 = serializers.CharField(
        min_length=6, max_length=68)
    
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

class IndividualParticipationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source = "event.title")
    start_time = serializers.CharField(source = "event.start_time")
    end_time = serializers.CharField(source = "event.end_time")
    is_team_event = serializers.BooleanField(source="event.team_event")
    class Meta:
        model = IndividualParticipation
        fields = ["event_title", "start_time", "end_time", "is_team_event", "registration_data", "submission_data"]

class TeamMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source = "account.first_name")
    last_name = serializers.CharField(source = "account.last_name")
    email = serializers.CharField(source = "account.email")
    
    class Meta:
        model = TeamMember
        fields = ["first_name", "last_name", "email", "registration_data"]

class TeamParticipationSerializer(serializers.ModelSerializer):
    team_member = TeamMemberSerializer(many = True)
    event_title = serializers.CharField(source = "event.title")
    start_time = serializers.CharField(source = "event.start_time")
    end_time = serializers.CharField(source = "event.end_time")
    max_size = serializers.IntegerField(source = "event.team_size")
    is_team_event = serializers.BooleanField(source="event.team_event")
    team_captain = serializers.CharField(source = "team_captain.email")
    class Meta:
        model = TeamParticipation
        fields = [
            "event_title", 
            "start_time", 
            "end_time", 
            "is_team_event",
            "max_size",
            "team_captain",
            "team_name",
            "current_size",
            "is_full",
            "team_code",
            "submission_data",
            "team_member"
        ]

class AccountDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["first_name", "last_name","institute_name", "email", "mobile_number"]

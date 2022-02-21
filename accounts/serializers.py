from rest_framework import serializers

from accounts.models import Account
from registration.models import TeamMember
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from docs.models import ProofPDF

class AccountSerializer(serializers.ModelSerializer):
    proof_id = serializers.PrimaryKeyRelatedField(queryset = ProofPDF.objects.all(), many = False)
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "institute_name","address","degree","password","proof", "proof_id"]
        read_only_fields = ("proof", )
        extra_kwargs = {
            'proof_id': {'write_only': True},
        }

class RegisteredEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.title")
    team_code = serializers.CharField(source="team.team_code")
    start_time = serializers.CharField(source="event.start_time")
    end_time = serializers.CharField(source="event.end_time")

    class Meta:
        model = TeamMember
        fields = ["event_name", "team_code", "start_time", "end_time", "id"]


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

class AccountDashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["first_name", "last_name","institute_name", "email", "mobile_number"]

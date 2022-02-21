from rest_framework import serializers
from registration.models import TeamMember, TeamParticipation, IndividualParticipation


class IndividualParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualParticipation
        fields = "__all__"
        read_only_fields = ["account"]

class TeamMemberSerializer(serializers.ModelSerializer):
    team_code = serializers.CharField(required=False, source="team.team_code")

    class Meta:
        model = TeamMember
        fields = "__all__"
        read_only_fields = ["account", "event", "team"]

class TeamParticipationSerializer(serializers.ModelSerializer):
    team_captain = TeamMemberSerializer()
    class Meta:
        model = TeamParticipation
        fields = "__all__" 
        read_only_fieldsjs = ["team_creator", "current_size", "is_full", "team_code"]
        
class TeamSubmissionSerializer(serializers.ModelSerializer):
    team_captain = TeamMemberSerializer(many=False, read_only= True)
    class Meta:
        model = TeamParticipation
        fields = "__all__" 
        read_only_fieldsjs = ["team_creator", "current_size", "is_full", "team_code"]


class SubmissionSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    submission_data = serializers.JSONField()
    
    class Meta:
        fields = "__all__" 


from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.response import Response

from team.models import Team
from team.serializers import TeamSerializer


class TeamViewSet(ReadOnlyModelViewSet):
    serializer_class = TeamSerializer

    def list(self, request, *args, **kwargs):
        team_choices = [
            ("core", "Core"),
            ("core-support", "Core Support"),
            ("web", "Web Dev"),
            ("design", "Design"),
            ("video-editing", "Video Editing"),
            ("pr", "PR"),
            ("gaming", "Gaming"),
            ("sponsorship", "Sponsorship")
        ]

        data = dict()

        for choice in team_choices:
            team = Team.objects.filter(team=choice[0]).order_by("priority")
            data[choice[1]] = self.serializer_class(team, many=True, context={"request": request}).data

        return Response(data, status=status.HTTP_200_OK)

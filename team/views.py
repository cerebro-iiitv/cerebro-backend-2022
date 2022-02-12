import imp
import stat
from typing import OrderedDict
from httplib2 import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from team.models import Team
from team.serializers import TeamSerializer


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.GET.get("team") is not None:
            team = self.request.GET.get("team")
            return Team.objects.filter(team=team).order_by("priority")

        return Team.objects.all().order_by("priority")

    def list(self, request, *args, **kwargs):
        team_choices = [
            ("core", "Core"),
            ("core-support", "Core Support"),
            ("web", "Web Dev"),
            ("design", "Design"),
            ("video-editing", "Video Editing"),
            ("pr", "PR"),
            ("gaming", "Gaming"),
        ]

        data = dict()

        for choice in team_choices:
            team = Team.objects.filter(team=choice[0]).order_by("priority")
            data[choice[1]] = self.serializer_class(team, many=True).data

        print(data)

        return Response(data, status=status.HTTP_200_OK)

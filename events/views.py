from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from events.models import Contact, Event
from events.serializers import ContactSerializer, EventSerializer

from registration.models import IndividualParticipation, TeamMember


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.GET.get("type") is not None:
            event_type = self.request.GET.get("type")
            return Event.objects.filter(event_type=event_type).order_by("priority")

        return Event.objects.all().order_by("priority")

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        else:
            events = self.get_queryset()
            events_data = list(self.serializer_class(events, many=True).data)

            zip_data = zip(events, events_data)

            response_data = []

            for data in zip_data:
                event = data[0]
                try:
                    participation = IndividualParticipation.objects.get(event=event, account=request.user)
                    data[1]["is_registered"] = True
                    if participation.submission_data is not None:
                       data[1]["submitted"] = True
                    else:
                        data[1]["submitted"] = False
                except IndividualParticipation.DoesNotExist:
                    try:
                        team_member = TeamMember.objects.get(event=event, account=request.user)
                        data[1]["is_registered"] = True
                        if team_member.team.submission_data is not None:
                            data[1]["submitted"] = True
                        else:
                            data[1]["submitted"] = False
                    except TeamMember.DoesNotExist:
                        data[1]["is_registered"] = False
                        data[1]["submitted"] = False 

                response_data.append(data[1])

            return Response(response_data, status = status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)
        else:
            event = self.get_object()
            event_data = self.serializer_class(event).data

            try:
                participation = IndividualParticipation.objects.get(event=event, account=request.user)
                event_data["is_registered"] = True
                if participation.submission_data is not None:
                    event_data["submitted"] = True
                else:
                    event_data["submitted"] = False
            except IndividualParticipation.DoesNotExist:
                try:
                    team_member = TeamMember.objects.get(event=event, account=request.user)
                    event_data["is_registered"] = True
                    if team_member.team.submission_data is not None:
                        event_data["submitted"] = True
                    else:
                        event_data["submitted"] = False
                except TeamMember.DoesNotExist:
                    event_data["is_registered"] = False
                    event_data["submitted"] = False 


            return Response(event_data, status = status.HTTP_200_OK)



class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all().order_by("priority")

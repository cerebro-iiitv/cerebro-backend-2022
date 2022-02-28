import random

from accounts.authentication import MultipleTokenAuthentication
from events.models import Event
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from registration.models import (IndividualParticipation, TeamMember,
                                 TeamParticipation)
from registration.serializers import (IndividualParticipationSerializer,
                                      SubmissionSerializer,
                                      TeamMemberSerializer,
                                      TeamParticipationSerializer)
from registration.utils import (validate_registration_data,
                                validate_submission_data)


class IndividualRegistrationViewSet(ModelViewSet):
    serializer_class = IndividualParticipationSerializer
    queryset = IndividualParticipation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        event = serializer.validated_data.get("event")

        # Checking if given event is individual event or not
        if event.team_size != 1:
            return Response({"Error": f"Event {event.title} is a team based event"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if user is alredy registered to the event:
        if IndividualParticipation.objects.filter(account=request.user, event=event).exists():
            return Response({"error": f"User already registered in event {event.title}"}, status=status.HTTP_400_BAD_REQUEST)

        # While registering one should not provide submission details
        if "submission_data" in serializer.validated_data.keys():
            return Response({"error": "Submission can't be provided while registering"}, status=status.HTTP_400_BAD_REQUEST)

        # Validating registration data provided by the user
        registration_attributes = event.registration_attributes
        registration_data = serializer.validated_data.get("registration_data", None)
        error_message = validate_registration_data(registration_attributes, registration_data)

        if error_message is not None:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        data["account"] = request.user

        participant = IndividualParticipation.objects.create(**data)
        participant.save()
        participant_serialized = IndividualParticipationSerializer(participant)
        return Response(participant_serialized.data, status=status.HTTP_201_CREATED)
    

class TeamRegistrationViewSet(ModelViewSet):
    serializer_class = TeamParticipationSerializer
    queryset = TeamParticipation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        event = serializer.validated_data.get("event")

        if event.team_size == 1:
            return Response({"Error": f"{event.title} is not a team event"})

        # Verify if the person creating team is already not a part of some other team of the same event
        if TeamMember.objects.filter(event=event, account=request.user).exists():
            return Response({"Error": "Given user is already a memeber of a team in this event"}, status=status.HTTP_400_BAD_REQUEST)     

        # Verify if team name is unique
        team_name = serializer.validated_data.get("team_name")
        if TeamParticipation.objects.filter(event=event, team_name=team_name).exists():
            return Response({"Error": f"Team name already taken in the event {event.title}"}, status=status.HTTP_400_BAD_REQUEST)

        #While registering one should not provide submission details
        if "submission_data" in serializer.validated_data.keys():
            return Response({"error": "Submission can't be provided while registering"}, status=status.HTTP_400_BAD_REQUEST)

        # Generating Team Code
        while(True):
            team_code = (
                event.short_name + "#" + f"{random.randint(0, 100000)}".zfill(5)
            )
            if not TeamParticipation.objects.filter(team_code=team_code).exists():
                break

        data = serializer.validated_data

        # Extract participation details of team creator
        team_captain = data.pop("team_captain")

        # Validating registration data provided by the team captain
        registration_attributes = event.registration_attributes
        registration_data = team_captain.get("registration_data", None)
        error_message = validate_registration_data(registration_attributes, registration_data)

        if error_message is not None:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        data["team_code"] = team_code
        data["team_captain"] = request.user

        # Creating team
        team = TeamParticipation.objects.create(**data)
        team.save()

        team_captain["team"] = team
        team_captain["account"] = request.user
        team_captain["event"] = event

        # Creating team captain object
        team_captain = TeamMember.objects.create(**team_captain)
        team_captain.save()

        return Response(
            {
                "success": "Team created successfully",
                "team_name": team.team_name,
                "team_code": team.team_code,
                "team_captain": request.user.email
            },
            status=status.HTTP_201_CREATED
        )
    
class SubmissionViewset(generics.GenericAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        
        event_id = serializer.validated_data.get("event_id")
        submission_data = serializer.validated_data.get("submission_data", None)
        
        event = Event.objects.get(id=event_id)
        is_team_event = event.team_event # True for team event, False for individual event
        
        if not is_team_event:
            if not IndividualParticipation.objects.filter(account_id=request.user, event=event).exists():
                return Response({"error": f"User is not registered in the event {event.title}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if is_team_event:
            try:
                team_code = self._get_user_teamCode(user=request.user, event_id= event_id)
                if not TeamParticipation.objects.filter(event_id=event_id, team_code= team_code).exists():
                    raise(Exception("User not found!"))
            except:
                return Response({"error": f"User is not registered in the event {event.title}"}, status=status.HTTP_400_BAD_REQUEST)
                
        if not event.submission_closed:
            
            submission_attributes = event.submission_attributes
            error_message = validate_submission_data(submission_attributes, submission_data)
                
            if error_message is not None:
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            
            if not is_team_event:
                
                submission = IndividualParticipation.objects.get(event_id=event_id, account_id =request.user.id)
                submission.submission_data = submission_data
                submission.save()
                
                return Response({'success': f"Submitted successfully for event {event.title}"}, status=status.HTTP_200_OK)
            
            else:
                team = TeamParticipation.objects.get(event_id=event_id, team_code=team_code)
                
                if team.is_full :
                    submission = TeamParticipation.objects.get(event_id=event_id, team_code= team_code)
                    submission.submission_data = submission_data
                    submission.save()
                    return Response({'success': f"Submitted successfully for event {event.title}"}, status=status.HTTP_200_OK)
                
                else:
                    return Response({"error": f"To submit for {event.title}, you need a team of size {event.team_size}!"}, status=status.HTTP_400_BAD_REQUEST)
                      
        else:
            return Response({"error": f"Submission has been closed for {event.title}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def _get_user_teamCode(self, user, event_id):
        obj = TeamMember.objects.get(account_id = user.id, event_id = event_id)
        return obj.team.team_code
            
         
class TeamMemberViewSet(ModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        # Validating team code
        event_id = request.data.get("event_id")
        team_code = serializer.validated_data.get("team").get("team_code")
        
        try:
            team = TeamParticipation.objects.get(team_code=team_code)
        except TeamParticipation.DoesNotExist:
            return Response({"error": "Invalid team code"}, status=status.HTTP_400_BAD_REQUEST)

        event = team.event
        
        if event_id != event.id:
            return Response({"error": f"Invalid team code {team_code} for event {event.title}."}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if given event is team based event or not
        if event.team_size == 1:
            return Response({"error": f"{event.title} is a team based event"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if the user is not already a part of some other team in the event
        if TeamMember.objects.filter(event=event, account=request.user).exists():
            return Response({"error": f"User is already a part of a team in {event.title}"})

        # Check if the team is full or not
        if team.is_full:
            return Response({"error": "Team is already full"}, status=status.HTTP_400_BAD_REQUEST)

        # Validating registration data provided by the user
        registration_attributes = event.registration_attributes
        registration_data = serializer.validated_data.get("registration_data", None)
        error_message = validate_registration_data(registration_attributes, registration_data)

        if error_message is not None:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        data.pop("team")

        data["account"] = request.user
        data["event"] = event
        data["team"] = team

        # Creating team member object
        team_member = TeamMember.objects.create(**data)
        team_member.save()

        team.current_size += 1

        if team.current_size == event.team_size:
            team.is_full = True

        team.save()

        return Response(
            {"success": f"{request.user.first_name} {request.user.last_name} registered to team {team.team_name} in event {event.title}"},
            status=status.HTTP_201_CREATED
        )


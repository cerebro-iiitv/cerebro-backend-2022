import json
import random
import csv
from tokenize import Token
from django.db.models.deletion import DO_NOTHING
import pandas as pd

from rest_framework.views import APIView

from accounts.authentication import MultipleTokenAuthentication
from accounts.models import Account
from django.shortcuts import render
from events.models import Event
from rest_framework import permissions, status, generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from registration.models import (
    IndividualParticipation,
    TeamMember,
    TeamParticipation)
from registration.serializers import (
    IndividualParticipationSerializer,
    SubmissionSerializer,
    TeamMemberSerializer,
    TeamParticipationSerializer)
from registration.utils import validate_registration_data, validate_submission_data


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
            print(serializer.errors)
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
        
        if not IndividualParticipation.objects.filter(account_id=request.user, event=event).exists():
            return Response({"error": f"User is not registered in the event {event.title}"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not event.submission_closed:
            
            if not event.team_event:
                submission_attributes = event.submission_attributes
                error_message = validate_submission_data(submission_attributes, submission_data)
                
                if error_message is not None:
                    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
                
                submission = IndividualParticipation.objects.get(event_id=event_id, account_id =request.user.id)
                submission.submission_data = submission_data
                submission.save()
                
                return Response({'success': f"Submitted successfully for event {event.title}"}, status=status.HTTP_200_OK)
                
            else:
                return Response({"error": f"{event.title} is not an individual participation event"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"error": f"Submission has been closed for {event.title}"}, status=status.HTTP_400_BAD_REQUEST)
            
         
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
        team_code = serializer.validated_data.get("team").get("team_code")
        print(team_code)
        try:
            team = TeamParticipation.objects.get(team_code=team_code)
        except TeamParticipation.DoesNotExist:
            return Response({"error": "Invalid team code"}, status=status.HTTP_400_BAD_REQUEST)

        event = team.event

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
            team.isfull = True

        team.save()

        return Response(
            {"success": f"{request.user.first_name} {request.user.last_name} registered to team {team.team_name} in event {event.title}"},
            status=status.HTTP_201_CREATED
        )



        

        

        

        

        
        

        

        

        


        
        

# class TeamRegistrationViewSet(ModelViewSet):
#     serializer_class = TeamMemberSerializer
#     queryset = TeamMember.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]
#     http_method_names = ["post", "delete"]

#     def list(self, request):
#         raise MethodNotAllowed("GET", detail="Method 'GET' not allowed without lookup")

#     def create(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
#             )
#         account_id = request.data.get("account")
#         event_id = request.data.get("event")
#         team_code = request.data.get("team_code")

#         try:
#             account = Account.objects.get(id=account_id)
#             if request.user == account.user:
#                 team_member = TeamMember.objects.get(account=account_id, event=event_id)
#                 print("Already registered")
#                 return Response(
#                     {
#                         "Error": f"{team_member.account.user.first_name}, you have already registered to the event!"
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             else:
#                 print("Invalid token, user and token's user don't match")
#                 return Response(
#                     {"error": "Invalid Token"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except TeamMember.DoesNotExist:
#             account = Account.objects.get(id=account_id)

#             # Check if the account is owned by the individual or he/she is an imposter
#             if request.user == account.user:
#                 event = Event.objects.get(id=event_id)
#                 if team_code:
#                     team_code = team_code.upper()
#                     try:
#                         reg_team = TeamStatus.objects.get(team_code=team_code)
#                         if event_id != reg_team.event.id:
#                             print("event id and dosen't match provided team code")
#                             print(event_id)
#                             print(reg_team.event.id)
#                             return Response(
#                                 {"Error": "Invalid Team Code"},
#                                 status=status.HTTP_400_BAD_REQUEST,
#                             )
#                         if reg_team.current_size < event.team_size:
#                             team_member = TeamMember.objects.create(
#                                 account=account, event=event, team=reg_team
#                             )
#                             reg_team.current_size += 1

#                             # Check if the team is full or not
#                             if reg_team.current_size == reg_team.event.team_size:
#                                 reg_team.is_full = True
#                             reg_team.save()
#                             return Response(
#                                 {
#                                     "Success": f"{account.user.first_name} added to team with code {team_code}"
#                                 },
#                                 status=status.HTTP_201_CREATED,
#                             )
#                         else:
#                             return Response(
#                                 {"Error": "The Team is full!"},
#                                 status=status.HTTP_406_NOT_ACCEPTABLE,
#                             )
#                     except TeamStatus.DoesNotExist:
#                         print("\n")
#                         print("No such team found")
#                         print(team_code)
#                         print("\n")
#                         return Response(
#                             {"Error": "Invalid Team Code"},
#                             status=status.HTTP_400_BAD_REQUEST,
#                         )
#                 else:
#                     while(True):
#                         team_code = (
#                             event.short_name + "#" + f"{random.randint(0, 100000)}".zfill(5)
#                         )
#                         if not TeamStatus.objects.filter(team_code=team_code).exists():
#                             break
                    
#                     team = TeamStatus.objects.create(event=event, team_code=team_code)
#                     if event.team_size == 1:
#                         team.is_full = True
#                     team.save()

#                     team_member = TeamMember.objects.create(
#                         account=account, event=event, team=team
#                     )
#                     team_member.save()
#                     return Response(
#                         {"team_code": team_code},
#                         status=status.HTTP_201_CREATED,
#                     )

#             else:
#                 print("Invalid token, user and token's user don't match")
#                 return Response(
#                     {"error": "Invalid Token"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#     def destroy(self, request, *args, **kwargs):

#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
#             )

#         try:
#             team_member = TeamMember.objects.get(id=kwargs.get("pk"))

#             # Verify token with the team member token
#             if request.user == team_member.account.user:
#                 team = team_member.team
#                 team.current_size -= 1
#                 if team.current_size == 0:
#                     team.delete()
#                 else:
#                     team.is_full = False
#                     team.save()
#                     team_member.delete()
#                 return Response(
#                     {"Success": "Registration removed from " + team.event.title},
#                     status=status.HTTP_204_NO_CONTENT,
#                 )

#             else:
#                 print("Invalid token, user and token's user don't match")
#                 return Response(
#                     {"error": "Invalid Token"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except TeamMember.DoesNotExist:
#             print("User not registered to the event")
#             return Response(
#                 {"error": "Given user is not registered to the event"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# class CsvGenerate(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [MultipleTokenAuthentication, TokenAuthentication]
    
#     def get(self, request, *args, **kwargs):

#         if(request.user.is_superuser):
#             pk = kwargs.get("pk")
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="btq.csv"'
#             writer = csv.writer(response)

#             try:
#                 event = Event.objects.get(pk=pk)
#                 teams = TeamStatus.objects.filter(event=event, is_full=True)
#                 writer.writerow(["Email Id", "First Name", "Last Name", "Mobile Number", "Institute", "Team Code", "Event"])
#                 for team in teams:
#                     teammembers = TeamMember.objects.filter(team=team)
#                     for teammember in teammembers:
#                         writer.writerow(
#                             [teammember.account.user.email, teammember.account.user.first_name, teammember.account.user.last_name,
#                             teammember.account.mobile_number, teammember.account.institute, team.team_code, event.title])
#                 return response
#             except Event.DoesNotExist:
#                 return Response(
#                     {"Error": "No such event"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             return Response(
#                 {"Error": "Access denied"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )


# class TeamData(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [BasicAuthentication]
  
#     def get(self, request, *args, **kwargs):

#         try:
#             short_name = request.user.username
#             event = Event.objects.get(short_name=short_name)
#             teams = TeamStatus.objects.filter(event=event)
#             data = []
            
#             for team in teams:
#                 teammembers = TeamMember.objects.filter(team=team)
#                 for teammember in teammembers:
#                     teammember_dict = {
#                         "Email Id": teammember.account.user.email,
#                         "First Name": teammember.account.user.first_name,
#                         "Last Name": teammember.account.user.last_name,
#                         "Mobile Number": teammember.account.mobile_number,
#                         "Institute": teammember.account.institute,
#                         "Team Code": team.team_code,    
#                     }
#                     data.append(teammember_dict)
            
#             if len(data) == 0:
#                 df = pd.DataFrame(
#                     data, 
#                     columns=(["Email Id", "First Name", "Last Name", "Mobile Number", "Institute", "Team Code"]
#                 ))
#             else:
#                 df = pd.DataFrame(data)
            
#             response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#             response["Content-Disposition"] = "attachment; filename=participants.xlsx"
#             df.to_excel(response)    
#             return response
        
#         except Event.DoesNotExist:
#             return Response(
#                 {"Error": f"Access denied for {request.user.username}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

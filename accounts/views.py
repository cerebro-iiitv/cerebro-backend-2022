import pandas as pd

from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from registration.models import (IndividualParticipation, TeamMember,
                                 TeamParticipation)
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.authentication import MultipleTokenAuthentication
from accounts.models import Account, AuthToken
from accounts.serializers import (AccountDashboardSerializer,
                                  AccountSerializer, ChangePasswordSerializer,
                                  IndividualParticipationSerializer,
                                  LoginSerializer,
                                  ResetPasswordRequestSerializer,
                                  SetNewPasswordSerializer,
                                  TeamParticipationSerializer)
from accounts.utils import Util


class CustomRedirect(HttpResponsePermanentRedirect):
    
    allowed_schemes = ['http', 'https']


def index(request):
    return render(request, "accounts/base.html")
    
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        user_data = serializer.validated_data
        proof = user_data.get("proof", None)
        email = user_data.get("email", None)

        if proof:
            if proof.email != email:
                return Response({"error": "Invalid Pdf"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid Pdf"}, status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.create_user(**user_data)

        useremail = Account.objects.get(email=user_data['email'])
        token = AuthToken.objects.create(user=user)
        
        # Fetching the url of domain accessing the api
        request_host = request.headers.get("Origin", request.get_host())
        relativeLink = reverse('email-verify') 
        absurl = request_host + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user_data['first_name'] + ',\n'\
            'Click the link below to verify your email \n' + absurl + " for Cerebro2022."
        data = {'email_body': email_body, 'to_email': useremail.email,
                'email_subject': 'no-reply: Verify your Cerebro2022 account'}

        Util.send_email(data)
        return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class VerifyEmail(APIView):

    def get(self, request):
        token = request.GET.get('token')
        try:
            user = AuthToken.objects.get(key=token)
            account = Account.objects.get(id=user.user_id)
            if not account.is_verified:
                account.is_verified = True
                account.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]

class DashboardView(APIView):
    serializer_class = AccountDashboardSerializer
    queryset = Account.objects.all()
    http_method_names = ["get"]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]

    def get(self, request, *args, **kwargs):

        account = request.user
        
        data = dict()

        data["personal_details"] = AccountDashboardSerializer(account).data
    
        individual_participations = IndividualParticipation.objects.filter(account=account)

        individual_participations_data = IndividualParticipationSerializer(individual_participations, many = True).data

        teams = TeamMember.objects.filter(account=account).values_list("team", flat = True)

        teams = TeamParticipation.objects.filter(id__in = teams)

        teams_data = TeamParticipationSerializer(teams, many=True).data

        data["registered_events"] = [*individual_participations_data, *teams_data]

        return Response(
            data,
            status = status.HTTP_200_OK
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = Account.objects.get(email = email)
            if not user.is_verified:
                return Response({"status": "User not verified"}, status=status.HTTP_403_FORBIDDEN)
        except Account.DoesNotExist:
            return Response({"status": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"status": "Email id or password incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        token = AuthToken.objects.create(user=user)

        return Response(
                {
                    "status": "User logged in successfully", 
                    "Token": str(token)
                },
                status=status.HTTP_200_OK
            )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if request.META.get("HTTP_AUTHORIZATION") is not None:
            _, token = request.META.get("HTTP_AUTHORIZATION").split(" ")
            AuthToken.objects.get(key=token).delete()
            return Response({"Success": "Logout"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Token not found!"}, status=status.status.HTTP_404_NOT_FOUND)
               
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        uidb64 = serializer.validated_data.get("uidb64")
        token = serializer.validated_data.get("token")
        password1 = serializer.validated_data.get("password1")
        password2 = serializer.validated_data.get("password2")
        
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
        except DjangoUnicodeDecodeError:
            return Response({"error": "Password reset link is not valid, please request a new link"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = Account.objects.get(id = id)
        except Account.DoesNotExist:
            return Response({"error": "Password reset link is not valid, please request a new link"}, status=status.HTTP_401_UNAUTHORIZED)

        if not PasswordResetTokenGenerator().check_token(user, token):    
            return Response({"error": "Password reset link is not valid, please request a new link"}, status=status.HTTP_401_UNAUTHORIZED)

        if password1 != password2:
            return Response({"error": "Password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password1)
        user.save()

        return Response({"success": True, "message": "Password reset success"}, status=status.HTTP_200_OK)

class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data.get("email")

        try:
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            
            request_host = request.headers.get("Origin", request.get_host())
            relativeLink = reverse(
                'password-reset-complete')
              
            absurl = 'http://' + request_host + relativeLink + uidb64 + "/" + token + "/"
            email_body = 'Hi,' + '\nThere was a request to change your password!'+ \
            '\nIf you did not make this request then please ignore this email.' + \
            '\nOtherwise, use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'no-reply: Password reset link for Cerebro2022 account'}
            Util.send_email(data)
            
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"status": "User with given email id does not exist"}, status=status.HTTP_200_OK)
        
class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = Account
    authentication_classes = [MultipleTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            new_password1 = serializer.validated_data.get("new_password1")
            new_password2 = serializer.validated_data.get("new_password2")
            
            if new_password1 != new_password2:
                return Response({"error": "Password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password1"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountCsvView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser):
            return Response(
                {
                    "error": "Access denied"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            accounts = Account.objects.all().order_by("institute_name")
            data = AccountSerializer(accounts, many=True).data
            if len(data) == 0:
                df = pd.DataFrame(
                    data,
                    columns = ([
                        "First Name",
                        "Last Name",
                        "Email",
                        "Mobile Number",
                        "Institute",
                        "Address",
                        "Degree"
                    ])
                )
            else:
                df = pd.DataFrame(data)
                response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = "attachment; filename=participants.xlsx"
                df.to_excel(response)    
                return response
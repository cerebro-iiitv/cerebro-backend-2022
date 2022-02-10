import requests

from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import permissions, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.authentication import MultipleTokenAuthentication
from accounts.models import Account, AuthToken
from accounts.serializers import AccountDashboardSerializer, AccountSerializer, LoginSerializer,EmailVerificationSerializer, SetNewPasswordSerializer, ResetPasswordRequestSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
import os


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
        user = Account.objects.create_user(**serializer.validated_data)
        user_data = serializer.data
        useremail = Account.objects.get(email=user_data['email'])
        token = AuthToken.objects.create(user=user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi ' + user_data['first_name'] + ',\n'\
            'Click the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': useremail.email,
                'email_subject': 'Verify your email'}
        

        Util.send_email(data)
        return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

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


class DashboardViewSet(ModelViewSet):
    serializer_class = AccountDashboardSerializer
    queryset = Account.objects.all()
    http_method_names = ["get", "put", "patch", "post", "head"]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]

    def list(self, request):
        raise MethodNotAllowed("GET", detail="Method 'GET' not allowed without lookup")

    def retrieve(self, request, *args, **kwargs):
        account = Account.objects.get(pk=kwargs.get("pk"))
        if request.user == account.user:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(
                {"Error": "Permission Denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

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

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return CustomRedirect(redirect_url+'?&uidb64='+uidb64+'&token='+token)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        
            
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data.get("eamil")
        print(request.headers)

        return Response(
            {
                "Headers": request.headers,
                "Origin": request.headers['Origin']
            }
        )
        # try:
        #     # user = User.objects.get(email=email)
        #     # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        #     # token = AuthToken.objects.get_or_create(user=user).key

        #     # password
        #     pass
        # except:
        #     pass



        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hi,' + '\nThere was a request to change your password!'+ '\nIf you did not make this request then please ignore this email.' '\nOtherwise, use link below to reset your password  \n' + \
            absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    

class GoogleLogin(APIView):
    def post(self, request):
        payload = {"access_token": request.data.get("Token")}
        r = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
        )
        data = json.loads(r.text)

        if "error" in data:
            return Response(
                {"error": "Invalid Google Token or this Token has already expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=data["email"])
            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                account = Account.objects.create(
                    user=user,
                    profile_pic=data["picture"],
                )

        except User.DoesNotExist:
            data_dict = {
                "username": data["email"],
                "first_name": "",
                "last_name": "",
                "email": data["email"]
            }
            
            if "given_name" in data.keys():
                data_dict["first_name"] = data["given_name"]
            
            if "family_name" in data.keys():
                data_dict["last_name"] = data["family_name"]
            
            user = User.objects.create(**data_dict)
            account = Account.objects.create(
                user=user,
                profile_pic=data["picture"],
            )

        token = AuthToken.objects.create(user=user)
        response = {}
        response["email"] = user.email
        response["user_id"] = account.id
        response["access_token"] = str(token)
        return Response(response, status=status.HTTP_200_OK)



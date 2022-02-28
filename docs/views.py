from tkinter import E
from urllib import response
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accounts import serializers
from docs.models import PDF, ProofPDF
from docs.serializers import FileUploadSerializer, ProofFileUploadSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.models import Account
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

class FileUploadViewSet(ModelViewSet):
    
    queryset = ProofPDF.objects.all()
    serializer_class = ProofFileUploadSerializer
    # parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)

    #     if not serializer.is_valid():
    #         return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    #     email = serializer.validated_data.get("email")

    #     try:
    #         prev_pdf = ProofPDF.objects.get(email=email)
    #         try:
    #             Account.objects.get(email = email)
    #             return Response(
    #                 {"error": f"Proof pdf already uploaded for {email}"}, 
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         except Account.DoesNotExist:
    #             prev_pdf.delete()
    #     except ProofPDF.DoesNotExist:
    #         pass    

    #     return super().create(request, *args, **kwargs)
    
    # def get_permissions(self):
    #     try:
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError: 
    #         return [permission() for permission in self.permission_classes]

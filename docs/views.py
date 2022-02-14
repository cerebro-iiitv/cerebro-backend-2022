from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accounts import serializers
from docs.models import PDF
from docs.serializers import FileUploadSerializer, ProofFileUploadSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.models import Account
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
class FileUploadViewSet(ModelViewSet):
    
    queryset = PDF.objects.all()
    serializer_class = ProofFileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [IsAuthenticated]}
    
    def list(self, request, *args, **kwargs):
        return super(FileUploadViewSet, self).list(request, *args, **kwargs)
    
    def perform_create(self,serializer):
        email = self.request.data.get('email')
        pdf = self.request.data.get('pdf')

        obj = serializer.save(email=email,
                       pdf=pdf)
        pdf_link = obj.pdf

        account = Account.objects.get(email=email)
        account.proof = pdf_link
        account.save()
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            return [permission() for permission in self.permission_classes]

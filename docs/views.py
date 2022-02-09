from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from docs.models import PDF
from docs.serializers import FileUploadSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.models import Account
# Create your views here.
class FileUploadViewSet(ModelViewSet):
    
    queryset = PDF.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self,serializer):
        email = self.request.data.get('email')
        pdf = self.request.data.get('pdf')

        obj = serializer.save(email=email,
                       pdf=pdf)
        pdf_link = obj.pdf

        account = Account.objects.get(email=email)
        account.proof = pdf_link
        account.save()
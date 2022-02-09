from rest_framework import serializers
from docs.models import PDF

class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PDF
        fields = ['email','pdf']
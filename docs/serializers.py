from rest_framework import serializers

from docs.models import PDF, ProofPDF


class ProofFileUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProofPDF
        fields = ['email','pdf', 'id']
        
        extra_kwargs = {
            'pdf': {'write_only': True},
        }

class FileUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PDF
        fields = ['title','pdf', 'id']

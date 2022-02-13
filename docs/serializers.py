from rest_framework import serializers
from docs.models import PDF, ProofPDF

class ProofFileUploadSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ProofPDF
        fields = ['email','pdf']
        
    """used pop pdf link from response"""
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('pdf')
        return result

class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PDF
        fields = ['title','pdf']
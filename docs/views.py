from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from docs.models import ProofPDF
from docs.serializers import ProofFileUploadSerializer


class FileUploadViewSet(ModelViewSet):
    
    queryset = ProofPDF.objects.all()
    serializer_class = ProofFileUploadSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

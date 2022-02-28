from api.storage_backends import PrivateMediaStorage
from django.db import models


class ProofPDF(models.Model):
    email = models.CharField(max_length=255)
    pdf = models.FileField(storage=PrivateMediaStorage(), blank=True)

    def __str__(self):
        return self.email

class PDF(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to="docs", blank=True)

    def __str__(self):
        return self.title

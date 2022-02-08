from django.db import models


class PDF(models.Model):
    email = models.CharField(max_length=255)
    pdf = models.FileField(upload_to="docs")

    def __str__(self):
        return self.email

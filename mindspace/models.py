from django.db import models
from django.urls import reverse

# Create your models here.
class Mindspace(models.Model):
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=220)

    def get_absolute_url(self):
        return reverse("mindspace:mindspace_detail", kwargs={"id": self.id})
    
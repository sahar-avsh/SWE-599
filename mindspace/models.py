from django.db import models

# Create your models here.
class Mindspace(models.Model):
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=220)
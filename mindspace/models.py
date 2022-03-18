from django.db import models
from django.urls import reverse

# Create your models here.
class Mindspace(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.id})

class Resource(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.belongs_to.id})
    
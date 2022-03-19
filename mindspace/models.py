from django.db import models
from django.urls import reverse
from profiles.models import Profile

# Create your models here.
class Mindspace(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mindspaces', null=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mindspace:resource_detail', kwargs={'ms_id': self.belongs_to.id, 'id': self.id})

    def __str__(self):
        return self.belongs_to.title + ' - ' + self.title
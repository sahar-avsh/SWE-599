from django.db import models
from django.urls import reverse
from profiles.models import Profile

from datetime import datetime, timedelta, timezone

# Create your models here.
class Mindspace(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mindspaces', null=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_at <= timedelta(seconds=60)

class Resource(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('mindspace:resource_detail', kwargs={'ms_id': self.belongs_to.id, 'id': self.id})

    def __str__(self):
        return self.belongs_to.title + ' - ' + self.title

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_at <= timedelta(seconds=60)
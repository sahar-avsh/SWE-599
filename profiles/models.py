from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  f_name = models.CharField(max_length=80)
  l_name = models.CharField(max_length=80)
  created_at = models.DateTimeField(auto_now_add=True)

  def get_absolute_url(self):
    return reverse('profiles:profile_detail', kwargs={'id': self.id})

  def __str__(self):
      return self.f_name + ' ' + self.l_name
  
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from datetime import datetime, timedelta, timezone

# Create your models here.
class Profile(models.Model):
  created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  f_name = models.CharField(max_length=80)
  l_name = models.CharField(max_length=80)
  company = models.CharField(blank=True, max_length=100, null=True)
  bio = models.TextField(blank=True, null=True)
  image = models.ImageField(blank=True, upload_to='profiles/', null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def been_member(self):
    now = datetime.now(timezone.utc)
    return (now - self.created_at).days

  def get_absolute_url(self):
    return reverse('profiles:profile_detail', kwargs={'id': self.id})

  def __str__(self):
    return self.f_name + ' ' + self.l_name

  def save(self, *args, **kwargs):
    from io import StringIO, BytesIO
    from PIL import Image

    image_field = self.image
    # image_field = self.cleaned_data.get('image')
    image_file = BytesIO(image_field.read())
    image = Image.open(image_file)
    # w, h = image.size

    image = image.resize((200, 200), Image.ANTIALIAS)

    image_file = BytesIO()
    image.save(image_file, 'JPEG', quality=90)

    image_field.file = image_file
    super().save(*args, **kwargs)

  
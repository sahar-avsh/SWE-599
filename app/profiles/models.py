from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from datetime import datetime, timedelta, timezone

# Create your models here.
class Profile(models.Model):
  created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  f_name = models.CharField(max_length=80)
  l_name = models.CharField(max_length=80)
  company = models.CharField(blank=True, max_length=100, null=True)
  bio = models.TextField(blank=True, null=True)
  image = models.ImageField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def been_member(self):
    now = datetime.now(timezone.utc)
    return (now - self.created_at).days

  @property
  def unseen_notifs(self):
    qs = Notification.objects.filter(received_by=self).filter(read_date__isnull=True)
    return len(qs)

  def get_absolute_url(self):
    return reverse('profiles:profile_detail', kwargs={'id': self.id})

  def __str__(self):
    return self.f_name + ' ' + self.l_name

  def save(self, *args, **kwargs):
    if self.image:
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


class Notification(models.Model):
  ADD_EDITOR = 'AE'
  REMOVE_EDITOR = 'RE'
  ADD_VIEWER = 'AV'
  REMOVE_VIEWER = 'RV'
  ADD_COMMENTER = 'AC'
  REMOVE_COMMENTER = 'RC'
  POST_ANSWER = 'PA'
  UPDATE_ANSWER = 'UA'
  UP_VOTE = 'UV'
  DOWN_VOTE = 'DV'
  TAKE_VOTE = 'TV'
  NOTIFICATION_TYPES = (
    (ADD_EDITOR, 'add_editor'),
    (REMOVE_EDITOR, 'remove_editor'),
    (ADD_VIEWER, 'add_viewer'),
    (REMOVE_VIEWER, 'remove_viewer'),
    (ADD_COMMENTER, 'add_commenter'),
    (REMOVE_COMMENTER, 'remove_commenter'),
    (POST_ANSWER, 'post_answer'),
    (UPDATE_ANSWER, 'update_answer'),
    (UP_VOTE, 'upvote_answer'),
    (DOWN_VOTE, 'downvote_answer'),
    (TAKE_VOTE, 'take_vote')
  )

  sent_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_notifications')
  received_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient_notifications')
  notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
  subject_answer = models.ForeignKey("qna.Answer", on_delete=models.CASCADE, null=True)
  subject_mindspace = models.ForeignKey("mindspace.Mindspace", on_delete=models.CASCADE, null=True)
  read_date = models.DateTimeField(null=True)
  sent_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.sent_by.f_name + '->' + self.received_by.f_name

  
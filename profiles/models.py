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

# NOTIFICATION_TYPE_CHOICES = (
#     ('qna', 'qna'),
#     ('mindspace_share', 'mindspace_share'),
#     ('mindspace_edit', 'mindspace_edit'),
#     ('mindspace_comment', 'mindspace_comment')
# )

# class Notification(models.Model):
#   sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_notifications')
#   recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient_notifications')

#   notification_type = models.CharField(max_length=17, choices=NOTIFICATION_TYPE_CHOICES)
#   question = models.ForeignKey("qna.Question", on_delete=models.CASCADE, related_name='question_notification', null=True)
#   answer = models.ForeignKey("qna.Answer", on_delete=models.CASCADE, related_name='answer_notification', null=True)
#   mindspace = models.ForeignKey("mindspace.Mindspace", on_delete=models.CASCADE, related_name='mindspace_notification', null=True)
#   resource = models.ForeignKey("mindspace.Resource", on_delete=models.CASCADE, related_name='resource_notification', null=True)
#   note = models.ForeignKey("mindspace.Note", on_delete=models.CASCADE, related_name='note_notification', null=True)
#   #comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_notification', null=True)

#   read_date = models.DateTimeField(null=True)
#   sent_date = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#       return self.sender.f_name + '->' + self.recipient.f_name

  
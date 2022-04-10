from django.db import models
from mindspace.models import *
from django.urls import reverse

from profiles.models import Profile

from datetime import datetime, timedelta, timezone

# Create your models here.
class Question(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    body = models.TextField()
    tagged_mindspace = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='mindspace_questions', null=True)
    tagged_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource_questions', null=True)
    asked_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.f_name + '-' + self.title

    def get_absolute_url(self):
        return reverse('qna:question_detail', kwargs={'id': self.id})

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_date <= timedelta(seconds=60)

class Answer(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    reply = models.TextField()
    tagged_mindspace = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='mindspace_answers', null=True)
    tagged_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource_answers', null=True)
    replied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.f_name + '-' + self.question.title

    def get_absolute_url(self):
        return reverse('qna:question_detail', kwargs={'id': self.question.id})

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_date <= timedelta(seconds=60)
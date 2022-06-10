from django.db import models
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericRelation

from datetime import datetime, timedelta, timezone

# Create your models here.
class Question(models.Model):
    owner = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    body = models.TextField()
    tagged_mindspace = models.ForeignKey("mindspace.Mindspace", on_delete=models.SET_NULL, related_name='mindspace_questions', null=True)
    tagged_resource = models.ForeignKey("mindspace.Resource", on_delete=models.SET_NULL, related_name='resource_questions', null=True)
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
    owner = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='profile_answers')
    question = models.ForeignKey("qna.Question", on_delete=models.CASCADE, related_name='answers')
    reply = models.TextField()
    tagged_mindspace = models.ForeignKey("mindspace.Mindspace", on_delete=models.SET_NULL, related_name='mindspace_answers', null=True)
    tagged_resource = models.ForeignKey("mindspace.Resource", on_delete=models.SET_NULL, related_name='resource_answers', null=True)
    replied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # activity = GenericRelation("profiles.Notification", related_query_name='answer_activities')

    def __str__(self):
        return self.owner.f_name + '-' + self.question.title

    def get_absolute_url(self):
        return reverse('qna:question_detail', kwargs={'id': self.question.id})

    def get_vote_score(self):
        score = 0
        for vote in self.votes.all():
            if vote.activity_type == 'U':
                score += 1
            else:
                score -= 1
        return score

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_date <= timedelta(seconds=60)


class Activity(models.Model):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote')
    )

    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='activity')
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    activity_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')

    def __str__(self):
        return self.owner.f_name + '-' + self.activity_type + '-' + str(self.answer.id)
from django.db import models
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericRelation

from datetime import datetime, timedelta, timezone

# Create your models here.
class Mindspace(models.Model):
    owner = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='mindspaces', null=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    editors = models.ManyToManyField("profiles.Profile", related_name='can_edit')
    viewers = models.ManyToManyField("profiles.Profile", related_name='can_view')
    commenters = models.ManyToManyField("profiles.Profile", related_name='can_comment')

    # shares = GenericRelation("profiles.Notification", related_query_name='mindspace_shares')

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_at <= timedelta(seconds=60)

FORMAT_CHOICES = (
    ('Video', 'Video'),
    ('Image', 'Image'),
    ('Document', 'Document'),
    ('Quote', 'Quote'),
    ('Link', 'Link to external source')
)

class Resource(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    res_format = models.CharField(max_length=8, choices=FORMAT_CHOICES, default='Link')

    video = models.FileField(blank=True, null=True, upload_to='mindspace/resource_video')
    image = models.ImageField(blank=True, null=True, upload_to='mindspace/resource_image')
    document = models.FileField(blank=True, null=True, upload_to='mindspace/resource_document')
    quote = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, max_length=200)

    # edits = GenericRelation("profiles.Notification", related_query_name='resource_edits')

    def get_absolute_url(self):
        return reverse('mindspace:resource_detail', kwargs={'ms_id': self.belongs_to.id, 'id': self.id})

    def __str__(self):
        return self.belongs_to.title + ' - ' + self.title

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_at <= timedelta(seconds=60)

class Note(models.Model):
    title = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    content = models.TextField()
    belongs_to = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # edits = GenericRelation("profiles.Notification", related_query_name='note_edits')

    def get_absolute_url(self):
        return reverse('mindspace:note_detail', \
            kwargs={'ms_id': self.belongs_to.belongs_to.id, 'r_id': self.belongs_to.id, 'id': self.id})
    
    def __str__(self):
        return self.id + ' - ' + self.belongs_to.title

    @property
    def is_recent(self):
        now = datetime.now(timezone.utc)
        return now - self.updated_at <= timedelta(seconds=60)
    
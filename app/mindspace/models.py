from django.db import models
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericRelation

from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class Mindspace(models.Model):
    owner = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='mindspaces', null=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    # editors = models.ManyToManyField("profiles.Profile", related_name='can_edit')
    # viewers = models.ManyToManyField("profiles.Profile", related_name='can_view')
    # commenters = models.ManyToManyField("profiles.Profile", related_name='can_comment')

    # shares = GenericRelation("profiles.Notification", related_query_name='mindspace_shares')

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title

    @property
    def is_recent(self):
        # now = datetime.now(timezone.utc)
        now = timezone.now()
        return now - self.updated_at <= timedelta(seconds=60)

FORMAT_CHOICES = (
    ('Video', 'Video'),
    ('Image', 'Image'),
    ('Document', 'Document'),
    ('Quote', 'Quote'),
    ('Link', 'Link to external source')
)

class Resource(models.Model):
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='resources_created', null=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    res_format = models.CharField(max_length=8, choices=FORMAT_CHOICES, default='Link')

    video = models.FileField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    document = models.FileField(blank=True, null=True)
    quote = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, max_length=200)

    # edits = GenericRelation("profiles.Notification", related_query_name='resource_edits')

    def get_absolute_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.belongs_to.id})

    def __str__(self):
        return self.belongs_to.title + ' - ' + self.title

    @property
    def is_recent(self):
        # now = datetime.now(timezone.utc)
        now = timezone.now()
        return now - self.updated_at <= timedelta(seconds=60)

class Note(models.Model):
    # title = models.CharField(max_length=220, blank=True)
    # description = models.TextField(blank=True)
    content = models.TextField()
    written_by = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE, related_name='written_notes')
    belongs_to = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # edits = GenericRelation("profiles.Notification", related_query_name='note_edits')

    # def get_absolute_url(self):
    #     return reverse('mindspace:note_detail', \
    #         kwargs={'ms_id': self.belongs_to.belongs_to.id, 'r_id': self.belongs_to.id, 'id': self.id})

    def save(self, *args, **kwargs):
        """Override resource's updated_at attribute"""
        Resource.objects.filter(id=self.belongs_to.id).update(updated_at=timezone.now())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.belongs_to.title

    @property
    def is_recent(self):
        # now = datetime.now(timezone.utc)
        now = timezone.now()
        return now - self.updated_at <= timedelta(seconds=60)


class ShareMindspace(models.Model):
    mindspace = models.ForeignKey(Mindspace, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='shared_by')
    shared_with = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='shared_with')
    shared_with_info = models.CharField(max_length=100)

    viewer = 'viewer'
    editor = 'editor'
    # commenter = 'commenter'

    ACCESS_LEVELS = (
        (viewer,'VIEW'),
        (editor, 'EDIT'),
        # (commenter, 'COMMENT')
    )

    access_level = models.CharField(max_length=9, choices=ACCESS_LEVELS)
    shared_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('mindspace', 'shared_with')

    def __str__(self):
        return self.shared_by.f_name + ':' + self.mindspace.title + ':' + self.shared_with.f_name + ':' + self.access_level
    
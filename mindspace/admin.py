from django.contrib import admin
from .models import (
  Mindspace,
  Resource,
  Note,
  ShareMindspace
)

# Register your models here.
admin.site.register([Mindspace, Resource, Note, ShareMindspace])
from django.contrib import admin
from .models import (
  Mindspace,
  Resource
)

# Register your models here.
admin.site.register([Mindspace, Resource])
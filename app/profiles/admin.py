from django.contrib import admin

from profiles.models import Profile, Notification

# Register your models here.
admin.site.register([Profile, Notification])
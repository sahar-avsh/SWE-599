from django.contrib import admin

from .models import Question, Answer, Activity

# Register your models here.
admin.site.register([Question, Answer, Activity])
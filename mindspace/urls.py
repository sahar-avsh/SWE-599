from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.simpleView, name='home_page')
]

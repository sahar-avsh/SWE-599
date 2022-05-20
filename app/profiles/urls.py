from django.urls import path

from .views import (
  ProfileDetailView,
  ProfileUpdateView,
  NotificationListView,
)

app_name = 'profiles'
urlpatterns = [
    path('<int:id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<int:id>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:id>/notifications/', NotificationListView.as_view(), name='profile_notifications'),
]

from django.urls import path

from .views import (
  ProfileDetailView,
  ProfileUpdateView,
  NotificationListView,
  GetNumOfUnseenNotifsAjax,
)

app_name = 'profiles'
urlpatterns = [
    path('<int:id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<int:id>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:id>/notifications/', NotificationListView.as_view(), name='profile_notifications'),
    path('ajax/unseen-notifs/', GetNumOfUnseenNotifsAjax.as_view(), name='unseen_notifs'),
]

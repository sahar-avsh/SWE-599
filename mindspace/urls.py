from django.urls import path
from .views import (
    MindspaceListView,
    MindspaceDetailView,
    MindspaceCreateView,
    MindspaceUpdateView,
    MindspaceDeleteView,
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView
)

app_name = 'mindspace'
urlpatterns = [
    path('', MindspaceListView.as_view(), name='mindspace_list'),
    path('<int:id>/', MindspaceDetailView.as_view(), name='mindspace_detail'),
    path('create/', MindspaceCreateView.as_view(), name='mindspace_create'),
    path('<int:id>/update/', MindspaceUpdateView.as_view(), name='mindspace_update'),
    path('<int:id>/delete/', MindspaceDeleteView.as_view(), name='mindspace_delete'),
    path('<int:ms_id>/create-resource/', ResourceCreateView.as_view(), name='resource_create'),
]

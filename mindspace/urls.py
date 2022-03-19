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
    path('dashboard/', MindspaceListView.as_view(), name='mindspace_list'),
    path('<int:id>/', MindspaceDetailView.as_view(), name='mindspace_detail'),
    path('create/', MindspaceCreateView.as_view(), name='mindspace_create'),
    path('<int:id>/update/', MindspaceUpdateView.as_view(), name='mindspace_update'),
    path('<int:id>/delete/', MindspaceDeleteView.as_view(), name='mindspace_delete'),
    path('<int:ms_id>/create-resource/', ResourceCreateView.as_view(), name='resource_create'),
    path('<int:ms_id>/<int:id>/update-resource/', ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:ms_id>/<int:id>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('<int:ms_id>/resources/', ResourceListView.as_view(), name='resource_list'),
    path('<int:ms_id>/<int:id>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),
]

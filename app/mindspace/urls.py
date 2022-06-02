from django.urls import path
from .views import (
    MindspaceListView,
    MindspaceDetailView,
    MindspaceCreateView,
    MindspaceUpdateView,
    MindspaceDeleteView,
    ShareMindspaceCreateView,
    AjaxMindspaceSearch,
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceUpdateView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    NoteListView,
)

app_name = 'mindspace'
urlpatterns = [
    path('dashboard/', MindspaceListView.as_view(), name='mindspace_list'),
    path('detail/<int:id>/', MindspaceDetailView.as_view(), name='mindspace_detail'),
    path('create/', MindspaceCreateView.as_view(), name='mindspace_create'),
    path('<int:id>/update/', MindspaceUpdateView.as_view(), name='mindspace_update'),
    path('<int:id>/delete/', MindspaceDeleteView.as_view(), name='mindspace_delete'),
    path('<int:id>/share/', ShareMindspaceCreateView.as_view(), name='mindspace_share'),
    path('ajax/load-search-results/', AjaxMindspaceSearch.as_view(), name='ajax_load_search_results'),
    path('<int:ms_id>/create-resource/', ResourceCreateView.as_view(), name='resource_create'),
    path('<int:ms_id>/<int:id>/update-resource/', ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:ms_id>/resource-detail/<int:id>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('<int:ms_id>/<int:id>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),
    path('<int:ms_id>/<int:r_id>/create-note/', NoteCreateView.as_view(), name='note_create'),
    path('<int:ms_id>/<int:r_id>/<int:id>/update-resource/', NoteUpdateView.as_view(), name='note_update'),
    path('<int:ms_id>/<int:r_id>/notes/', NoteListView.as_view(), name='note_list'),
    path('<int:ms_id>/<int:r_id>/<int:id>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]

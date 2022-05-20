from django.urls import path
from .views import (
    MindspaceListView,
    MindspaceDetailView,
    MindspaceCreateView,
    MindspaceUpdateView,
    MindspaceDeleteView,
    ShareMindspaceCreateView,
    MindspaceSearchListView,
    AjaxMindspaceSearch,
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    NotesAjaxView,
)

app_name = 'mindspace'
urlpatterns = [
    path('dashboard/', MindspaceListView.as_view(), name='mindspace_list'),
    path('<int:id>/', MindspaceDetailView.as_view(), name='mindspace_detail'),
    path('create/', MindspaceCreateView.as_view(), name='mindspace_create'),
    path('<int:id>/update/', MindspaceUpdateView.as_view(), name='mindspace_update'),
    path('<int:id>/delete/', MindspaceDeleteView.as_view(), name='mindspace_delete'),
    path('<int:id>/share/', ShareMindspaceCreateView.as_view(), name='mindspace_share'),
    path('timeline/', MindspaceSearchListView.as_view(), name='mindspace_search'),
    path('ajax/load-search-results/', AjaxMindspaceSearch.as_view(), name='ajax_load_search_results'),
    path('<int:ms_id>/create-resource/', ResourceCreateView.as_view(), name='resource_create'),
    path('<int:ms_id>/<int:id>/update-resource/', ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:ms_id>/<int:id>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('<int:ms_id>/resources/', ResourceListView.as_view(), name='resource_list'),
    path('<int:ms_id>/<int:id>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),
    path('<int:ms_id>/<int:r_id>/create-note/', NoteCreateView.as_view(), name='note_create'),
    path('<int:ms_id>/<int:r_id>/<int:id>/update-resource/', NoteUpdateView.as_view(), name='note_update'),
    # path('<int:ms_id>/<int:r_id>/<int:id>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:ms_id>/<int:r_id>/notes/', NotesAjaxView.as_view(), name='note_list'),
    path('<int:ms_id>/<int:r_id>/<int:id>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]

from django.urls import path
from .views import (
    QuestionCreateView,
    QuestionDetailView, 
    QuestionListView,
    QuestionUpdateView, 
    QuestionDeleteView,
    QuestionSearchView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
    LoadResources,
    VoteView,
)

app_name = 'qna'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<int:id>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreateView.as_view(), name='question_create'),
    path('<int:id>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('<int:id>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('ajax/question-search/', QuestionSearchView.as_view(), name='question_search'),
    path('<int:q_id>/answer/', AnswerCreateView.as_view(), name='answer_create'),
    path('<int:q_id>/<int:id>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:q_id>/<int:id>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
    path('ajax/load-resources/', LoadResources.as_view(), name='ajax_load_resources'),
    path('ajax/vote-answer/', VoteView.as_view(), name='answer_vote'),
]
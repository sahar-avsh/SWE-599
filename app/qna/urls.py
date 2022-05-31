from django.urls import path
from .views import (
    QuestionCreateView,
    QuestionDetailView, 
    OwnQuestionsListView,
    OwnAnswersListView,
    CommunityQuestionsListView,
    QuestionUpdateView, 
    QuestionDeleteView,
    QuestionSearchView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerListView,
    AnswerDeleteView,
    AnswerDetailView,
    LoadResources,
    VoteView,
    # MyAnswerListView,
    # AnswersAjaxView,
    # AnswerFormAjax
)

app_name = 'qna'
urlpatterns = [
    path('', CommunityQuestionsListView.as_view(), name='question_list'),
    path('own-questions/ajax/', OwnQuestionsListView.as_view(), name='own_questions_list'),
    path('own-answers/ajax/', OwnAnswersListView.as_view(), name='own_answers_list'),
    path('<int:id>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreateView.as_view(), name='question_create'),
    path('<int:id>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('<int:id>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('ajax/question-search/', QuestionSearchView.as_view(), name='question_search'),
    path('<int:q_id>/answer/', AnswerCreateView.as_view(), name='answer_create'),
    path('<int:q_id>/<int:id>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:q_id>/<int:id>/detail/', AnswerDetailView.as_view(), name='answer_detail'),
    path('<int:q_id>/<int:id>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
    path('ajax/load-answers/', AnswerListView.as_view(), name='answer_list'),
    path('ajax/load-resources/', LoadResources.as_view(), name='ajax_load_resources'),
    path('ajax/vote-answer/', VoteView.as_view(), name='answer_vote'),
]
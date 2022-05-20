from django.urls import path
from .views import (
    QuestionCreateView,
    QuestionDetailView, 
    QuestionListView, 
    QuestionUpdateView, 
    QuestionDeleteView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
    AnswersAjaxView,
    AnswerFormAjax
)

app_name = 'qna'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<int:id>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreateView.as_view(), name='question_create'),
    path('<int:id>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('<int:id>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('<int:q_id>/answer/', AnswerCreateView.as_view(), name='answer_create'),
    path('<int:q_id>/<int:id>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:q_id>/<int:id>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
    path('<int:q_id>/ajax/load-answers/', AnswersAjaxView.as_view(), name='answer_list'),
    path('ajax/answer-form/', AnswerFormAjax.as_view(), name='ajax_render_answer_form'),
]
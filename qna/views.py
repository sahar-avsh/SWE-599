from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.exceptions import PermissionDenied

from django.db.models import Q

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView
)

from .models import *
from .forms import *

# Create your views here.
class QuestionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'qna/question_create.html'
    model = Question
    form_class = QuestionModelForm
    success_message = 'Your question was created successfully'

    def form_valid(self, form):
        # assign owner to the question
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs 

class LoadResources(LoginRequiredMixin, TemplateView):
    template_name = 'qna/resource_dropdown_list_options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mindspace_id = self.request.GET.get('mindspace')
        try:
            resources = Resource.objects.filter(belongs_to_id=mindspace_id).order_by('title')
            context['resources'] = resources
        except (ValueError, TypeError):
            pass
        return context

class QuestionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'qna/question_update.html'
    form_class = QuestionModelForm
    success_message = 'Your question was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Question, id=id_)

    def form_valid(self, form):
        # assign owner to the question
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        object = Question.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class QuestionListView(LoginRequiredMixin, ListView):
    template_name = 'qna/question_list.html'

    def get_queryset(self):
        queryset = Question.objects.filter(owner=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_questions = Question.objects.filter(~Q(owner=self.request.user.profile)).order_by('asked_date')
        context['object_list_questions'] = other_questions
        return context

class QuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'qna/question_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Question, id=id_)

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'qna/question_delete.html'
    success_message = 'Your question was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Question, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('qna:question_list')

    def dispatch(self, request, *args, **kwargs):
        object = Question.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

############################ Answer ############################
class AnswerCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'qna/answer_create.html'
    model = Answer
    form_class = AnswerModelForm
    success_message = 'Your answer was created successfully'

    def form_valid(self, form):
        question_id = self.kwargs.get('id')
        # assign owner to the answer
        form.instance.owner = self.request.user.profile
        # assign question to the answer
        form.instance.question = Question.objects.get(id=question_id)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs 

class AnswerUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'qna/answer_update.html'
    form_class = AnswerModelForm
    success_message = 'Your answer was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Answer, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        object = Answer.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# class AnswerListView(LoginRequiredMixin, ListView):
#     template_name = 'qna/question_list.html'

#     def get_queryset(self):
#         queryset = Question.objects.filter(owner=self.request.user.profile)
#         return queryset

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     view = self.request.user.profile.can_view.all()
#     #     comment = self.request.user.profile.can_comment.all()
#     #     edit = self.request.user.profile.can_edit.all()
#     #     context['object_list_view'] = view
#     #     context['object_list_comment'] = comment
#     #     context['object_list_edit'] = edit
#     #     return context

# class AnswerDetailView(LoginRequiredMixin, DetailView):
#     template_name = 'qna/question_detail.html'

#     def get_object(self):
#         id_ = self.kwargs.get('id')
#         return get_object_or_404(Question, id=id_)

class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'qna/answer_delete.html'
    success_message = 'Your answer was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Answer, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('qna:question_detail', kwargs={'id': Question.objects.get(id=self.kwargs.get('q_id'))})

    def dispatch(self, request, *args, **kwargs):
        object = Answer.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
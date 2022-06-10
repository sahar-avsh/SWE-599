from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, Http404

from django.core.exceptions import PermissionDenied

from django.db.models import Q

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, Page, InvalidPage

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,
    View
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
        question = form.save()
        return JsonResponse({'nextURL': question.get_absolute_url()}, status=200)

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        object = Question.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class QuestionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'qna/question_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_create'] = QuestionModelForm(self.request.user.profile)
        context['form_search'] = QuestionSearchForm()
        return context


class QuestionListView(LoginRequiredMixin, TemplateView):
    template_name = 'qna/question_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comm_questions = Question.objects.filter(~Q(owner=self.request.user.profile)).order_by('-asked_date')
        my_questions = Question.objects.filter(owner=self.request.user.profile).order_by('-asked_date')
        answers = Answer.objects.filter(owner=self.request.user.profile).prefetch_related('question').order_by('-replied_date')
        my_answers = []
        for answer in answers:
            if answer.question not in my_answers:
                my_answers.append(answer.question)

        if 'community-questions-page' in self.request.GET.keys():
            paginator = Paginator(comm_questions, self.paginate_by)
            page_kwarg = 'community-questions-page'
            context['is_viewing'] = 'community-questions'
        elif 'my-questions-page' in self.request.GET.keys():
            paginator = Paginator(my_questions, self.paginate_by)
            page_kwarg = 'my-questions-page'
            context['is_viewing'] = 'my-questions'
        elif 'my-answers-page' in self.request.GET.keys():
            paginator = Paginator(my_answers, self.paginate_by)
            page_kwarg = 'my-answers-page'
            context['is_viewing'] = 'my-answers'

        page = self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404()
        
        try:
            page = paginator.page(page_number)
            context['is_paginated'] = page.has_other_pages()
            context['page_obj'] = page
        except InvalidPage:
            raise Http404

        return context

class QuestionSearchView(LoginRequiredMixin, ListView):
    template_name = 'qna/question_search_results.html'
    paginate_by = 5
    page_kwarg = 'search-question-page'

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        search_words = [word for word in keyword.strip().split() if word != '']
        arguments = Q()
        for w in search_words:
            arguments |= Q(**{'title__icontains': w})
            arguments |= Q(**{'body__icontains': w})
        queryset = Question.objects.filter(*(arguments, )).order_by('asked_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_keyword'] = self.request.GET.get('keyword')
        return context
class QuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'qna/question_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Question, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_object().answers.all()
        context['answers'] = qs
        return context

class QuestionDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'qna/question_delete.html'
    success_message = 'Your question was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Question, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

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

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(id=self.kwargs.get('q_id'))
        return context

    def form_valid(self, form):
        question_id = self.kwargs.get('q_id')
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
    model = Answer
    success_message = 'Your answer was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Answer, id=id_)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile # pass the 'profile' in kwargs
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        object = Answer.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AnswerDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'qna/answer_delete.html'
    success_message = 'Your answer was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Answer, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        question = Question.objects.get(id=self.kwargs.get('q_id'))
        return reverse('qna:question_detail', kwargs={'id': question.id})

    def dispatch(self, request, *args, **kwargs):
        object = Answer.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

############################ Activity ############################
class VoteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        upvote_html = '<div id="id-newvoted"> \
                            <svg id="id-vote-U-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16"> \
                                <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/> \
                            </svg> \
                            <svg id="id-vote-D-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-down" viewBox="0 0 16 16"> \
                                <path d="M8.864 15.674c-.956.24-1.843-.484-1.908-1.42-.072-1.05-.23-2.015-.428-2.59-.125-.36-.479-1.012-1.04-1.638-.557-.624-1.282-1.179-2.131-1.41C2.685 8.432 2 7.85 2 7V3c0-.845.682-1.464 1.448-1.546 1.07-.113 1.564-.415 2.068-.723l.048-.029c.272-.166.578-.349.97-.484C6.931.08 7.395 0 8 0h3.5c.937 0 1.599.478 1.934 1.064.164.287.254.607.254.913 0 .152-.023.312-.077.464.201.262.38.577.488.9.11.33.172.762.004 1.15.069.13.12.268.159.403.077.27.113.567.113.856 0 .289-.036.586-.113.856-.035.12-.08.244-.138.363.394.571.418 1.2.234 1.733-.206.592-.682 1.1-1.2 1.272-.847.283-1.803.276-2.516.211a9.877 9.877 0 0 1-.443-.05 9.364 9.364 0 0 1-.062 4.51c-.138.508-.55.848-1.012.964l-.261.065zM11.5 1H8c-.51 0-.863.068-1.14.163-.281.097-.506.229-.776.393l-.04.025c-.555.338-1.198.73-2.49.868-.333.035-.554.29-.554.55V7c0 .255.226.543.62.65 1.095.3 1.977.997 2.614 1.709.635.71 1.064 1.475 1.238 1.977.243.7.407 1.768.482 2.85.025.362.36.595.667.518l.262-.065c.16-.04.258-.144.288-.255a8.34 8.34 0 0 0-.145-4.726.5.5 0 0 1 .595-.643h.003l.014.004.058.013a8.912 8.912 0 0 0 1.036.157c.663.06 1.457.054 2.11-.163.175-.059.45-.301.57-.651.107-.308.087-.67-.266-1.021L12.793 7l.353-.354c.043-.042.105-.14.154-.315.048-.167.075-.37.075-.581 0-.211-.027-.414-.075-.581-.05-.174-.111-.273-.154-.315l-.353-.354.353-.354c.047-.047.109-.176.005-.488a2.224 2.224 0 0 0-.505-.804l-.353-.354.353-.354c.006-.005.041-.05.041-.17a.866.866 0 0 0-.121-.415C12.4 1.272 12.063 1 11.5 1z"/> \
                            </svg> \
                        </div>'

        downvote_html = '<div id="id-newvoted"> \
                            <svg id="id-vote-U-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-up" viewBox="0 0 16 16"> \
                                <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/> \
                            </svg> \
                            <svg id="id-vote-D-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-down-fill" viewBox="0 0 16 16"> \
                                <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.378 1.378 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51.136.02.285.037.443.051.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.896 1.896 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2.094 2.094 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.162 3.162 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.823 4.823 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591z"/> \
                            </svg> \
                        </div>'

        novote_html = '<div id="id-newvoted"> \
                            <svg id="id-vote-U-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-up" viewBox="0 0 16 16"> \
                                <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/> \
                            </svg> \
                            <svg id="id-vote-D-' + request.POST.get('answer_id') + '" style="cursor: pointer;" action-url="/questions/ajax/vote-answer/" xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-hand-thumbs-down" viewBox="0 0 16 16"> \
                                <path d="M8.864 15.674c-.956.24-1.843-.484-1.908-1.42-.072-1.05-.23-2.015-.428-2.59-.125-.36-.479-1.012-1.04-1.638-.557-.624-1.282-1.179-2.131-1.41C2.685 8.432 2 7.85 2 7V3c0-.845.682-1.464 1.448-1.546 1.07-.113 1.564-.415 2.068-.723l.048-.029c.272-.166.578-.349.97-.484C6.931.08 7.395 0 8 0h3.5c.937 0 1.599.478 1.934 1.064.164.287.254.607.254.913 0 .152-.023.312-.077.464.201.262.38.577.488.9.11.33.172.762.004 1.15.069.13.12.268.159.403.077.27.113.567.113.856 0 .289-.036.586-.113.856-.035.12-.08.244-.138.363.394.571.418 1.2.234 1.733-.206.592-.682 1.1-1.2 1.272-.847.283-1.803.276-2.516.211a9.877 9.877 0 0 1-.443-.05 9.364 9.364 0 0 1-.062 4.51c-.138.508-.55.848-1.012.964l-.261.065zM11.5 1H8c-.51 0-.863.068-1.14.163-.281.097-.506.229-.776.393l-.04.025c-.555.338-1.198.73-2.49.868-.333.035-.554.29-.554.55V7c0 .255.226.543.62.65 1.095.3 1.977.997 2.614 1.709.635.71 1.064 1.475 1.238 1.977.243.7.407 1.768.482 2.85.025.362.36.595.667.518l.262-.065c.16-.04.258-.144.288-.255a8.34 8.34 0 0 0-.145-4.726.5.5 0 0 1 .595-.643h.003l.014.004.058.013a8.912 8.912 0 0 0 1.036.157c.663.06 1.457.054 2.11-.163.175-.059.45-.301.57-.651.107-.308.087-.67-.266-1.021L12.793 7l.353-.354c.043-.042.105-.14.154-.315.048-.167.075-.37.075-.581 0-.211-.027-.414-.075-.581-.05-.174-.111-.273-.154-.315l-.353-.354.353-.354c.047-.047.109-.176.005-.488a2.224 2.224 0 0 0-.505-.804l-.353-.354.353-.354c.006-.005.041-.05.041-.17a.866.866 0 0 0-.121-.415C12.4 1.272 12.063 1 11.5 1z"/> \
                            </svg> \
                        </div>'

        vote_type = request.POST.get('vote_type')
        answer = Answer.objects.get(id=request.POST.get('answer_id'))

        # check if there is a vote for this answer from the same user already
        try:
            # if there is a vote already and it is different from the new vote
            vote = Activity.objects.get(owner=request.user.profile, answer=answer)
            if vote and vote_type != vote.activity_type:
                # update this object with the new vote
                vote.activity_type = vote_type
                vote.save()
                return JsonResponse({
                    'nature': 'change',
                    'vote': vote.activity_type,
                    'vote_html': upvote_html if vote.activity_type == 'U' else downvote_html
                }, status=200)
            # if there is a vote already and it is the same
            elif vote and vote_type == vote.activity_type:
                vote.delete()
                return JsonResponse({
                    'nature': 'delete', 
                    'vote': vote.activity_type,
                    'vote_html': novote_html
                }, status=200)
        except Activity.DoesNotExist:
            vote = Activity.objects.create(
                owner=request.user.profile,
                activity_type=vote_type,
                answer=answer
            )
            return JsonResponse({
                'nature': 'create', 
                'vote': vote.activity_type,
                'vote_html': upvote_html if vote.activity_type == 'U' else downvote_html
            }, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

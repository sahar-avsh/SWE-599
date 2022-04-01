from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import (
    Mindspace,
    Resource,
    Note,
)

from .forms import (
    MindspaceModelForm,
    ResourceModelForm,
    NoteModelForm
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

##################### Mindspace #####################
# Create your views here.
class MindspaceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm
    success_message = 'Your Mindspace was created successfully'

    def form_valid(self, form):
        mindspace = form.save()
        mindspace.owner = self.request.user.profile
        return super().form_valid(form)


class MindspaceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/mindspace_update.html'
    form_class = MindspaceModelForm
    success_message = 'Your Mindspace was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class MindspaceListView(LoginRequiredMixin, ListView):
    template_name = 'mindspace/mindspace_list.html'

    def get_queryset(self):
        queryset = Mindspace.objects.filter(owner=self.request.user.profile)
        return queryset


class MindspaceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/mindspace_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)


class MindspaceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mindspace/mindspace_delete.html'
    success_message = 'Your Mindspace was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mindspace:mindspace_list')

##################### Resource #####################
class ResourceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/resource_create.html'
    form_class = ResourceModelForm
    success_message = 'Your Resource was created successfully'

    def form_valid(self, form):
        form.instance.belongs_to_id = self.kwargs.get('ms_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        return context


class ResourceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/resource_update.html'
    form_class = ResourceModelForm
    success_message = 'Your Resource was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class ResourceListView(LoginRequiredMixin, ListView):
    template_name = 'mindspace/resource_list.html'

    def get_queryset(self):
        mindspace_id = self.kwargs.get('ms_id')
        queryset = Resource.objects.filter(belongs_to_id=mindspace_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        return context


class ResourceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/resource_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mindspace/resource_delete.html'
    success_message = 'Your Resource was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.object.belongs_to.id})


##################### Note #####################
class NoteCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/note_create.html'
    form_class = NoteModelForm
    success_message = 'Your Note was created successfully'

    def form_valid(self, form):
        form.instance.belongs_to_id = self.kwargs.get('r_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Resource.objects.get(id=self.kwargs.get('r_id'))
        return context


class NoteUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/note_update.html'
    form_class = NoteModelForm
    success_message = 'Your Note was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'mindspace/note_list.html'

    def get_queryset(self):
        resource_id = self.kwargs.get('r_id')
        queryset = Note.objects.filter(belongs_to_id=resource_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Resource.objects.get(id=self.kwargs.get('r_id'))
        return context


class NoteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/note_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mindspace/note_delete.html'
    success_message = 'Your Note was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('mindspace:resource_detail', kwargs={'id': self.object.belongs_to.id})
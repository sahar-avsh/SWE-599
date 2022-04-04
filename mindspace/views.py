from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.exceptions import PermissionDenied

from profiles.models import Profile

from .models import (
    Mindspace,
    Resource,
    Note,
)

from .forms import (
    MindspaceModelForm,
    ResourceModelForm,
    NoteModelForm,
    ShareMindspaceForm
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    FormView
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

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner and request.user.profile not in object.editors.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class MindspaceListView(LoginRequiredMixin, ListView):
    template_name = 'mindspace/mindspace_list.html'

    def get_queryset(self):
        queryset = Mindspace.objects.filter(owner=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view = self.request.user.profile.can_view.all()
        comment = self.request.user.profile.can_comment.all()
        edit = self.request.user.profile.can_edit.all()
        context['object_list_view'] = view
        context['object_list_comment'] = comment
        context['object_list_edit'] = edit
        return context

class MindspaceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/mindspace_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
        if not object.is_public:
            if request.user.profile != object.owner:
                if request.user.profile not in all_permissions:
                    raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner and request.user.profile not in object.editors.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ShareMindspaceView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'mindspace/mindspace_share.html'
    form_class = ShareMindspaceForm
    success_message = 'Your Mindspace was shared successfully'
    success_url = reverse_lazy('mindspace:mindspace_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_ = self.kwargs.get('id')
        context['object'] = Mindspace.objects.get(id=id_)
        return context

    def form_valid(self, form):
        if form.cleaned_data['profile_to_share'] not in [p.created_by.email for p in Profile.objects.all()]:
            form.add_error('profile_to_share', 'This profile does not exist.')
            return self.form_invalid(form)
        else:
            profile = Profile.objects.get(created_by__email=form.cleaned_data['profile_to_share'])
            id_ = self.kwargs.get('id')
            mindspace = Mindspace.objects.get(id=id_)
            if form.cleaned_data['access_level'] == 'viewer':
                mindspace.viewers.add(profile)
            elif form.cleaned_data['access_level'] == 'commenter':
                mindspace.commenters.add(profile)
            else:
                mindspace.editors.add(profile)
            return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        if request.user.profile != object.owner and request.user.profile not in object.editors.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ResourceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/resource_update.html'
    form_class = ResourceModelForm
    success_message = 'Your Resource was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        if request.user.profile != object.owner and request.user.profile not in object.editors.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
        if not object.is_public:
            if request.user.profile != object.owner:
                if request.user.profile not in all_permissions:
                    raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ResourceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/resource_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)
    
    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
        if not object.is_public:
            if request.user.profile != object.owner:
                if request.user.profile not in all_permissions:
                    raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        if request.user.profile != object.owner and request.user.profile not in object.editors.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
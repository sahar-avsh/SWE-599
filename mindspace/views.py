from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Mindspace,
    Resource,
)

from .forms import (
    MindspaceModelForm,
    ResourceModelForm,
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
class MindspaceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm

    def form_valid(self, form):
        mindspace = form.save()
        mindspace.owner = self.request.user.profile
        return super().form_valid(form)


class MindspaceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm

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

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def get_success_url(self):
        return reverse('mindspace:mindspace_list')

##################### Resource #####################
class ResourceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mindspace/resource_create.html'
    form_class = ResourceModelForm

    def form_valid(self, form):
        form.instance.belongs_to_id = self.kwargs.get('ms_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        return context


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/resource_create.html'
    form_class = ResourceModelForm

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

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('mindspace:resource_list', kwargs={'ms_id': self.object.belongs_to.id})
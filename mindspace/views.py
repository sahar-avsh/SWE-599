from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Mindspace
from .forms import MindspaceModelForm
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
# Create your views here.
class MindspaceCreateView(CreateView):
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm

    def form_valid(self, form):
        return super().form_valid(form)

    # override default success redirect url
"""     def get_success_url(self):
        return '/' """

class MindspaceUpdateView(UpdateView):
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class MindspaceListView(ListView):
    template_name = 'mindspace/mindspace_list.html'
    queryset = Mindspace.objects.all()


class MindspaceDetailView(DetailView):
    template_name = 'mindspace/mindspace_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)


class MindspaceDeleteView(DeleteView):
    template_name = 'mindspace/mindspace_delete.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def get_success_url(self):
        return reverse('mindspace:mindspace_list')


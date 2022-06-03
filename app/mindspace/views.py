from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse, Http404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, Page, InvalidPage

from profiles.models import Profile

from .models import (
    Mindspace,
    Resource,
    Note,
    ShareMindspace,
)

from .forms import (
    MindspaceModelForm,
    ResourceModelForm,
    NoteModelForm,
    ShareMindspaceModelForm,
    ShareMindspaceModelFormSet,
    MindspaceSearchForm,
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,
    View,
)

##################### Mindspace #####################
# Create your views here.
class MindspaceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = MindspaceModelForm
    success_message = 'Your Mindspace was created successfully'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
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
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile, access_level=ShareMindspace.editor).exists()
        if request.user.profile != object.owner and not allowed:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class MindspaceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mindspace/mindspace_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_create'] = MindspaceModelForm()
        context['form_search'] = MindspaceSearchForm()
        return context

class MindspaceListView(LoginRequiredMixin, TemplateView):
    template_name = 'mindspace/mindspace_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shared_with = [i.mindspace for i in ShareMindspace.objects.filter(shared_with=self.request.user.profile).order_by('shared_date')]
        my_mindspaces = Mindspace.objects.filter(owner=self.request.user.profile).order_by('created_at')

        if 'shared-mindspace-page' in self.request.GET.keys():
            paginator = Paginator(shared_with, self.paginate_by)
            page_kwarg = 'shared-mindspace-page'
            context['is_viewing'] = 'shared-mindspace'
        elif 'my-mindspace-page' in self.request.GET.keys():
            paginator = Paginator(my_mindspaces, self.paginate_by)
            page_kwarg = 'my-mindspace-page'
            context['is_viewing'] = 'my-mindspace'

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

class LoadMindspaceDetailItems(LoginRequiredMixin, ListView):
    template_name = 'mindspace/mindspace_detail_items.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET.get('category') == 'resources':
            queryset = Mindspace.objects.get(id=self.request.GET.get('ms_id')).resources.all().order_by('updated_at')
        else:
            queryset = Mindspace.objects.get(id=self.request.GET.get('ms_id')).mindspace_questions.all().order_by('asked_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Mindspace.objects.get(id=self.request.GET.get('ms_id'))

        shares = obj.shares.all()
        edit_access = [i.shared_with for i in shares if i.access_level == 'editor']
        context['profile_has_edit_access'] = self.request.user.profile in edit_access

        context['object'] = obj
        context['category'] = self.request.GET.get('category')

        if 'resources-page' in self.request.GET.keys(): 
            page_kwarg = 'resources-page'
        elif 'questions-page' in self.request.GET.keys():
            page_kwarg = 'questions-page'
        else:
            page_kwarg = None

        paginator = Paginator(self.get_queryset(), self.paginate_by)
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


class MindspaceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/mindspace_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        shares = obj.shares.all()
        edit_access = [i.shared_with for i in shares if i.access_level == 'editor']
        context['profile_has_edit_access'] = self.request.user.profile in edit_access
        return context

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile).exists()
        if not object.is_public:
            if request.user.profile != object.owner:
                if not allowed:
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
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('mindspace:mindspace_list')

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ShareMindspaceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/mindspace_share.html'
    form_class = ShareMindspaceModelForm
    model = ShareMindspace
    success_message = "Your Mindspace's access levels have been updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mindspace = Mindspace.objects.get(id=self.kwargs.get('id'))
        sm = ShareMindspace.objects.filter(mindspace=mindspace)
        context['formset'] = ShareMindspaceModelFormSet(queryset=sm)
        context['mindspace'] = mindspace
        return context

    def post(self, request, *args, **kwargs):
        formset = ShareMindspaceModelFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            self.object = None
            return self.form_invalid(formset)

    def form_valid(self, formset):
        for instance in formset:
            if instance.has_changed():
                if instance.cleaned_data['shared_with_info'] not in [p.created_by.email for p in Profile.objects.all()] and instance.cleaned_data['shared_with_info'] not in [p.created_by.username for p in Profile.objects.all()]:
                    instance.add_error('shared_with_info', 'This profile does not exist.')
                    return self.form_invalid(formset)
                else:
                    form = instance.save(commit=False)
                    form.shared_by = self.request.user.profile
                    try:
                        profile = Profile.objects.get(created_by__email=instance.cleaned_data['shared_with_info'])
                    except (Profile.DoesNotExist):
                        profile = Profile.objects.get(created_by__username=instance.cleaned_data['shared_with_info'])
                    form.shared_with = profile
                    form.shared_with_info = profile.created_by.username
                    form.mindspace = Mindspace.objects.get(id=self.kwargs.get('id'))
        return super().form_valid(formset)

    def form_invalid(self, formset):
        form_errors = formset.errors
        err_msgs = {}
        for index, error in enumerate(form_errors):
            if error:
                error_list = error.as_text().split('*')
                err_msg = error_list[-1].strip()
                err_msgs[index] = err_msg
        self.object = None
        return JsonResponse({'error': err_msgs}, status=400)

    def get_success_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.kwargs.get('id')})

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AjaxMindspaceSearch(LoginRequiredMixin, ListView):
    template_name = 'mindspace/ajax_mindspace_results.html'
    paginate_by = 5
    page_kwarg = 'search-mindspace-page'

    def get_queryset(self):
        queryset = Mindspace.objects.filter(is_public=True).exclude(owner=self.request.user.profile).order_by('created_at')

        keyword_query = self.request.GET.get('keyword_query')
        owner_query = self.request.GET.get('owner_query')

        # filter by title
        if keyword_query:
            queryset = queryset.filter(
                Q(title__icontains=keyword_query) | Q(description__icontains=keyword_query) | Q(resources__title__icontains=keyword_query) | Q(resources__description__icontains=keyword_query)
            )
        # filter by owner
        if owner_query:
            queryset = queryset.filter(owner__created_by__username__icontains=owner_query)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.request.GET.items():
            if key in ['keyword_query', 'owner_query'] and value:
                context[key] = value
                context['filter_flag'] = True
        return context


##################### Resource #####################
class ResourceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/resource_create.html'
    form_class = ResourceModelForm
    success_message = 'Your Resource was created successfully'

    def form_valid(self, form):
        form.instance.belongs_to_id = self.kwargs.get('ms_id')
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        return context

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile, access_level=ShareMindspace.editor).exists()
        if request.user.profile != object.owner and not allowed:
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
        self.object = form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile, access_level=ShareMindspace.editor).exists()
        if request.user.profile != object.owner and not allowed:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ResourceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/resource_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Resource, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Note.objects.filter(belongs_to=self.get_object())
        context['notes'] = qs
        return context
    
    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile).exists()
        if not object.is_public:
            if request.user.profile != object.owner:
                if not allowed:
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
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

##################### Note #####################
class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'mindspace/note_list.html'
    model = Note
    
    def get_queryset(self):
        resource_id = self.request.GET.get('resource')
        queryset = Note.objects.filter(belongs_to_id=resource_id).order_by('created_at')
        return queryset

class NoteCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/note_create.html'
    model = Note
    form_class = NoteModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource'] = Resource.objects.get(id=self.kwargs.get('r_id'))
        return context

    def get_success_url(self):
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.kwargs.get('ms_id'), 'id': self.kwargs.get('r_id')})

    def form_valid(self, form):
        form.instance.belongs_to = Resource.objects.get(id=self.kwargs.get('r_id'))
        form.instance.written_by = self.request.user.profile
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'mindspace/note_update.html'
    form_class = NoteModelForm
    model = Note

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def get_success_url(self):
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.kwargs.get('ms_id'), 'id': self.kwargs.get('r_id')})


class NoteDeleteView(LoginRequiredMixin, DeleteView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.object.belongs_to.belongs_to.id, 'id': self.object.belongs_to.id})
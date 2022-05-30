from itertools import chain
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from django.core.exceptions import PermissionDenied

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
    # ShareMindspaceForm,
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
    template_name = 'mindspace/mindspace_create.html'
    form_class = MindspaceModelForm
    success_message = 'Your Mindspace was created successfully'

    def form_valid(self, form):
        mindspace = form.save(commit=False)
        mindspace.owner = self.request.user.profile
        # return super().form_valid(form)
        mindspace.save()
        return JsonResponse({'nextURL': reverse('mindspace:mindspace_detail', kwargs={'id': mindspace.id})}, status=200)


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

class MindspaceListView(LoginRequiredMixin, ListView):
    # template_name = 'mindspace/mindspace_list.html'
    template_name = 'mindspace/mindspace_dashboard.html'

    def get_queryset(self):
        queryset = Mindspace.objects.filter(owner=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_create'] = MindspaceModelForm()
        context['form_search'] = MindspaceSearchForm()

        view = ShareMindspace.objects.filter(shared_with=self.request.user.profile, access_level=ShareMindspace.viewer)
        comment = ShareMindspace.objects.filter(shared_with=self.request.user.profile, access_level=ShareMindspace.commenter)
        edit = ShareMindspace.objects.filter(shared_with=self.request.user.profile, access_level=ShareMindspace.editor)
        context['object_list_view'] = view
        context['object_list_comment'] = comment
        context['object_list_edit'] = edit
        return context

class MindspaceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mindspace/mindspace_detail2.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Mindspace, id=id_)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        # all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
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
        self.object.delete()
        # return super().delete(request, *args, **kwargs)
        return JsonResponse({'nextURL': reverse('mindspace:mindspace_list')}, status=200)

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
        # sm_shared_with = [s.shared_with.created_by.email for s in sm]
        # initial_data = {}
        # for i in range(len(sm)):
        #     initial_data['access_level'] = sm[i].access_level
        #     initial_data['shared_with_info'] = sm_shared_with[i]
        # print(initial_data)
        # context['formset'] = ShareMindspaceModelFormSet(initial=shared_profiles, queryset=ShareMindspace.objects.none())
        # context['formset'] = ShareMindspaceModelFormSet(initial=[initial_data], queryset=ShareMindspace.objects.none())
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
            # return super().post(self, request, *args, **kwargs)

    def form_valid(self, formset):
        # instances = formset.save(commit=False)
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
                    #form.save()
        # formset.save()
        return super().form_valid(formset)
        #return HttpResponseRedirect(reverse('mindspace:mindspace_detail', kwargs={'id': self.kwargs.get('id')}))

    def form_invalid(self, formset):
        form_errors = formset.errors
        err_msgs = {}
        for index, error in enumerate(form_errors):
            if error:
                error_list = error.as_text().split('*')
                err_msg = error_list[-1].strip()
                err_msgs[index] = err_msg
        self.object = None
        return self.render_to_response(self.get_context_data(formset=formset, form_errors=form_errors, err_msgs=err_msgs))

    def get_success_url(self):
        return reverse('mindspace:mindspace_detail', kwargs={'id': self.kwargs.get('id')})

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object.owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# class ShareMindspaceView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = 'mindspace/mindspace_share.html'
#     form_class = ShareMindspaceForm
#     success_message = 'Your Mindspace was shared successfully'
#     success_url = reverse_lazy('mindspace:mindspace_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         id_ = self.kwargs.get('id')
#         object = Mindspace.objects.get(id=id_)
#         context['object'] = object
#         editors = object.editors.all()
#         context['editors'] = editors
#         commenters = object.commenters.all()
#         context['commenters'] = commenters
#         viewers = object.viewers.all()
#         context['viewers'] = viewers
#         context['access_levels'] = self.form_class.ACCESS_LEVELS
#         return context

#     def form_valid(self, form):
#         if form.cleaned_data['profile_to_share'] not in [p.created_by.email for p in Profile.objects.all()]:
#             form.add_error('profile_to_share', 'This profile does not exist.')
#             return self.form_invalid(form)
#         else:
#             profile = Profile.objects.get(created_by__email=form.cleaned_data['profile_to_share'])
#             id_ = self.kwargs.get('id')
#             mindspace = Mindspace.objects.get(id=id_)
#             if form.cleaned_data['access_level'] == 'viewer':
#                 mindspace.viewers.add(profile)
#             elif form.cleaned_data['access_level'] == 'commenter':
#                 mindspace.commenters.add(profile)
#             else:
#                 mindspace.editors.add(profile)
#             return super().form_valid(form)

#     def dispatch(self, request, *args, **kwargs):
#         object = Mindspace.objects.get(id=self.kwargs.get('id'))
#         if request.user.profile != object.owner:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)

class AjaxMindspaceSearch(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        result = Mindspace.objects.filter(is_public=True).exclude(owner=request.user.profile)

        keyword_query = request.GET.get('keyword_query')
        owner_query = request.GET.get('owner_query')

        # filter by title
        if keyword_query:
            result = result.filter(
                Q(title__icontains=keyword_query) | Q(description__icontains=keyword_query) | Q(resources__title__icontains=keyword_query) | Q(resources__description__icontains=keyword_query)
            )
        # filter by owner
        if owner_query:
            result = result.filter(owner__created_by__username__icontains=owner_query)

        context['filter_flag'] = False
        for key, value in self.request.GET.items():
            if key in ['keyword_query', 'owner_query'] and value:
                context[key] = value
                context['filter_flag'] = True

        context['result_list'] = result.distinct()

        return render(request, 'mindspace/ajax_mindspace_results.html', context)

class MindspaceSearchListView(LoginRequiredMixin, ListView):
    model = Mindspace
    template_name = 'mindspace/mindspace_search_list.html'

    def get_queryset(self):
        result = Mindspace.objects.all().exclude(owner=self.request.user.profile)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MindspaceSearchForm()
        context['form'] = form
        return context

##################### Resource #####################
class ResourceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'mindspace/resource_create.html'
    form_class = ResourceModelForm
    success_message = 'Your Resource was created successfully'

    def form_valid(self, form):
        form.instance.belongs_to_id = self.kwargs.get('ms_id')
        resource = form.save()
        return JsonResponse({'resource_id': resource.id}, status=200)
        # return super().form_valid(form)

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
        return JsonResponse({'update': 'done'}, status=200)
        # return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        object = Mindspace.objects.get(id=self.kwargs.get('ms_id'))
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile, access_level=ShareMindspace.editor).exists()
        if request.user.profile != object.owner and not allowed:
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
        allowed = ShareMindspace.objects.filter(mindspace=object, shared_with=request.user.profile).exists()
        # all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
        if not object.is_public:
            if request.user.profile != object.owner:
                if not allowed:
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
        # all_permissions = object.editors.all() | object.commenters.all() | object.viewers.all()
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
class NotesAjaxView(TemplateView):
    template_name = 'mindspace/notes_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource_id = self.request.GET.get('resource')
        qs = Note.objects.filter(belongs_to_id=resource_id).order_by('created_at')
        context['note_list'] = qs
        return context


from django.http import JsonResponse
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.id,
            }
            return JsonResponse(data)
        else:
            return response


class NoteFormAjax(TemplateView):
    template_name = 'mindspace/note_form_ajax.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NoteModelForm()
        return context


class NoteCreateView(SuccessMessageMixin, LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    template_name = 'mindspace/note_create.html'
    model = Note
    form_class = NoteModelForm
    success_message = 'Your Note was created successfully'

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.kwargs.get('ms_id'), 'id': self.kwargs.get('r_id')})

    def form_valid(self, form):
        form.instance.belongs_to = Resource.objects.get(id=self.kwargs.get('r_id'))
        form.instance.written_by = self.request.user.profile
        return super().form_valid(form)


# class NoteUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     template_name = 'mindspace/note_update.html'
#     form_class = NoteModelForm
#     success_message = 'Your Note was updated successfully'

#     def get_object(self):
#         id_ = self.kwargs.get('id')
#         return get_object_or_404(Note, id=id_)

#     def form_valid(self, form):
#         return super().form_valid(form)


# class NoteListView(LoginRequiredMixin, ListView):
#     template_name = 'mindspace/note_list.html'

#     def get_queryset(self):
#         resource_id = self.kwargs.get('r_id')
#         queryset = Note.objects.filter(belongs_to_id=resource_id)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['parent'] = Resource.objects.get(id=self.kwargs.get('r_id'))
#         return context


# class NoteDetailView(LoginRequiredMixin, DetailView):
#     template_name = 'mindspace/note_detail.html'

#     def get_object(self):
#         id_ = self.request.GET.get('note_id')
#         # id_ = self.kwargs.get('id')
#         return get_object_or_404(Note, id=id_)


class NoteUpdateView(SuccessMessageMixin, LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    template_name = 'mindspace/note_update.html'
    form_class = NoteModelForm
    model = Note
    success_message = 'Your Note was updated successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def get_success_url(self):
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.kwargs.get('ms_id'), 'id': self.kwargs.get('r_id')})


class NoteDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    # template_name = 'mindspace/note_delete.html'
    # success_message = 'Your Note was deleted successfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Note, id=id_)

    def delete(self, request, *args, **kwargs):
        # messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('mindspace:resource_detail', kwargs={'ms_id': self.object.belongs_to.belongs_to.id, 'id': self.object.belongs_to.id})
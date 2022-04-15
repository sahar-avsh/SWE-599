from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView,
)

from django.contrib.auth import login, authenticate

from django.core.exceptions import PermissionDenied

from .models import (
  Profile,
  Notification
)

from .forms import (
    ProfileModelForm,
    UserLoginForm,
    UserRegisterForm
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView
)


class HomeView(TemplateView):
    template_name = 'profiles/home.html'


class CustomLoginView(SuccessMessageMixin, FormView):
    template_name = 'profiles/user_login.html'
    form_class = UserLoginForm
    success_message = 'You have successfully logged in'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        else:
            return reverse_lazy('mindspace:mindspace_list')


class CustomSignUpView(SuccessMessageMixin, CreateView):
    template_name = 'profiles/user_register.html'
    form_class = UserRegisterForm
    success_message = 'Your profile was created successfully'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(created_by=user, f_name=user.first_name, l_name=user.last_name)
        return super().form_valid(form)


class CustomResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'profiles/password_reset.html'
    email_template_name = 'profiles/password_reset_email.html'
    subject_template_name = 'profiles/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting up your password, " \
                      "if an account exists with the email you entered, you should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you had registered with, and check your spam folder."
    success_url = reverse_lazy('main_page')


class ProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profile_update.html'
    form_class = ProfileModelForm
    success_message = 'Your profile was updated succesfully'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        object = Profile.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)

class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'profiles/notification_list.html'

    def get_queryset(self):
        queryset = Notification.objects.filter(received_by=self.request.user.profile).order_by('sent_date')
        return queryset
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import login, authenticate

from .models import (
  Profile
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
    success_url = reverse_lazy('mindspace:mindspace_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)


class CustomSignUpView(SuccessMessageMixin, CreateView):
    template_name = 'profiles/user_register.html'
    form_class = UserRegisterForm
    success_message = 'Your profile was created successfully'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(created_by=user, f_name=user.first_name, l_name=user.last_name)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profile_update.html'
    form_class = ProfileModelForm

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)
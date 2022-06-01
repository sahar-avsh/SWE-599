"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView

from profiles.views import (
    HomeView,
    CustomLoginView,
    CustomSignUpView,
    CustomResetPasswordView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mindspace/', include('mindspace.urls')),
    path('profiles/', include('profiles.urls')),
    path('questions/', include('qna.urls')),
    path('accounts/signup/', CustomSignUpView.as_view(), name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('main_page')),  name='logout'),
    path('accounts/password-reset/', CustomResetPasswordView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', \
        PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'), \
        name='password_reset_confirm'),
    path('accounts/password-reset-complete/', \
        PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), \
        name='password_reset_complete'),
    path('home/', HomeView.as_view(), name='main_page'),
    path('', HomeView.as_view(), name='main_page'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

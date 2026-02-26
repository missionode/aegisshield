from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from .forms import SignupForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

def logout_view(request):
    logout(request)
    return redirect('core:index')

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:onboarding')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

class LoginView(DjangoLoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('diagnose:dashboard')

class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = 'users/onboarding.html'

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    fields = ['full_name', 'location', 'avatar']
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
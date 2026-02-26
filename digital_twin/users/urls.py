from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('onboarding/', views.OnboardingView.as_view(), name='onboarding'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
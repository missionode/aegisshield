from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('blog/', views.blog, name='blog'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('contact-us/', views.contact_us, name='contact_us'),
]

from django.urls import path
from . import views

app_name = 'diagnose'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('scanner/', views.ScannerView.as_view(), name='scanner'),
    path('analysis/<int:scan_id>/', views.AnalysisView.as_view(), name='analysis'),
    path('api/analyze/<int:scan_id>/', views.start_analysis, name='start_analysis'),
    path('api/favorite/<int:scan_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('result/<int:scan_id>/', views.ResultView.as_view(), name='result'),
]
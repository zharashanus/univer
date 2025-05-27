from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    path('', views.RecognitionInfoView.as_view(), name='info'),
    path('apply/', views.RecognitionApplyView.as_view(), name='apply'),
    path('apply/success/', views.RecognitionApplySuccessView.as_view(), name='apply_success'),
    path('check-status/', views.CheckStatusView.as_view(), name='check_status'),
    path('calculator/', views.CalculatorView.as_view(), name='calculator'),
] 
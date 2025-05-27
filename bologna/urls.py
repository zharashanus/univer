from django.urls import path
from . import views

app_name = 'bologna'

urlpatterns = [
    path('', views.BolognaInfoView.as_view(), name='info'),
    path('esg/', views.ESGView.as_view(), name='esg'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
] 
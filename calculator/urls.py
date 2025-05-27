from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.CalculatorView.as_view(), name='index'),
] 
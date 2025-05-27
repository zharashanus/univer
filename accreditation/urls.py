from django.urls import path
from . import views

app_name = 'accreditation'

urlpatterns = [
    path('', views.AccreditationInfoView.as_view(), name='info'),
    path('registry/', views.RegistryView.as_view(), name='registry'),
    path('criteria/', views.CriteriaView.as_view(), name='criteria'),
] 
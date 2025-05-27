from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.ContactInfoView.as_view(), name='info'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('feedback/success/', views.FeedbackSuccessView.as_view(), name='feedback_success'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('quick-feedback-process/', views.QuickFeedbackProcessView.as_view(), name='quick_feedback_process'),
] 
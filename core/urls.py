"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.views.i18n import set_language

# API URLs (without language prefix)
api_urlpatterns = [
    path('api/', include('rest_framework.urls')),
    # Add other API endpoints here when needed
]

# Main URL patterns with i18n support
urlpatterns = [
    # Redirect root to Kazakh version
    path('', RedirectView.as_view(url='/kk/', permanent=False)),
]

urlpatterns += i18n_patterns(
    # Admin
    path('admin/', admin.site.urls),
    
    # Main applications
    path('', include('pages.urls')),
    path('news/', include('news.urls')),
    path('recognition/', include('recognition.urls')),
    path('accreditation/', include('accreditation.urls')),
    path('bologna/', include('bologna.urls')),
    path('contacts/', include('contacts.urls')),
    path('accounts/', include('accounts.urls')),
    path('calculator/', include('calculator.urls')),
    
    prefix_default_language=True,
)

# Add API URLs without language prefix
urlpatterns += api_urlpatterns

# Language switching
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

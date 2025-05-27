from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Главная страница'),
            'meta_description': _('Национальный центр развития высшего образования - признание документов об образовании, аккредитация, болонский процесс'),
        })
        return context


class AboutView(TemplateView):
    """О центре"""
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('О центре'),
            'breadcrumbs': [
                {'title': _('О центре'), 'url': None}
            ]
        })
        return context


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика конфиденциальности'
        return context


class TermsView(TemplateView):
    template_name = 'pages/terms.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Условия использования'
        return context


class SearchView(TemplateView):
    """Поиск по сайту"""
    template_name = 'pages/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        context['title'] = f'Результаты поиска: {query}' if query else 'Поиск по сайту'
        return context

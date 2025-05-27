from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class NewsListView(TemplateView):
    """Список новостей"""
    template_name = 'news/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Новости'),
            'breadcrumbs': [
                {'title': _('Новости'), 'url': None}
            ]
        })
        return context


class NewsDetailView(TemplateView):
    """Детальная страница новости"""
    template_name = 'news/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Новость'),
            'breadcrumbs': [
                {'title': _('Новости'), 'url': 'news:list'},
                {'title': _('Новость'), 'url': None}
            ]
        })
        return context

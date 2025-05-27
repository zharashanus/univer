from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class BolognaInfoView(TemplateView):
    template_name = 'bologna/info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Болонский процесс'),
        })
        return context


class ESGView(TemplateView):
    template_name = 'bologna/esg.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ESG стандарты'
        return context


class ReportsView(TemplateView):
    template_name = 'bologna/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Национальные доклады'
        return context

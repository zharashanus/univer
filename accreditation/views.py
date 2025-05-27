from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class AccreditationInfoView(TemplateView):
    template_name = 'accreditation/info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Аккредитация образовательных программ'),
        })
        return context


class RegistryView(TemplateView):
    template_name = 'accreditation/registry.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Реестр аккредитованных программ'),
        })
        return context


class CriteriaView(TemplateView):
    template_name = 'accreditation/criteria.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Критерии аккредитации'),
        })
        return context

from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class CalculatorView(TemplateView):
    template_name = 'calculator/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Калькулятор признания документов'),
        })
        return context

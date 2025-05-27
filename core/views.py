from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


def handler404(request, exception):
    """Обработчик ошибки 404 - страница не найдена"""
    context = {
        'title': _('Страница не найдена'),
        'message': _('Запрашиваемая страница не существует или была перемещена.'),
    }
    return render(request, 'errors/404.html', context, status=404)


def handler500(request):
    """Обработчик ошибки 500 - внутренняя ошибка сервера"""
    context = {
        'title': _('Внутренняя ошибка сервера'),
        'message': _('Произошла ошибка на сервере. Попробуйте повторить запрос позже.'),
    }
    return render(request, 'errors/500.html', context, status=500)


class SearchView(TemplateView):
    """Поиск по сайту"""
    template_name = 'search/results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        context.update({
            'title': _('Результаты поиска'),
            'query': query,
            'results': [],  # TODO: Implement search functionality
        })
        
        return context 
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm, QuickFeedbackForm
from .models import FAQ, ContactMessage


class ContactInfoView(TemplateView):
    template_name = 'contacts/info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Контакты'),
            'quick_feedback_form': QuickFeedbackForm()
        })
        return context


class FeedbackView(FormView):
    template_name = 'contacts/feedback.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:feedback_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Обратная связь'),
        })
        return context

    def form_valid(self, form):
        try:
            form.save(request=self.request) # Передаем request для сохранения IP и User Agent
            messages.success(self.request, 
                _('Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, _('Произошла ошибка при отправке сообщения: %(error)s') % {'error': str(e)})
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Пожалуйста, исправьте ошибки в форме.'))
        return super().form_invalid(form)


class FeedbackSuccessView(TemplateView):
    template_name = 'contacts/feedback_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Сообщение отправлено'),
        })
        return context


class FAQListView(ListView):
    model = FAQ
    template_name = 'contacts/faq.html'
    context_object_name = 'faq_list'
    paginate_by = 20 # Если вопросов много

    def get_queryset(self):
        return FAQ.objects.filter(is_published=True).order_by('category', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Часто задаваемые вопросы'),
            'categories': FAQ.CATEGORY_CHOICES
        })
        return context

# View для обработки QuickFeedbackForm (например, в футере сайта)
class QuickFeedbackProcessView(FormView):
    form_class = QuickFeedbackForm
    # Успешный URL зависит от того, где используется форма (AJAX или обычная отправка)
    # Для AJAX можно вернуть JSON-ответ, для обычной - редирект или сообщение
    success_url = reverse_lazy('pages:home') # Пример, изменить на нужный

    def form_valid(self, form):
        try:
            form.save(request=self.request)
            messages.success(self.request, _('Ваш вопрос отправлен!'))
            # Если это AJAX-запрос, можно вернуть JsonResponse
            # if self.request.is_ajax(): 
            #     return JsonResponse({'message': _('Ваш вопрос отправлен!')}, status=200)
        except Exception as e:
            messages.error(self.request, _('Ошибка отправки: %(error)s') % {'error': str(e)})
            # if self.request.is_ajax():
            #     return JsonResponse({'error': str(e)}, status=400)
        
        # Для не-AJAX запросов, делаем редирект (можно на ту же страницу с якорем)
        referer_url = self.request.META.get('HTTP_REFERER', self.success_url)
        return redirect(referer_url + '#quick-feedback-form') # Добавляем якорь

    def form_invalid(self, form):
        messages.error(self.request, _('Ошибка в форме быстрой обратной связи.'))
        # if self.request.is_ajax():
        #     return JsonResponse(form.errors, status=400)
        referer_url = self.request.META.get('HTTP_REFERER', self.success_url)
        # Можно передать ошибки формы в сессию, чтобы отобразить их на предыдущей странице
        # self.request.session['quick_feedback_errors'] = form.errors.as_json()
        return redirect(referer_url + '#quick-feedback-form')

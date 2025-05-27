from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404

from .forms import RecognitionApplicationForm, StatusCheckForm
from .models import RecognitionApplication, RecognitionApplicationHistory, RecognitionDocument


class RecognitionInfoView(TemplateView):
    template_name = 'recognition/info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Признание зарубежных документов об образовании'),
        })
        return context


class RecognitionApplyView(FormView):
    template_name = 'recognition/apply.html'
    form_class = RecognitionApplicationForm
    success_url = reverse_lazy('recognition:apply_success')

    def get_form_kwargs(self):
        """Передаем request в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Подать заявку на признание'),
        })
        return context

    def form_valid(self, form):
        try:
            # Метод save формы теперь сам обрабатывает пользователя, если request передан
            application = form.save() 
            
            # Сохраняем номер заявки в сессии для отображения на странице успеха
            self.request.session['last_application_number'] = application.application_number

            messages.success(self.request, 
                _('Ваша заявка №{application_number} успешно подана! Вы можете отслеживать ее статус на сайте.')
                .format(application_number=application.application_number)
            )
            return super().form_valid(form)
        except Exception as e:
            # Логирование ошибки может быть полезно здесь
            # logger.error(f"Error submitting recognition application: {e}", exc_info=True)
            messages.error(self.request, _('Произошла ошибка при подаче заявки. Пожалуйста, попробуйте снова. Детали: %(error)s') % {'error': str(e)})
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Пожалуйста, исправьте ошибки в форме. Проверьте все поля.'))
        return super().form_invalid(form)

class RecognitionApplySuccessView(TemplateView):
    template_name = 'recognition/apply_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно передать номер заявки через сессию или URL, если нужно его здесь отобразить
        # application_number = self.request.session.get('last_application_number')
        context.update({
            'title': _('Заявка успешно подана'),
            # 'application_number': application_number 
        })
        return context


class CheckStatusView(FormView):
    template_name = 'recognition/check_status.html'
    form_class = StatusCheckForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Проверить статус заявки'),
        })
        return context

    def form_valid(self, form):
        application_number = form.cleaned_data['application_number']
        applicant_email = form.cleaned_data['applicant_email']
        
        try:
            application = RecognitionApplication.objects.get(
                application_number__iexact=application_number, # Регистронезависимый поиск
                applicant_email__iexact=applicant_email
            )
            documents = application.documents.all() # Используем related_name
            history = application.history.all().order_by('-changed_at') # Используем related_name
            
            return render(self.request, self.template_name, {
                'form': form, # Передаем форму обратно для отображения
                'application': application,
                'documents': documents,
                'history': history,
                'title': _('Статус заявки №{number}').format(number=application.application_number),
                'search_successful': True
            })
        except RecognitionApplication.DoesNotExist:
            messages.error(self.request, _('Заявка с указанным номером и/или email не найдена. Проверьте введенные данные.'))
            return render(self.request, self.template_name, {
                'form': form,
                'title': _('Проверить статус заявки'),
                'search_successful': False
            })
        except Exception as e:
            # logger.error(f"Error checking application status: {e}", exc_info=True)
            messages.error(self.request, _('Произошла ошибка при проверке статуса: %(error)s') % {'error': str(e)})
            # Важно вернуть form_invalid, чтобы не пытаться сделать редирект
            return self.render_to_response(self.get_context_data(form=form, search_successful=False))

    # def form_invalid(self, form): # Стандартная обработка form_invalid из FormView уже добавляет ошибки в messages
    #     messages.error(self.request, _('Пожалуйста, исправьте ошибки в форме проверки статуса.'))
    #     return super().form_invalid(form)


class CalculatorView(TemplateView):
    template_name = 'recognition/calculator.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Калькулятор признания'),
        })
        return context

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Field
import re

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""
    
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label=_('Подтверждение')
    )
    
    # Согласие на обработку данных
    data_processing_consent = forms.BooleanField(
        required=True,
        label=_('Я согласен на обработку персональных данных'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'organization', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите ваше имя')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('example@email.com')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите ваш номер телефона (необязательно)')
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Название организации (необязательно)')
            }),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': _('Опишите ваш вопрос или проблему подробно')
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="alert alert-info"><i class="bi bi-info-circle"></i> {% trans "Заполните форму ниже, и мы свяжемся с вами в течение 1-2 рабочих дней." %}</div>'),
            
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-3'),
                Column('organization', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('subject', css_class='mb-3'),
            Field('message', css_class='mb-4'),
            Field('captcha', css_class='mb-3'),
            Field('data_processing_consent', css_class='mb-3'),
            
            Submit('submit', _('Отправить сообщение'), css_class='btn btn-primary btn-lg')
        )
    
    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Убираем все символы кроме цифр и +
            phone_digits = re.sub(r'[^\d+]', '', phone)
            if not re.match(r'^\+?[78]\d{10}$', phone_digits):
                raise ValidationError(_('Введите корректный номер телефона'))
        return phone
    
    def clean_message(self):
        """Валидация сообщения"""
        message = self.cleaned_data.get('message')
        if message:
            # Проверяем минимальную длину сообщения
            if len(message.strip()) < 10:
                raise ValidationError(_('Сообщение должно содержать не менее 10 символов'))
            
            # Простая проверка на спам (повторяющиеся символы)
            import re
            spam_patterns = [
                r'(.)\1{10,}',  # 10+ одинаковых символов подряд
                r'[A-Z]{20,}',  # 20+ заглавных букв подряд
                r'www\.|http|\.com|\.org|\.net',  # ссылки
            ]
            
            for pattern in spam_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    raise ValidationError(_('Сообщение содержит недопустимый контент'))
        
        return message
    
    def save(self, request=None, commit=True):
        """Сохранение сообщения с дополнительной информацией"""
        message = super().save(commit=False)
        
        if request:
            # Сохраняем IP адрес и User Agent
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                message.ip_address = x_forwarded_for.split(',')[0]
            else:
                message.ip_address = request.META.get('REMOTE_ADDR')
            
            message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Связываем с пользователем, если он авторизован
            if request.user.is_authenticated:
                message.user = request.user
        
        if commit:
            message.save()
        
        return message


class QuickFeedbackForm(forms.Form):
    """Быстрая форма обратной связи для виджетов на сайте"""
    
    name = forms.CharField(
        max_length=100,
        label=_('Ваше имя'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваше имя')
        })
    )
    
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@email.com')
        })
    )
    
    message = forms.CharField(
        label=_('Ваш вопрос'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Задайте ваш вопрос')
        })
    )
    
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label=_('Подтверждение')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('email', css_class='mb-3'),
            Field('message', css_class='mb-3'),
            Field('captcha', css_class='mb-3'),
            Submit('submit', _('Отправить'), css_class='btn btn-primary')
        )
    
    def clean_message(self):
        """Валидация сообщения"""
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 5:
            raise ValidationError(_('Сообщение должно содержать не менее 5 символов'))
        return message
    
    def save(self, request=None):
        """Сохранение быстрого сообщения"""
        data = self.cleaned_data
        
        contact_message = ContactMessage(
            name=data['name'],
            email=data['email'],
            message=data['message'],
            subject='general',  # По умолчанию общий вопрос
        )
        
        if request:
            # Сохраняем IP адрес и User Agent
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact_message.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact_message.ip_address = request.META.get('REMOTE_ADDR')
            
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Связываем с пользователем, если он авторизован
            if request.user.is_authenticated:
                contact_message.user = request.user
        
        contact_message.save()
        return contact_message 
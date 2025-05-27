from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div, Field
from crispy_forms.bootstrap import PrependedText, AppendedText
import re

from .models import RecognitionApplication, RecognitionDocument


class RecognitionApplicationForm(forms.ModelForm):
    """Форма подачи заявки на признание документов"""
    
    # Поля для загрузки документов
    diploma_file = forms.FileField(
        required=True,
        label=_('Диплом (PDF, JPG, PNG)'),
        help_text=_('Максимальный размер файла: 5MB'),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    transcript_file = forms.FileField(
        required=True,
        label=_('Транскрипт/Приложение к диплому (PDF, JPG, PNG)'),
        help_text=_('Максимальный размер файла: 5MB'),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    passport_file = forms.FileField(
        required=True,
        label=_('Копия паспорта (PDF, JPG, PNG)'),
        help_text=_('Максимальный размер файла: 5MB'),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    translation_file = forms.FileField(
        required=False,
        label=_('Нотариальный перевод (PDF, JPG, PNG)'),
        help_text=_('Максимальный размер файла: 5MB. Необязательно'),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    # reCAPTCHA
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
        model = RecognitionApplication
        fields = [
            'applicant_first_name', 'applicant_last_name', 'applicant_middle_name',
            'applicant_email', 'applicant_phone', 'applicant_iin',
            'institution_name', 'institution_country', 'education_level',
            'specialty', 'graduation_year', 'duration_years',
            'purpose', 'notes'
        ]
        widgets = {
            'applicant_first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите ваше имя')
            }),
            'applicant_last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите вашу фамилию')
            }),
            'applicant_middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите ваше отчество (необязательно)')
            }),
            'applicant_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('example@email.com')
            }),
            'applicant_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите ваш номер телефона')
            }),
            'applicant_iin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('12 цифр ИИН'),
                'maxlength': '12'
            }),
            'institution_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Название университета/института')
            }),
            'institution_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Страна, где получено образование')
            }),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'specialty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Специальность по диплому')
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1950',
                'max': '2024' # Consider making this dynamic
            }),
            'duration_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Опишите цель признания документа')
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Дополнительные комментарии (необязательно)')
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h4 class="border-bottom pb-2 mb-4">{% trans "Личная информация" %}</h4>'),
            Row(
                Column('applicant_last_name', css_class='form-group col-md-4 mb-3'),
                Column('applicant_first_name', css_class='form-group col-md-4 mb-3'),
                Column('applicant_middle_name', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('applicant_email', css_class='form-group col-md-6 mb-3'),
                Column('applicant_phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('applicant_iin', css_class='mb-3'),
            
            HTML('<h4 class="border-bottom pb-2 mb-4 mt-4">{% trans "Информация об образовании" %}</h4>'),
            Field('institution_name', css_class='mb-3'),
            Row(
                Column('institution_country', css_class='form-group col-md-6 mb-3'),
                Column('education_level', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('specialty', css_class='mb-3'),
            Row(
                Column('graduation_year', css_class='form-group col-md-6 mb-3'),
                Column('duration_years', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('purpose', css_class='mb-3'),
            Field('notes', css_class='mb-3'),
            
            HTML('<h4 class="border-bottom pb-2 mb-4 mt-4">{% trans "Документы" %}</h4>'),
            HTML('<div class="alert alert-info"><i class="bi bi-info-circle"></i> {% trans "Загрузите все необходимые документы. Поддерживаемые форматы: PDF, JPG, PNG. Максимальный размер файла: 5MB." %}</div>'),
            Field('diploma_file', css_class='mb-3'),
            Field('transcript_file', css_class='mb-3'),
            Field('passport_file', css_class='mb-3'),
            Field('translation_file', css_class='mb-3'),
            
            HTML('<h4 class="border-bottom pb-2 mb-4 mt-4">{% trans "Подтверждение" %}</h4>'),
            Field('captcha', css_class='mb-3'),
            Field('data_processing_consent', css_class='mb-3'),
            
            Submit('submit', _('Подать заявку'), css_class='btn btn-primary btn-lg mt-3')
        )
    
    def clean_applicant_iin(self):
        """Валидация ИИН"""
        iin = self.cleaned_data.get('applicant_iin')
        if iin:
            if not re.match(r'^\d{12}$', iin):
                raise ValidationError(_('ИИН должен состоять из 12 цифр'))
            
            def validate_iin_checksum(iin_str):
                weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
                
                s = sum(int(iin_str[i]) * weights1[i] for i in range(11))
                k = s % 11
                
                if k < 10:
                    return k == int(iin_str[11])
                else:
                    s = sum(int(iin_str[i]) * weights2[i] for i in range(11))
                    k = s % 11
                    return k == int(iin_str[11]) if k < 10 else False # Added check for k < 10 for second pass
            
            if not validate_iin_checksum(iin):
                raise ValidationError(_('Некорректный ИИН'))
        
        return iin
    
    def clean_applicant_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('applicant_phone')
        if phone:
            phone_digits = re.sub(r'[^\d+]', '', phone)
            if not re.match(r'^\+?[78]\d{10}$', phone_digits): # KZ/RU phone format
                raise ValidationError(_('Введите корректный номер телефона (+7 XXX XXX XX XX)'))
        return phone
    
    def clean_graduation_year(self):
        """Валидация года окончания"""
        year = self.cleaned_data.get('graduation_year')
        if year:
            import datetime
            current_year = datetime.date.today().year
            if year < 1950 or year > current_year: # Adjusted min year
                raise ValidationError(
                    _('Год окончания должен быть между 1950 и %(current_year)s') 
                    % {'current_year': current_year}
                )
        return year
    
    def _validate_file(self, file_field_name, file_obj):
        """Общая валидация файлов (размер и расширение)"""
        if not file_obj:
            return
        
        if file_obj.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(
                _('Размер файла %(filename)s превышает максимально допустимый (%(max_size)sMB)') 
                % {'filename': file_obj.name, 'max_size': settings.MAX_UPLOAD_SIZE // (1024*1024)}
            )
        
        allowed_extensions = settings.ALLOWED_UPLOAD_EXTENSIONS
        file_extension = '.' + file_obj.name.lower().split('.')[-1]
        if file_extension not in allowed_extensions:
            raise ValidationError(
                _('Недопустимый тип файла: %(filename)s. Разрешены: %(allowed_types)s') %
                {'filename': file_obj.name, 'allowed_types': ", ".join(allowed_extensions)}
            )
        
    def clean_diploma_file(self):
        diploma_file = self.cleaned_data.get('diploma_file')
        self._validate_file('diploma_file', diploma_file)
        return diploma_file
    
    def clean_transcript_file(self):
        transcript_file = self.cleaned_data.get('transcript_file')
        self._validate_file('transcript_file', transcript_file)
        return transcript_file
    
    def clean_passport_file(self):
        passport_file = self.cleaned_data.get('passport_file')
        self._validate_file('passport_file', passport_file)
        return passport_file
    
    def clean_translation_file(self):
        translation_file = self.cleaned_data.get('translation_file')
        if translation_file: # Это поле необязательное
            self._validate_file('translation_file', translation_file)
        return translation_file
    
    def save(self, commit=True):
        """Сохранение заявки и документов"""
        application = super().save(commit=False) # commit=False, чтобы получить объект перед сохранением

        if self.request and self.request.user.is_authenticated: # Добавляем пользователя, если он есть
            application.user = self.request.user

        if commit:
            application.save() # Сохраняем саму заявку
            
            # Сохраняем документы
            document_mapping = {
                'diploma_file': 'diploma',
                'transcript_file': 'transcript',
                'passport_file': 'passport',
                'translation_file': 'translation',
            }
            
            for field_name, doc_type in document_mapping.items():
                file_obj = self.cleaned_data.get(field_name)
                if file_obj:
                    RecognitionDocument.objects.create(
                        application=application,
                        document_type=doc_type,
                        file=file_obj
                        # original_name и file_size будут установлены в RecognitionDocument.save()
                    )
            self.save_m2m() # Для ManyToMany полей, если они есть/появятся
        
        return application


class StatusCheckForm(forms.Form):
    """Форма проверки статуса заявки"""
    
    application_number = forms.CharField(
        max_length=20,
        label=_('Номер заявки'),
        help_text=_('Введите номер заявки в формате REC2024-00001'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Например: REC2024-00001')
        })
    )
    
    applicant_email = forms.EmailField(
        label=_('Email заявителя'),
        help_text=_('Email, указанный при подаче заявки'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@email.com')
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
            Field('application_number', css_class='mb-3'),
            Field('applicant_email', css_class='mb-3'),
            Field('captcha', css_class='mb-3'),
            Submit('submit', _('Проверить статус'), css_class='btn btn-primary')
        )
    
    def clean_application_number(self):
        """Валидация номера заявки"""
        number = self.cleaned_data.get('application_number')
        if number:
            if not re.match(r'^REC\d{4}-\d{5}$', number): # Example: REC2024-00001
                raise ValidationError(
                    _('Неверный формат номера заявки. Ожидается формат: RECГОД-НОМЕР (например, REC2024-00001)')
                )
        return number
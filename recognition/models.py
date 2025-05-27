from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os

User = get_user_model()


def upload_to_recognition(instance, filename):
    """Функция для определения пути загрузки файлов заявок на признание"""
    # Убедимся, что application существует и у него есть application_number
    if instance.application and instance.application.application_number:
        return f'recognition/{instance.application.application_number}/{filename}'
    # Резервный путь, если application_number еще не установлен (маловероятно при текущей логике сохранения)
    return f'recognition/unknown_application/{filename}'


class RecognitionApplication(models.Model):
    """Модель заявки на признание зарубежных документов об образовании"""
    
    STATUS_CHOICES = [
        ('draft', _('Черновик')),
        ('submitted', _('Подана')),
        ('in_review', _('На рассмотрении')),
        ('additional_docs_required', _('Требуются дополнительные документы')),
        ('approved', _('Одобрена')),
        ('rejected', _('Отклонена')),
        ('completed', _('Завершена')),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('bachelor', _('Бакалавриат')),
        ('master', _('Магистратура')),
        ('doctorate', _('Докторантура')),
        ('specialist', _('Специалитет')),
        ('other', _('Другое')),
    ]
    
    # Основная информация
    application_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name=_('Номер заявки'),
        help_text=_('Автоматически генерируется при создании')
    )
    status = models.CharField(
        max_length=30, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name=_('Статус')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    # Информация о заявителе
    applicant_first_name = models.CharField(max_length=100, verbose_name=_('Имя'))
    applicant_last_name = models.CharField(max_length=100, verbose_name=_('Фамилия'))
    applicant_middle_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_('Отчество')
    )
    applicant_email = models.EmailField(verbose_name=_('Email'))
    applicant_phone = models.CharField(max_length=20, verbose_name=_('Телефон'))
    applicant_iin = models.CharField(
        max_length=12, 
        verbose_name=_('ИИН'),
        help_text=_('Индивидуальный идентификационный номер')
    )
    
    # Информация об образовании
    institution_name = models.CharField(
        max_length=255, 
        verbose_name=_('Название учебного заведения')
    )
    institution_country = models.CharField(
        max_length=100, 
        verbose_name=_('Страна обучения')
    )
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name=_('Уровень образования')
    )
    specialty = models.CharField(
        max_length=255, 
        verbose_name=_('Специальность')
    )
    graduation_year = models.PositiveIntegerField(verbose_name=_('Год окончания'))
    duration_years = models.PositiveIntegerField(
        verbose_name=_('Продолжительность обучения (лет)')
    )
    
    # Дополнительная информация
    purpose = models.TextField(
        verbose_name=_('Цель признания'),
        help_text=_('Для чего нужно признание документа')
    )
    notes = models.TextField(
        blank=True, 
        verbose_name=_('Дополнительные комментарии')
    )
    
    # Связь с пользователем (если зарегистрирован)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Пользователь')
    )
    
    class Meta:
        verbose_name = _('Заявка на признание')
        verbose_name_plural = _('Заявки на признание')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application_number} - {self.applicant_last_name} {self.applicant_first_name}"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            # Генерируем номер заявки
            import datetime
            now = datetime.datetime.now()
            prefix = f"REC{now.year}"
            last_app = RecognitionApplication.objects.filter(
                application_number__startswith=prefix
            ).order_by('-id').first()
            
            if last_app:
                last_number = int(last_app.application_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.application_number = f"{prefix}-{new_number:05d}"
        
        super().save(*args, **kwargs)


class RecognitionDocument(models.Model):
    """Модель для хранения документов заявки на признание"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('diploma', _('Диплом')),
        ('transcript', _('Транскрипт/Приложение к диплому')),
        ('passport', _('Копия паспорта')),
        ('translation', _('Нотариальный перевод')),
        ('apostille', _('Апостиль')),
        ('other', _('Другой документ')),
    ]
    
    application = models.ForeignKey(
        RecognitionApplication, 
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Заявка')
    )
    document_type = models.CharField(
        max_length=20, 
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('Тип документа')
    )
    file = models.FileField(
        upload_to=upload_to_recognition,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name=_('Файл')
    )
    original_name = models.CharField(
        max_length=255, 
        verbose_name=_('Оригинальное имя файла')
    )
    file_size = models.PositiveIntegerField(verbose_name=_('Размер файла (байт)'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата загрузки'))
    description = models.TextField(
        blank=True, 
        verbose_name=_('Описание')
    )
    
    class Meta:
        verbose_name = _('Документ заявки')
        verbose_name_plural = _('Документы заявок')
        ordering = ['document_type', 'uploaded_at']
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.original_name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.original_name = os.path.basename(self.file.name)
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class RecognitionApplicationHistory(models.Model):
    """Модель для отслеживания истории изменений заявки"""
    
    application = models.ForeignKey(
        RecognitionApplication, 
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name=_('Заявка')
    )
    status_from = models.CharField(
        max_length=30, 
        choices=RecognitionApplication.STATUS_CHOICES,
        verbose_name=_('Статус "от"')
    )
    status_to = models.CharField(
        max_length=30, 
        choices=RecognitionApplication.STATUS_CHOICES,
        verbose_name=_('Статус "к"')
    )
    changed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_('Изменил')
    )
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата изменения'))
    comment = models.TextField(blank=True, verbose_name=_('Комментарий'))
    
    class Meta:
        verbose_name = _('История заявки')
        verbose_name_plural = _('История заявок')
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.application.application_number}: {self.status_from} → {self.status_to}"

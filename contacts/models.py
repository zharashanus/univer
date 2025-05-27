from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactMessage(models.Model):
    """Модель для сообщений обратной связи"""
    
    SUBJECT_CHOICES = [
        ('general', _('Общий вопрос')),
        ('recognition', _('Признание документов')),
        ('accreditation', _('Аккредитация')),
        ('technical', _('Техническая поддержка')),
        ('complaint', _('Жалоба')),
        ('suggestion', _('Предложение')),
        ('other', _('Другое')),
    ]
    
    STATUS_CHOICES = [
        ('new', _('Новое')),
        ('in_progress', _('В обработке')),
        ('answered', _('Отвечено')),
        ('closed', _('Закрыто')),
    ]
    
    # Основная информация
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_('Телефон')
    )
    subject = models.CharField(
        max_length=20, 
        choices=SUBJECT_CHOICES,
        verbose_name=_('Тема')
    )
    message = models.TextField(verbose_name=_('Сообщение'))
    
    # Дополнительная информация
    organization = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name=_('Организация')
    )
    
    # Служебная информация
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name=_('Статус')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        verbose_name=_('IP адрес')
    )
    user_agent = models.TextField(
        blank=True, 
        verbose_name=_('User Agent')
    )
    
    # Связь с пользователем (если зарегистрирован)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Пользователь')
    )
    
    # Ответ администратора
    admin_response = models.TextField(
        blank=True, 
        verbose_name=_('Ответ администратора')
    )
    responded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='responded_messages',
        verbose_name=_('Ответил')
    )
    responded_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name=_('Дата ответа')
    )
    
    class Meta:
        verbose_name = _('Сообщение обратной связи')
        verbose_name_plural = _('Сообщения обратной связи')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"


class FAQ(models.Model):
    """Модель для часто задаваемых вопросов"""
    
    CATEGORY_CHOICES = [
        ('general', _('Общие вопросы')),
        ('recognition', _('Признание документов')),
        ('accreditation', _('Аккредитация')),
        ('procedures', _('Процедуры')),
        ('documents', _('Документы')),
        ('fees', _('Оплата')),
    ]
    
    question = models.TextField(verbose_name=_('Вопрос'))
    answer = models.TextField(verbose_name=_('Ответ'))
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        verbose_name=_('Категория')
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('Порядок отображения')
    )
    is_published = models.BooleanField(
        default=True, 
        verbose_name=_('Опубликовано')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    class Meta:
        verbose_name = _('Часто задаваемый вопрос')
        verbose_name_plural = _('Часто задаваемые вопросы')
        ordering = ['category', 'order', 'question']
    
    def __str__(self):
        return self.question[:100]

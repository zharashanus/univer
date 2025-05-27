from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class SiteSettings(models.Model):
    """Настройки сайта"""
    site_name = models.CharField(_('Название сайта'), max_length=200, default='ENIC Kazakhstan')
    site_description = models.TextField(_('Описание сайта'), blank=True)
    site_keywords = models.TextField(_('Ключевые слова'), blank=True)
    contact_email = models.EmailField(_('Email для связи'), blank=True)
    contact_phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    address = models.TextField(_('Адрес'), blank=True)
    working_hours = models.TextField(_('Часы работы'), blank=True)
    
    # Социальные сети
    facebook_url = models.URLField(_('Facebook'), blank=True)
    instagram_url = models.URLField(_('Instagram'), blank=True)
    youtube_url = models.URLField(_('YouTube'), blank=True)
    telegram_url = models.URLField(_('Telegram'), blank=True)
    
    # Логотипы
    logo = models.ImageField(_('Логотип'), upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(
        _('Favicon'), 
        upload_to='logos/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['ico', 'png'])]
    )
    
    # Настройки отображения
    enable_chat_bot = models.BooleanField(_('Включить чат-бот'), default=False)
    enable_calculator = models.BooleanField(_('Включить калькулятор'), default=True)
    enable_search = models.BooleanField(_('Включить поиск'), default=True)
    
    # Версия для слабовидящих
    enable_accessibility = models.BooleanField(_('Включить версию для слабовидящих'), default=True)
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Настройки сайта')
        verbose_name_plural = _('Настройки сайта')
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            # Разрешаем только одну запись настроек
            raise ValueError('Может существовать только одна запись настроек сайта')
        return super().save(*args, **kwargs)


class SEOSettings(models.Model):
    """SEO настройки для страниц"""
    page_name = models.CharField(_('Название страницы'), max_length=100, unique=True)
    meta_title = models.CharField(_('Meta Title'), max_length=60, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.TextField(_('Meta Keywords'), blank=True)
    og_title = models.CharField(_('Open Graph Title'), max_length=60, blank=True)
    og_description = models.CharField(_('Open Graph Description'), max_length=160, blank=True)
    og_image = models.ImageField(_('Open Graph Image'), upload_to='seo/', blank=True, null=True)
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('SEO настройки')
        verbose_name_plural = _('SEO настройки')
    
    def __str__(self):
        return self.page_name


class FAQ(models.Model):
    """Часто задаваемые вопросы"""
    question = models.CharField(_('Вопрос'), max_length=500)
    answer = models.TextField(_('Ответ'))
    category = models.CharField(_('Категория'), max_length=100, blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Часто задаваемый вопрос')
        verbose_name_plural = _('Часто задаваемые вопросы')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question[:100]


class Translation(models.Model):
    """Переводы для динамических текстов"""
    key = models.CharField(_('Ключ'), max_length=100, unique=True)
    value_kk = models.TextField(_('Значение (казахский)'), blank=True)
    value_ru = models.TextField(_('Значение (русский)'), blank=True)
    value_en = models.TextField(_('Значение (английский)'), blank=True)
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Перевод')
        verbose_name_plural = _('Переводы')
    
    def __str__(self):
        return self.key
    
    def get_value(self, language='kk'):
        """Получить значение для определенного языка"""
        if language == 'kk':
            return self.value_kk
        elif language == 'ru':
            return self.value_ru
        elif language == 'en':
            return self.value_en
        return self.value_kk  # По умолчанию казахский


class Breadcrumb(models.Model):
    """Хлебные крошки для навигации"""
    page_url = models.CharField(_('URL страницы'), max_length=200, unique=True)
    title = models.CharField(_('Заголовок'), max_length=100)
    parent_url = models.CharField(_('URL родительской страницы'), max_length=200, blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    
    class Meta:
        verbose_name = _('Хлебная крошка')
        verbose_name_plural = _('Хлебные крошки')
    
    def __str__(self):
        return f"{self.page_url} - {self.title}" 
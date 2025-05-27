from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    
    USER_TYPES = (
        ('applicant', _('Заявитель')),
        ('moderator', _('Модератор')),
        ('admin', _('Администратор')),
    )
    
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(
        _('Телефон'), 
        max_length=20, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_('Номер телефона должен быть в формате: "+999999999". До 15 цифр.')
        )]
    )
    user_type = models.CharField(_('Тип пользователя'), max_length=20, choices=USER_TYPES, default='applicant')
    
    # Дополнительные поля
    middle_name = models.CharField(_('Отчество'), max_length=150, blank=True)
    birth_date = models.DateField(_('Дата рождения'), blank=True, null=True)
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', blank=True, null=True)
    
    # Контактная информация
    organization = models.CharField(_('Организация'), max_length=255, blank=True)
    position = models.CharField(_('Должность'), max_length=100, blank=True)
    country = models.CharField(_('Страна'), max_length=100, blank=True)
    city = models.CharField(_('Город'), max_length=100, blank=True)
    address = models.TextField(_('Адрес'), blank=True)
    
    # Предпочтения
    preferred_language = models.CharField(
        _('Предпочитаемый язык'), 
        max_length=2, 
        choices=[('kk', 'Қазақша'), ('ru', 'Русский'), ('en', 'English')],
        default='kk'
    )
    receive_notifications = models.BooleanField(_('Получать уведомления'), default=True)
    receive_newsletter = models.BooleanField(_('Получать рассылку'), default=False)
    
    # Метаданные
    email_verified = models.BooleanField(_('Email подтвержден'), default=False)
    phone_verified = models.BooleanField(_('Телефон подтвержден'), default=False)
    last_login_ip = models.GenericIPAddressField(_('IP последнего входа'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}".strip()
    
    def get_short_name(self):
        """Возвращает краткое имя пользователя"""
        return self.first_name
    
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором"""
        return self.user_type == 'moderator' or self.is_staff
    
    def is_admin_user(self):
        """Проверяет, является ли пользователь администратором"""
        return self.user_type == 'admin' or self.is_superuser


class UserProfile(models.Model):
    """Дополнительная информация профиля пользователя"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Дополнительная персональная информация
    iin = models.CharField(_('ИИН'), max_length=12, blank=True, unique=True, null=True)
    passport_number = models.CharField(_('Номер паспорта'), max_length=20, blank=True)
    nationality = models.CharField(_('Национальность'), max_length=50, blank=True)
    
    # Образование
    education_level = models.CharField(
        _('Уровень образования'),
        max_length=50,
        choices=[
            ('secondary', _('Среднее')),
            ('higher', _('Высшее')),
            ('postgraduate', _('Послевузовское')),
        ],
        blank=True
    )
    university = models.CharField(_('Университет'), max_length=255, blank=True)
    graduation_year = models.PositiveIntegerField(_('Год окончания'), blank=True, null=True)
    
    # Статистика
    applications_count = models.PositiveIntegerField(_('Количество заявок'), default=0)
    last_activity = models.DateTimeField(_('Последняя активность'), auto_now=True)
    
    # Настройки конфиденциальности
    profile_visibility = models.CharField(
        _('Видимость профиля'),
        max_length=20,
        choices=[
            ('public', _('Публичный')),
            ('private', _('Приватный')),
        ],
        default='private'
    )
    
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
    
    def __str__(self):
        return f"Профиль {self.user.get_full_name()}"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Профиль пользователя')
    fields = [
        ('iin', 'passport_number'),
        'nationality',
        ('education_level', 'university', 'graduation_year'),
        ('applications_count', 'profile_visibility'),
    ]


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    
    list_display = [
        'email', 'get_full_name', 'user_type', 'is_active', 
        'email_verified', 'date_joined'
    ]
    list_filter = [
        'user_type', 'is_active', 'is_staff', 'email_verified', 
        'preferred_language', 'date_joined'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'username', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Персональная информация'), {
            'fields': (
                ('first_name', 'last_name', 'middle_name'),
                ('phone', 'birth_date'),
                'avatar',
            )
        }),
        (_('Контактная информация'), {
            'fields': (
                ('organization', 'position'),
                ('country', 'city'),
                'address',
            )
        }),
        (_('Предпочтения'), {
            'fields': (
                'preferred_language',
                ('receive_notifications', 'receive_newsletter'),
            )
        }),
        (_('Разрешения'), {
            'fields': (
                'user_type',
                ('is_active', 'is_staff', 'is_superuser'),
                'groups',
                'user_permissions',
            )
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined')
        }),
        (_('Верификация'), {
            'fields': (
                ('email_verified', 'phone_verified'),
                'last_login_ip',
            )
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'password1', 'password2', 'user_type'
            ),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'last_login_ip']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Полное имя')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'iin', 'education_level', 'university', 
        'applications_count', 'last_activity'
    ]
    list_filter = [
        'education_level', 'profile_visibility', 'created_at'
    ]
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'iin', 'passport_number', 'university'
    ]
    readonly_fields = ['applications_count', 'last_activity', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('user',)
        }),
        (_('Документы'), {
            'fields': (
                ('iin', 'passport_number'),
                'nationality',
            )
        }),
        (_('Образование'), {
            'fields': (
                'education_level',
                ('university', 'graduation_year'),
            )
        }),
        (_('Статистика'), {
            'fields': (
                'applications_count',
                'last_activity',
            )
        }),
        (_('Настройки'), {
            'fields': ('profile_visibility',)
        }),
        (_('Системная информация'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

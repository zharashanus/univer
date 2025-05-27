from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, SEOSettings, FAQ, Translation, Breadcrumb


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone', 'updated_at']
    fields = [
        ('site_name', 'site_description'),
        'site_keywords',
        ('contact_email', 'contact_phone'),
        'address',
        'working_hours',
        ('facebook_url', 'instagram_url'),
        ('youtube_url', 'telegram_url'),
        ('logo', 'favicon'),
        ('enable_chat_bot', 'enable_calculator', 'enable_search'),
        'enable_accessibility',
    ]
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если нет записей
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление
        return False


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'meta_title', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['page_name', 'meta_title', 'meta_keywords']
    fields = [
        'page_name',
        ('meta_title', 'meta_description'),
        'meta_keywords',
        ('og_title', 'og_description'),
        'og_image',
    ]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'category']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-created_at']
    
    def question_short(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = _('Вопрос')
    
    fields = [
        'question',
        'answer',
        ('category', 'order'),
        'is_active',
    ]


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_kk_short', 'value_ru_short', 'value_en_short', 'updated_at']
    search_fields = ['key', 'value_kk', 'value_ru', 'value_en']
    list_filter = ['created_at', 'updated_at']
    
    def value_kk_short(self, obj):
        return obj.value_kk[:30] + '...' if len(obj.value_kk) > 30 else obj.value_kk
    value_kk_short.short_description = _('Казахский (короткий)')
    
    def value_ru_short(self, obj):
        return obj.value_ru[:30] + '...' if len(obj.value_ru) > 30 else obj.value_ru
    value_ru_short.short_description = _('Русский (короткий)')
    
    def value_en_short(self, obj):
        return obj.value_en[:30] + '...' if len(obj.value_en) > 30 else obj.value_en
    value_en_short.short_description = _('Английский (короткий)')
    
    fields = [
        'key',
        'value_kk',
        'value_ru',
        'value_en',
    ]


@admin.register(Breadcrumb)
class BreadcrumbAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'title', 'parent_url', 'is_active']
    list_filter = ['is_active']
    search_fields = ['page_url', 'title']
    list_editable = ['is_active']
    
    fields = [
        ('page_url', 'title'),
        'parent_url',
        'is_active',
    ] 
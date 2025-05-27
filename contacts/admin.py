from django.contrib import admin
from .models import ContactMessage, FAQ


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('name', 'email', 'message', 'admin_response')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent', 'user')
    fieldsets = (
        (None, {
            'fields': ('status', 'subject', 'name', 'email', 'phone', 'organization')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Ответ администратора', {
            'classes': ('collapse',), # Скрыто по умолчанию
            'fields': ('admin_response', 'responded_by', 'responded_at')
        }),
        ('Служебная информация', {
            'classes': ('collapse',), 
            'fields': ('user', 'ip_address', 'user_agent', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """При сохранении ответа администратора, устанавливаем responded_by и responded_at"""
        if obj.admin_response and not obj.responded_by:
            obj.responded_by = request.user
            from django.utils import timezone
            obj.responded_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_published', 'updated_at')
    list_filter = ('category', 'is_published')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_published')
    ordering = ('category', 'order')

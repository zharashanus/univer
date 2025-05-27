from django.contrib import admin
from .models import RecognitionApplication, RecognitionDocument, RecognitionApplicationHistory


@admin.register(RecognitionApplication)
class RecognitionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'application_number', 'applicant_last_name', 'applicant_first_name', 
        'education_level', 'status', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'education_level', 'created_at')
    search_fields = (
        'application_number', 'applicant_last_name', 'applicant_first_name', 
        'applicant_email', 'applicant_iin', 'institution_name'
    )
    readonly_fields = ('application_number', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('application_number', 'status')
        }),
        ('Информация о заявителе', {
            'fields': (
                ('applicant_last_name', 'applicant_first_name', 'applicant_middle_name'),
                'applicant_email', 'applicant_phone', 'applicant_iin', 'user'
            )
        }),
        ('Информация об образовании', {
            'fields': (
                'institution_name', 'institution_country', 'education_level',
                'specialty', 'graduation_year', 'duration_years'
            )
        }),
        ('Дополнительная информация', {
            'fields': ('purpose', 'notes')
        }),
        ('Даты', {
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    # Можно добавить инлайн для документов и истории
    # inlines = [RecognitionDocumentInline, RecognitionApplicationHistoryInline]

@admin.register(RecognitionDocument)
class RecognitionDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'original_name', 'file_size', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('application__application_number', 'original_name')
    readonly_fields = ('original_name', 'file_size', 'uploaded_at')


@admin.register(RecognitionApplicationHistory)
class RecognitionApplicationHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'status_from', 'status_to', 'changed_by', 'changed_at')
    list_filter = ('status_to', 'changed_at')
    search_fields = ('application__application_number', 'comment')
    readonly_fields = ('changed_at',)

# TODO: Определить инлайн классы, если они нужны:
# class RecognitionDocumentInline(admin.TabularInline):
#     model = RecognitionDocument
#     extra = 1 # Количество пустых форм для добавления
#     readonly_fields = ('original_name', 'file_size', 'uploaded_at')

# class RecognitionApplicationHistoryInline(admin.TabularInline):
#     model = RecognitionApplicationHistory
#     extra = 0
#     readonly_fields = ('status_from', 'status_to', 'changed_by', 'changed_at', 'comment')
#     can_delete = False
#     max_num = 0 # Запретить добавление через инлайн, только просмотр

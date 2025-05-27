from django.conf import settings
from django.utils.translation import gettext as _

def site_settings(request):
    """
    Добавляет основные настройки сайта во все шаблоны
    """
    return {
        'SITE_NAME': 'ENIC Kazakhstan',
        'SITE_DESCRIPTION': _('Национальный центр развития высшего образования'),
        'CONTACT_EMAIL': 'info@enic-kazakhstan.edu.kz',
        'CONTACT_PHONE': '+7 (727) 123-45-67',
        'CONTACT_ADDRESS': _('г. Алматы, ул. Пример, 123'),
        'SOCIAL_LINKS': {
            'facebook': '#',
            'twitter': '#',
            'linkedin': '#',
            'youtube': '#',
        },
        'WORKING_HOURS': _('Пн-Пт: 9:00-18:00'),
        'DEBUG': settings.DEBUG,
    } 
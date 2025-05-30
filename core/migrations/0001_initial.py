# Generated by Django 4.2.7 on 2025-05-27 09:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breadcrumb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.CharField(max_length=200, unique=True, verbose_name='URL страницы')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('parent_url', models.CharField(blank=True, max_length=200, verbose_name='URL родительской страницы')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Хлебная крошка',
                'verbose_name_plural': 'Хлебные крошки',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('category', models.CharField(blank=True, max_length=100, verbose_name='Категория')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Часто задаваемый вопрос',
                'verbose_name_plural': 'Часто задаваемые вопросы',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='SEOSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=100, unique=True, verbose_name='Название страницы')),
                ('meta_title', models.CharField(blank=True, max_length=60, verbose_name='Meta Title')),
                ('meta_description', models.CharField(blank=True, max_length=160, verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, verbose_name='Meta Keywords')),
                ('og_title', models.CharField(blank=True, max_length=60, verbose_name='Open Graph Title')),
                ('og_description', models.CharField(blank=True, max_length=160, verbose_name='Open Graph Description')),
                ('og_image', models.ImageField(blank=True, null=True, upload_to='seo/', verbose_name='Open Graph Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'SEO настройки',
                'verbose_name_plural': 'SEO настройки',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='ENIC Kazakhstan', max_length=200, verbose_name='Название сайта')),
                ('site_description', models.TextField(blank=True, verbose_name='Описание сайта')),
                ('site_keywords', models.TextField(blank=True, verbose_name='Ключевые слова')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Email для связи')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('address', models.TextField(blank=True, verbose_name='Адрес')),
                ('working_hours', models.TextField(blank=True, verbose_name='Часы работы')),
                ('facebook_url', models.URLField(blank=True, verbose_name='Facebook')),
                ('instagram_url', models.URLField(blank=True, verbose_name='Instagram')),
                ('youtube_url', models.URLField(blank=True, verbose_name='YouTube')),
                ('telegram_url', models.URLField(blank=True, verbose_name='Telegram')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/', verbose_name='Логотип')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='logos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'png'])], verbose_name='Favicon')),
                ('enable_chat_bot', models.BooleanField(default=False, verbose_name='Включить чат-бот')),
                ('enable_calculator', models.BooleanField(default=True, verbose_name='Включить калькулятор')),
                ('enable_search', models.BooleanField(default=True, verbose_name='Включить поиск')),
                ('enable_accessibility', models.BooleanField(default=True, verbose_name='Включить версию для слабовидящих')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='Ключ')),
                ('value_kk', models.TextField(blank=True, verbose_name='Значение (казахский)')),
                ('value_ru', models.TextField(blank=True, verbose_name='Значение (русский)')),
                ('value_en', models.TextField(blank=True, verbose_name='Значение (английский)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Перевод',
                'verbose_name_plural': 'Переводы',
            },
        ),
    ]

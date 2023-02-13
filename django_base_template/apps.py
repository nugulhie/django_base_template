from django.apps import AppConfig


class DjangoBaseTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_base_template'

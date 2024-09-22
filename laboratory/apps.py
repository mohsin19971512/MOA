from django.apps import AppConfig


class LaboratoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laboratory'
    verbose_name = 'اعدادات المختبرات'
    def ready(self):
        import laboratory.signals
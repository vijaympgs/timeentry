from django.apps import AppConfig


class HrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrm'
    verbose_name = 'HRM'
    
    def ready(self):
        # Import admin modules to register models
        import hrm.admin

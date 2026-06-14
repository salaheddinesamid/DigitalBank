from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_management'

    def ready(self):
        from .initializers.initialize_roles import test_roles
        test_roles()
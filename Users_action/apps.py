from django.apps import AppConfig


class UsersActionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users_action'
    def ready(self):
        import Users_action.signals
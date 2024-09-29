from django.apps import AppConfig
from .json_updater import JsonUpdater

class MapConfig(AppConfig):
    name = 'map'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # Start the JSON updater when the app is ready
        self.json_updater = JsonUpdater()
        self.json_updater.start()

# Import Django's base AppConfig class
from django.apps import AppConfig


# Define configuration class for the 'streaming' application
class StreamingConfig(AppConfig):
    # Specify the primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    # Set the name of the application
    name = 'streaming'

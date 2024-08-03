"""apps.py

This file defines the configuration for the Django app. It specifies the app's name 
and default settings for model fields, ensuring consistent behavior across the app.
"""

# Import AppConfig to define the configuration of the Django app.
from django.apps import AppConfig

class MainAppConfig(AppConfig):
    """Configuration class for a Django application. It defines application-specific settings 
    such as the app's name and default settings for auto-generated model fields.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

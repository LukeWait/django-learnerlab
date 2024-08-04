"""admin.py

This file configures the Django admin interface for your application. It registers models (database tables) with the admin panel, 
allowing you to manage them easily. By registering your models, you enable the admin interface to provide functionality for 
creating, reading, updating, and deleting (CRUD) data.

When using Django's built-in User and Group models, these models are automatically available in the admin panel. 
If you are using custom user or group models, you will need to register those as well to manage them through the admin interface.
"""

# Import the 'admin' module to register models for the Django admin interface.
from django.contrib import admin

# Import the models defined in the 'models.py' file for this app (main_app).
from .models import RecordLabel, Musician, Album

# Register your models here to make them available in the Django admin interface.
# This allows you to manage these models through the built-in admin panel.
admin.site.register(RecordLabel)
admin.site.register(Musician)
admin.site.register(Album)

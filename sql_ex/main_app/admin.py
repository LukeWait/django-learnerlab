""" admin.py

This file configures the Django admin interface for your application. It is used to register 
models (database tables) so they can be managed through the admin panel, enabling easy creation, 
reading, updating, and deletion (CRUD) of data.
"""

# Import the admin module to register models for the Django admin interface.
from django.contrib import admin

# Import the models defined in the models.py file for this app (main_app).
from .models import RecordLabel, Musician, Album

# Register your models here to make them available in the Django admin interface.
# This allows you to manage these models through the built-in admin panel.
admin.site.register(RecordLabel)
admin.site.register(Musician)
admin.site.register(Album)

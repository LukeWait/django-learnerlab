"""models.py

This file defines the database models for the Django app.
Each model represents a table in the database, with fields corresponding to columns.
Models establish the structure of the database and define relationships between different types of data.

When using Django's default database (SQLite), there is no need to explicitly define the User and Group authentication models, 
as Django manages them internally. However, if you choose to use an external database, you must declare the User and Group 
models in this file to ensure they are properly mapped and managed within your application.
"""

# Import 'models' from Django's ORM to define the database schema and create database tables.
from django.db import models

# Create your models here - this project doesn't use models or the admin portal, so this file can be ignored in this setup.

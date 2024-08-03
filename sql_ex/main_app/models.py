"""models.py

This file defines the database models for the Django app.
Each model represents a table in the database, with fields corresponding to columns.
Models establish the structure of the database and define relationships between different types of data.
"""

# Import models from Django's ORM to define the database schema and create database tables.
from django.db import models

# OPTIONAL: Import User from the Django auth model to associate data entries with specific users.
# This enables user-based data management, allowing control over who can view or modify data in views.py and API views.
from django.contrib.auth.models import User

class RecordLabel(models.Model):
    """Example model representing a record label.
    """
    name = models.CharField('Label Name', max_length=100)
    address = models.CharField('Address', max_length=300)
    email = models.EmailField('Contact Email')
    
    def __str__(self):
        """Returns a string representation of the model,
        typically used in the Django admin site
        """
        return self.name

class Musician(models.Model):
    """Example model representing a musician.
    """
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    instrument = models.CharField('Instrument', max_length=50)
    # The agent field creates a ForeignKey relationship to the PrimaryKey (id) of the User model.
    # This links each musician to the id of a specific user (agent) who manages them.
    agent = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        """Returns a string representation of the model,
        typically used in the Django admin site
        """
        return f"{self.first_name} {self.last_name} ({self.instrument})"

class Album(models.Model):
    """Example model representing a music album.
    """
    title = models.CharField('Album Title', max_length=200)
    artist = models.CharField('Artist', max_length=200)
    release_date = models.DateField('Release Date')
    genre = models.CharField('Genre', max_length=100)
    # The label field creates a ForeignKey relationship to the PrimaryKey (id) of the RecordLabel model.
    # This links each album to the id of a specific record label.
    label = models.ForeignKey(RecordLabel, on_delete=models.CASCADE, verbose_name='Record Label')
    # The album_members field creates a ManyToManyField relationship to the Musician model.
    # This allows each album to have multiple musicians, and each musician to be part of multiple albums.
    # Django automatically creates a linking table using the id fields from corresponding tables (Album and Musician).
    album_members = models.ManyToManyField(Musician, blank=True, verbose_name='Album Members')

    def __str__(self):
        """Returns a string representation of the model,
        typically used in the Django admin site
        """
        return f"{self.artist}: {self.title}"

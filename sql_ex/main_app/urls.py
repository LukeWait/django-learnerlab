"""urls.py

This file defines the URL patterns for the Django application, mapping URL paths to their corresponding views. 
This allows users to access various functionalities of the app through specific routes. 
It is referenced by the main project's URL configuration (config/urls.py) and serves to extend the base URL patterns defined there, 
enabling more granular control over the application's routing, such as handling API endpoints and views specific to the app.
"""

# Import path from Django's URL dispatcher to define URL patterns and map them to specific views.
from django.urls import path

# Import all views from views.py to utilize specific functions and classes for handling requests and responses.
from . import views

# URL patterns define the routes for the application, mapping specific URL paths to their corresponding view functions.
# Remember the base URL is defined in config/urls.py (main_app/), so these serve as an extention to that.
# For example: http://<your-ip>:8000/main_app/recordlabel, or http://<your-ip>:8000/main_app/musicians/3
urlpatterns = [
    path('',views.index,name='index'),
    path('recordlabel', views.RecordLabelListApiView.as_view()),
    path('musicians/', views.MusicianListApiView.as_view()),
    path('musicians/<int:musician_id>/', views.MusicianDetailApiView.as_view()),
    path('musicians/', views.AlbumListApiView.as_view()),
]
"""urls.py

This file defines the URL patterns for the Django application, mapping URL paths to their corresponding views.
It extends the base URL patterns defined in the main project's URL configuration (config/urls.py).
Each URL pattern is considered an endpoint (or API endpoint for API views), providing specific routes to access the app's functionalities.
"""

# Import 'path' from Django's URL dispatcher to define URL patterns and map them to specific views.
from django.urls import path
# Import all views from 'views.py' to utilize specific functions and classes for handling requests and responses.
from . import views

# URL patterns define the routes for the application, mapping specific URL paths to their corresponding view functions.
# The base URL is defined in 'config/urls.py' (main_app/), so these serve as an extension to that.
# For example when using 'python manage.py runserver 10.0.0.42:8000' -> http://10.0.0.42:8000/main_app/api/recordlabel/
urlpatterns = [
    # Endpoints - represent routes in the application that provide access to various client-facing views, such as web pages or forms.
    path('', views.index, name='index'),
    # API endpoints - represent routes that allow programmatic access to the application's backend functionalities, 
    # enabling clients to interact with the data through HTTP requests.
    path('api/recordlabel/', views.RecordLabelListApiView.as_view()),
    path('api/musician/', views.MusicianListApiView.as_view()),
    path('api/musician/<int:musician_id>/', views.MusicianDetailApiView.as_view()),
    path('api/album/', views.AlbumListApiView.as_view()),
]

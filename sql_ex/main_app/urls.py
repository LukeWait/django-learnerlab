from django.urls import path
from .views import (
    RecordLabelListApiView, 
    MusicianListApiView,
    MusicianDetailApiView,
    AlbumListApiView
)
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('recordlabel', RecordLabelListApiView.as_view()),  # Default path for listing and creating record labels
    path('musicians/', MusicianListApiView.as_view()),  # Path for listing and creating musicians
    path('musicians/<int:musician_id>/', MusicianDetailApiView.as_view()),  # Path for retrieving, updating, and deleting a specific musician
    path('musicians/', AlbumListApiView.as_view()),  # Path for listing and creating albums
]
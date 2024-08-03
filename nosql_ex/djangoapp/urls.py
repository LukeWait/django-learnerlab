from django.urls import path
from .views import TheModelView

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('themodel/', TheModelView)
    ]
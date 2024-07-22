from django.urls import path
from djangoapp.views import TheModelView

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('themodel/', TheModelView)
    ]
from django.urls import path
from .views import RecordLabelListApiView, RecordLabelDetailApiView

urlpatterns = [
    path('', RecordLabelListApiView.as_view()),  # Default path for listing and creating todos
    path('<int:todo_id>/', RecordLabelDetailApiView.as_view()),  # Path for retrieving, updating, and deleting a specific todo
]
from django.urls import path
from .views import TodoListApiView, TodoDetailApiView

urlpatterns = [
    path('', TodoListApiView.as_view()),  # Default path for listing and creating todos
    path('<int:todo_id>/', TodoDetailApiView.as_view()),  # Path for retrieving, updating, and deleting a specific todo
]
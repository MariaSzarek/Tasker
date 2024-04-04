from django.urls import include, path
from rest_framework import routers
from .views import Task_todoListView, Task_todoItemView

urlpatterns = [
    path('tasker/', Task_todoListView.as_view()),
    path('tasker/<int:pk>/', Task_todoItemView.as_view()),
    ]

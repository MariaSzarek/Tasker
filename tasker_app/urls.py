from django.urls import include, path, re_path
from rest_framework import routers
from .views import Task_todoListView, Task_todoItemView, signup, login, test_token, logout
from .views import VerifyEmail

urlpatterns = [
    path('signup/', signup),
    re_path('login', login),
    re_path('logout', logout),
    re_path('test_token', test_token),
    path('tasker/', Task_todoListView.as_view()),
    path('tasker/<int:pk>/', Task_todoItemView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify')
    ]

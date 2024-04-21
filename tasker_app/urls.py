from django.urls import include, path, re_path
from rest_framework import routers
from .views import Task_todoListView, Task_todoItemView, signup, login, test_token, logout
from .views import VerifyEmail


from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('api_schema/', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api_schema'),
    path('signup/', signup),
    re_path('login', login),
    re_path('logout', logout),
    re_path('test_token', test_token),
    path('tasker/', Task_todoListView.as_view()),
    path('tasker/<int:pk>/', Task_todoItemView.as_view()),
    path('activation-confirmed/', VerifyEmail.as_view(), name='activation-confirmed')

    ]

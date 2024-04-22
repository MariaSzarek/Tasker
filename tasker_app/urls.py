from django.urls import path, re_path
from .views import Task_todoListView, Task_todoItemView, signup, login, logout
from .views import VerifyEmail
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('api_schema/', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api_schema'),
    path('docs/', TemplateView.as_view(template_name='docs.html', extra_context={'schema_url': 'api_schema'}), name='swagger-ui'),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('tasker/', Task_todoListView.as_view()),
    path('tasker/<int:pk>/', Task_todoItemView.as_view()),
    path('activation-confirmed/', VerifyEmail.as_view(), name='activation-confirmed')
    ]

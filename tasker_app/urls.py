from django.urls import path
from .views import Full_Task_todoListView, Task_todoItemView, signup, login, logout, Short_Task_todoListView
from .views import VerifyEmail
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api_schema/', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api_schema'),
    path('docs/', TemplateView.as_view(template_name='docs.html', extra_context={'schema_url': 'api_schema'}), name='swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signup),
    path('signup/activation-confirmed/', VerifyEmail.as_view(), name='activation-confirmed'),
    path('login/', login),
    path('logout/', logout),
    path('task_todo/', Full_Task_todoListView.as_view(), name='task_todo'),
    path('task_todo/<int:pk>/', Task_todoItemView.as_view(), name='task_todo_detail'),
    path('short_task_todo/', Short_Task_todoListView.as_view(), name='short_task_todo')
    ]

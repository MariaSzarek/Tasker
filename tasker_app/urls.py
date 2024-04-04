from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# router.register('tasker', views.Task_todoView)


from .views import Task_todoListView, Task_todoItemView

urlpatterns = [
    path('', include(router.urls)),
    path('tasker/', Task_todoListView.as_view()),
    path('tasker/<int:pk>/', Task_todoItemView.as_view()),
    ]
#
# urlpatterns = [
#     path('tasker/', Task_todoListView.as_view()),
#     path('tasker/<int:pk>/', Task_todoDetailView.as_view())
# ]
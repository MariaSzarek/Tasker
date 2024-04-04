from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('tasker', views.Task_todoView)

urlpatterns = [
    path('', include(router.urls)),

    ]
#
# urlpatterns = [
#     path('tasker/', Task_todoListView.as_view()),
#     path('tasker/<int:pk>/', Task_todoDetailView.as_view())
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import EmployeeViewSet

router = DefaultRouter()

router.register('employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('api/', include(router.urls)),
]

"""
URL configuration for Organization Chart and Employee Directory APIs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.organization_views import (
    OrganizationChartViewSet,
    EmployeeDirectoryViewSet
)
from ..views.employee import EmployeeRecordViewSet

# Create router for organization APIs
router = DefaultRouter()
router.register(r'organization-chart', OrganizationChartViewSet, basename='organization-chart')
router.register(r'employee-directory', EmployeeDirectoryViewSet, basename='employee-directory')
router.register(r'employees', EmployeeRecordViewSet, basename='employees')

app_name = 'organization'

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DepartmentViewSet
from .views.organizational_unit import OrganizationalChartViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'organizational-chart', OrganizationalChartViewSet, basename='organizational-chart')

urlpatterns = [
    path('', include(router.urls)),
]

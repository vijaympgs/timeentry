"""HRM API URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.employee import EmployeeRecordViewSet
from .views.toolbar_config import ToolbarConfigView
from .views.toolbar_permissions import get_toolbar_permissions, list_toolbar_permissions, get_user_toolbar_permissions
from .urls.profile_view import urlpatterns as profile_view_urls

# Create router for API endpoints
router = DefaultRouter()
router.register(r'employees', EmployeeRecordViewSet, basename='employee')

urlpatterns = [
    # API endpoints
    path('api/v1/', include(router.urls)),
    
    # Profile View endpoints (Layer 3: Experience/Enrichment Layer)
    path('', include(profile_view_urls)),
    
    # Toolbar configuration endpoint
    path('api/toolbar-config/<str:view_id>/', ToolbarConfigView.as_view(), name='toolbar-config'),
    
    # Toolbar permissions endpoint (v2.0 API-driven)
    path('api/toolbar-permissions/', get_toolbar_permissions, name='toolbar-permissions'),
    path('api/toolbar-permissions/list/', list_toolbar_permissions, name='toolbar-permissions-list'),
    path('api/toolbar-permissions/user/', get_user_toolbar_permissions, name='user-toolbar-permissions'),
]

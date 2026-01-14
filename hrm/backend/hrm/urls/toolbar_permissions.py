"""
Toolbar Permissions URLs

URL configuration for v2.0 API-driven toolbar permission system.
"""

from django.urls import path
from ..views.toolbar_permissions import (
    get_toolbar_permissions, 
    list_toolbar_permissions, 
    get_user_toolbar_permissions
)

urlpatterns = [
    # Main toolbar permissions endpoint
    path('', get_toolbar_permissions, name='toolbar-permissions'),
    
    # List all toolbar configurations
    path('list/', list_toolbar_permissions, name='toolbar-permissions-list'),
    
    # User-specific toolbar permissions (requires authentication)
    path('user/', get_user_toolbar_permissions, name='user-toolbar-permissions'),
]

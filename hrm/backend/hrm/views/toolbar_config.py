"""
Toolbar Configuration API Views

Provides API endpoints for frontend to fetch toolbar configurations
based on ERPMenuItem settings.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from ..models.toolbar_config import ERPMenuItem


@csrf_exempt
@require_http_methods(["GET"])
def get_toolbar_config(request, menu_id):
    """
    API endpoint to fetch toolbar configuration for a given menu_id.
    
    Args:
        request: HTTP request object
        menu_id: The menu_id to lookup (e.g., 'EMPLOYEE_MASTER')
    
    Returns:
        JsonResponse with toolbar configuration or error
    """
    try:
        # Fetch the menu item
        menu_item = ERPMenuItem.objects.get(
            menu_id=menu_id,
            is_active=True
        )
        
        # Return the toolbar configuration
        return JsonResponse({
            'menu_id': menu_item.menu_id,
            'menu_name': menu_item.menu_name,
            'toolbar_config': menu_item.toolbar_config,
            'applicable_toolbar_config': menu_item.applicable_toolbar_config,
            'menu_type': menu_item.menu_type,
            'app': menu_item.app,
            'module': menu_item.module,
            'submodule': menu_item.submodule,
            'is_active': menu_item.is_active
        })
        
    except ERPMenuItem.DoesNotExist:
        return JsonResponse({
            'error': f'Menu item not found: {menu_id}',
            'menu_id': menu_id
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_toolbar_configs(request):
    """
    API endpoint to list all active toolbar configurations.
    
    Returns:
        JsonResponse with list of all active menu items and their configs
    """
    try:
        menu_items = ERPMenuItem.objects.filter(is_active=True).order_by('module', 'menu_name')
        
        configs = []
        for item in menu_items:
            configs.append({
                'menu_id': item.menu_id,
                'menu_name': item.menu_name,
                'toolbar_config': item.toolbar_config,
                'menu_type': item.menu_type,
                'app': item.app,
                'module': item.module,
                'submodule': item.submodule
            })
        
        return JsonResponse({
            'menu_items': configs,
            'count': len(configs)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)

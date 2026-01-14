"""
Toolbar Permissions API Views - v2.0 API-Driven System

Provides API endpoints for frontend to fetch filtered toolbar actions
based on ERPMenuItem settings, user roles, and UI modes.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import models
from ..models.toolbar_config import ERPMenuItem, Role, RolePermission, UserRole
from django.contrib.auth.models import User
import json

# Action mapping from character codes to action IDs
ACTION_MAP = {
    'N': 'new',
    'E': 'edit',
    'R': 'refresh',
    'Q': 'search',
    'F': 'filter',
    'X': 'exit',
    'V': 'view',
    'D': 'delete',
    'I': 'import',
    'O': 'export',
    'L': 'clone',
    'B': 'notes',
    'U': 'attach',
    'G': 'help',
    'S': 'save',
    'C': 'cancel',
    'K': 'clear',
    'A': 'authorize',
    'T': 'submit',
    'J': 'reject',
    'W': 'amend',
    'P': 'print',
    'M': 'email',
    '1': 'first',
    '2': 'prev',
    '3': 'next',
    '4': 'last',
    'H': 'hold',
    'Z': 'void',
}

# Mode-based action filtering rules
MODE_ACTION_FILTERS = {
    'VIEW': [
        'new', 'edit', 'view', 'delete', 'refresh', 'search', 'filter', 
        'import', 'export', 'exit', 'authorize', 'submit', 'reject', 
        'amend', 'print', 'email', 'first', 'previous', 'next', 'last'
    ],
    'VIEW_FORM': [
        'edit', 'delete', 'print', 'email', 'clone', 'exit',
        'authorize', 'reject', 'amend', 'first', 'previous', 'next', 'last'
    ],
    'CREATE': [
        'save', 'cancel', 'clear', 'exit', 'help', 'notes', 'attach'
    ],
    'EDIT': [
        'save', 'cancel', 'clear', 'exit', 'help', 'notes', 'attach', 'submit'
    ]
}

def parse_config_string(config_string):
    """Parse character string configuration to action IDs."""
    actions = []
    for char in config_string.upper():
        if char in ACTION_MAP:
            actions.append(ACTION_MAP[char])
    return actions

def filter_actions_by_mode(actions, mode):
    """Filter actions based on UI mode."""
    if mode in MODE_ACTION_FILTERS:
        return [action for action in actions if action in MODE_ACTION_FILTERS[mode]]
    return actions

def get_user_roles(user):
    """Get all roles assigned to a user."""
    if user.is_anonymous:
        return []
    user_roles = UserRole.objects.filter(user=user).select_related('role')
    return [ur.role for ur in user_roles]

def apply_role_permissions(menu_item, user, actions):
    """Apply role-based permission overrides to actions."""
    if user.is_anonymous:
        # For anonymous users, return the actual toolbar config actions as fallback
        return parse_config_string(menu_item.toolbar_config)
    
    try:
        user_roles = get_user_roles(user)
        if not user_roles:
            # If no user roles exist, return the actual toolbar config actions as fallback
            return parse_config_string(menu_item.toolbar_config)
        
        # Check for role-specific overrides
        for role in user_roles:
            try:
                role_perm = RolePermission.objects.get(
                    menu_item=menu_item,
                    role=role,
                    override_enabled=True
                )
                if role_perm.toolbar_override:
                    # Parse override configuration
                    override_actions = parse_config_string(role_perm.toolbar_override)
                    # Only keep actions that are in both base config and override
                    actions = [action for action in actions if action in override_actions]
                    # Add any actions from override that aren't in base (for additional permissions)
                    for action in override_actions:
                        if action not in actions:
                            actions.append(action)
                    break  # Use first matching role override
            except RolePermission.DoesNotExist:
                continue
    except:
        # If there's any error with user roles/permissions, return the actual toolbar config actions as fallback
        return parse_config_string(menu_item.toolbar_config)
    
    return actions

@csrf_exempt
@require_http_methods(["GET"])
def get_toolbar_permissions(request):
    """
    API endpoint to fetch filtered toolbar permissions based on view_id, mode, and user roles.
    
    Query Parameters:
        view_id: The menu_id to lookup (e.g., 'HRM_EMPLOYEE_MASTER')
        mode: The UI mode (VIEW, VIEW_FORM, CREATE, EDIT)
    
    Returns:
        JsonResponse with filtered allowed_actions array
    """
    view_id = request.GET.get('view_id')
    mode = request.GET.get('mode', 'VIEW')
    
    if not view_id:
        return JsonResponse({
            'error': 'view_id parameter is required',
            'allowed_actions': []
        }, status=400)
    
    if mode not in MODE_ACTION_FILTERS:
        return JsonResponse({
            'error': f'Invalid mode: {mode}. Valid modes: {list(MODE_ACTION_FILTERS.keys())}',
            'allowed_actions': []
        }, status=400)
    
    try:
        # Fetch the menu item
        menu_item = ERPMenuItem.objects.get(
            menu_id=view_id,
            is_active=True
        )
        
        # Parse base configuration
        base_actions = parse_config_string(menu_item.toolbar_config)
        
        # Filter by mode
        mode_filtered_actions = filter_actions_by_mode(base_actions, mode)
        
        # Apply user role permissions
        user = request.user if hasattr(request, 'user') and request.user else None
        final_actions = apply_role_permissions(menu_item, user, mode_filtered_actions)
        
        return JsonResponse({
            'allowed_actions': final_actions,
            'view_id': menu_item.menu_id,
            'menu_name': menu_item.menu_name,
            'mode': mode,
            'toolbar_config': menu_item.toolbar_config,
            'user_roles': [role.name for role in get_user_roles(user)] if user else []
        })
        
    except ERPMenuItem.DoesNotExist:
        return JsonResponse({
            'error': f'Menu item not found: {view_id}',
            'allowed_actions': []
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e),
            'allowed_actions': []
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def list_toolbar_permissions(request):
    """
    API endpoint to list all available toolbar configurations with their permissions.
    
    Returns:
        JsonResponse with all menu items and their permission details
    """
    try:
        menu_items = ERPMenuItem.objects.filter(is_active=True).order_by('module', 'menu_name')
        
        configs = []
        for item in menu_items:
            # Get permissions for each mode
            mode_permissions = {}
            for mode in MODE_ACTION_FILTERS:
                base_actions = parse_config_string(item.toolbar_config)
                mode_filtered = filter_actions_by_mode(base_actions, mode)
                mode_permissions[mode] = mode_filtered
            
            configs.append({
                'menu_id': item.menu_id,
                'menu_name': item.menu_name,
                'toolbar_config': item.toolbar_config,
                'menu_type': item.menu_type,
                'app': item.app,
                'module': item.module,
                'submodule': item.submodule,
                'mode_permissions': mode_permissions
            })
        
        return JsonResponse({
            'menu_items': configs,
            'count': len(configs),
            'available_modes': list(MODE_ACTION_FILTERS.keys())
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_user_toolbar_permissions(request):
    """
    API endpoint to get toolbar permissions for the authenticated user.
    
    Query Parameters:
        view_id: The menu_id to lookup
        mode: The UI mode (VIEW, VIEW_FORM, CREATE, EDIT)
    
    Returns:
        JsonResponse with user-specific allowed_actions
    """
    view_id = request.GET.get('view_id')
    mode = request.GET.get('mode', 'VIEW')
    
    if not view_id:
        return JsonResponse({
            'error': 'view_id parameter is required',
            'allowed_actions': []
        }, status=400)
    
    # Reuse the main permissions function with authenticated user
    return get_toolbar_permissions(request)

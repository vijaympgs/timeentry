from django.db import models

"""
TOOLBAR BACKEND MODELS REFERENCE
--------------------------------
These models define how toolbar configurations are stored and retrieved.
They should be replicated or extended in the HRM/CRM user management modules.
"""

class ERPToolbarControl(models.Model):
    """
    Superset definitions for action codes.
    Action Codes Mapping:
    - N: New (Plus)         - E: Edit (Edit)        - S: Save (Save)
    - C: Cancel (X)         - K: Clear (Rotate)     - V: View (Eye)
    - P: Print (Printer)    - M: Email (Mail)       - R: Refresh (Refresh)
    - D: Delete (Trash)     - X: Exit (LogOut)      - Q: Search (Search)
    - F: Filter (Filter)    - I: Import (Upload)    - O: Export (Download)
    - L: Clone (Copy)       - B: Notes (Note)       - U: Attach (Paperclip)
    - G: Settings (Gear)    - ?: Help (Help)
    
    Workflows:
    - T: Submit (Send)      - J: Reject (Ban)       - H: Hold (Pause)
    - Z: Void (Octagon)     - A: Authorize (Check)  - W: Amend (FileEdit)
    """
    module_name = models.CharField(max_length=50, unique=True, choices=[
        ('RETAIL', 'Retail Operations'),
        ('FMS', 'Financial Management'),
        ('HRM', 'Human Resources'),
        ('CRM', 'Customer Relationship Management')
    ])
    master_toolbar_string = models.CharField(
        max_length=100,
        placeholder="NESCKVPMRDXQF IOLBUGTJ HZAW?" # Full superset
    )

class ERPMenuItem(models.Model):
    """Registry item for every Page/Menu in the ERP"""
    menu_id = models.CharField(max_length=100, unique=True) # Used as viewId in Frontend
    menu_name = models.CharField(max_length=200)
    
    # The crucial configuration field
    applicable_toolbar_config = models.CharField(
        max_length=100,
        help_text="Config string for this page. Example: 'NRQFX' (New, Refresh, Search, Filter, Exit)"
    )

class RolePermission(models.Model):
    """Allows per-role overrides for the toolbar"""
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ERPMenuItem, on_delete=models.CASCADE)
    
    toolbar_override = models.CharField(
        max_length=100,
        null=True, blank=True,
        help_text="Override string for specific roles (e.g., restricted users cannot Delete 'D')"
    )
    override_enabled = models.BooleanField(default=False)

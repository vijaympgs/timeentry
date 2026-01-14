from django.db import models
from django.contrib.auth.models import User


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
        ('FMS', 'Financial Management'),
        ('HRM', 'Human Resources'),
        ('CRM', 'Customer Relationship Management')
    ])
    master_toolbar_string = models.CharField(
        max_length=100,
        default="NESCKVPMRDXQF IOLBUGTJ HZAW?",
        help_text="Full superset of all available toolbar actions"
    )
    
    class Meta:
        db_table = 'hrm_toolbar_control'
        verbose_name = "Toolbar Control"
        verbose_name_plural = "Toolbar Controls"
    
    def __str__(self):
        return f"{self.module_name} Toolbar Control"


class ERPMenuItem(models.Model):
    """
    Registry item for every Page/Menu in the ERP
    """
    menu_id = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Used as viewId in Frontend (e.g., 'HRM_EMPLOYEE_MASTER')"
    )
    menu_name = models.CharField(max_length=200)
    app = models.CharField(
        max_length=50,
        choices=[
            ('FMS', 'Financial Management'),
            ('HRM', 'Human Resources'),
            ('CRM', 'Customer Relationship Management')
        ],
        default='HRM',
        help_text="Application/Module this menu belongs to"
    )
    submodule = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Submodule or subcategory within the application"
    )
    module = models.CharField(
        max_length=50,
        choices=[
            ('FMS', 'Financial Management'),
            ('HRM', 'Human Resources'),
            ('CRM', 'Customer Relationship Management')
        ],
        default='HRM',
        help_text="Module classification for organization"
    )
    menu_type = models.CharField(
        max_length=10,
        choices=[
            # Master Data Templates
            ('MST-S', 'Simple Master'),
            ('MST-M', 'Medium Master'),
            ('MST-C', 'Complex Master'),
            # Transaction Templates
            ('TXN-S', 'Simple Transaction'),
            ('TXN-M', 'Medium Transaction'),
            ('TXN-C', 'Complex Transaction'),
            # Other Types
            ('M', 'Master (Legacy)'),
            ('T', 'Transaction (Legacy)'),
            ('D', 'Dashboard'),
            ('R', 'Report'),
            ('C', 'Configuration'),
            ('S', 'Setup'),
            ('U', 'Utility'),
            ('Q', 'Query'),
            ('W', 'Workflow'),
            ('A', 'Analytics')
        ],
        default='M',
        help_text="Type of menu item based on template classification"
    )
    
    # The crucial configuration field
    toolbar_config = models.CharField(
        max_length=100,
        default="NRQFX",
        help_text="Toolbar configuration string for this page. Example: 'NRQFX' (New, Refresh, Search, Filter, Exit)"
    )
    applicable_toolbar_config = models.CharField(
        max_length=100,
        default="NRQFX",
        help_text="Legacy field - use toolbar_config instead"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hrm_menu_item'
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['module', 'menu_name']
    
    def __str__(self):
        return f"{self.menu_name} ({self.menu_id})"


class Role(models.Model):
    """
    User roles for the system
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hrm_role'
        verbose_name = "Role"
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """
    Allows per-role overrides for the toolbar
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ERPMenuItem, on_delete=models.CASCADE)
    
    toolbar_override = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Override string for specific roles (e.g., restricted users cannot Delete 'D')"
    )
    override_enabled = models.BooleanField(
        default=False,
        help_text="Enable this override for the specified role"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hrm_role_permission'
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"
        unique_together = ['role', 'menu_item']
    
    def __str__(self):
        return f"{self.role.name} - {self.menu_item.menu_name}"
    
    def get_effective_config(self):
        """
        Returns the effective toolbar configuration for this role/menu combination
        """
        if self.override_enabled and self.toolbar_override:
            return self.toolbar_override
        return self.menu_item.applicable_toolbar_config


class UserRole(models.Model):
    """
    Many-to-many relationship between Users and Roles
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='role_assignments'
    )
    
    class Meta:
        db_table = 'hrm_user_role'
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"
        unique_together = ['user', 'role']
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

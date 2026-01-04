# Permissions Service

Role-based access control (RBAC) system for the enterprise platform.

## Features

- Role management
- Permission management
- Resource-based access control
- Dynamic permission assignment
- Module-specific permissions

## Structure

```
permissions/
├── models.py          # Role and permission models
├── serializers.py     # Permission serializers
├── views.py          # Permission management views
├── urls.py           # Permission URLs
├── decorators.py     # Permission decorators
├── utils.py          # Permission utilities
├── mixins.py         # DRF permission mixins
└── migrations/       # Database migrations
```

## Permission Types

- **Module Permissions**: HRM, CRM, FMS access
- **Resource Permissions**: Create, Read, Update, Delete
- **Field Permissions**: Field-level access control
- **Custom Permissions**: Business-specific permissions

# Authentication Service

Centralized authentication and authorization service for all platform modules.

## Features

- JWT-based authentication
- User management
- Session management
- Multi-factor authentication support
- SSO integration ready

## Structure

```
auth/
├── models.py          # User and authentication models
├── serializers.py     # Authentication serializers
├── views.py          # Authentication views
├── urls.py           # Authentication URLs
├── permissions.py    # Custom permissions
├── middleware.py     # Authentication middleware
├── utils.py          # Authentication utilities
└── migrations/       # Database migrations

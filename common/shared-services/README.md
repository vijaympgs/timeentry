# Shared Services

Common utilities and services used across all platform modules.

## Features

- Database utilities
- API utilities
- File handling services
- Notification services
- Logging utilities
- Cache management
- Validation helpers

## Structure

```
shared-services/
├── database/
│   ├── __init__.py
│   ├── utils.py          # Database utilities
│   └── managers.py       # Custom model managers
├── api/
│   ├── __init__.py
│   ├── utils.py          # API utilities
│   ├── middleware.py     # API middleware
│   └── exceptions.py     # Custom API exceptions
├── file_handling/
│   ├── __init__.py
│   ├── storage.py        # File storage utilities
│   └── processors.py     # File processors
├── notifications/
│   ├── __init__.py
│   ├── email.py          # Email services
│   ├── sms.py            # SMS services
│   └── push.py           # Push notifications
├── logging/
│   ├── __init__.py
│   ├── utils.py          # Logging utilities
│   └── handlers.py       # Custom log handlers
├── cache/
│   ├── __init__.py
│   ├── utils.py          # Cache utilities
│   └── decorators.py     # Cache decorators
└── validation/
    ├── __init__.py
    ├── utils.py          # Validation utilities
    └── validators.py     # Custom validators

# CRM Module - Customer Relationship Management

Customer Relationship Management module for the enterprise platform.

## Features

- Lead management and tracking
- Contact management
- Account management
- Opportunity pipeline
- Sales forecasting
- Campaign management
- Customer support
- Analytics and reporting

## Structure

```
crm/
├── backend/                    # Django Backend
│   ├── __init__.py
│   ├── settings.py            # CRM-specific settings
│   ├── urls.py                # CRM URL configuration
│   ├── wsgi.py                # WSGI configuration
│   ├── asgi.py                # ASGI configuration
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── customer.py        # Customer model
│   │   ├── lead.py            # Lead model
│   │   ├── contact.py         # Contact model
│   │   ├── account.py         # Account model
│   │   ├── opportunity.py     # Opportunity model
│   │   ├── campaign.py        # Campaign model
│   │   └── activity.py        # Activity model
│   ├── serializers/           # API serializers
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── contact.py
│   │   ├── account.py
│   │   ├── opportunity.py
│   │   ├── campaign.py
│   │   └── activity.py
│   ├── views/                 # API views
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── contact.py
│   │   ├── account.py
│   │   ├── opportunity.py
│   │   ├── campaign.py
│   │   └── activity.py
│   ├── urls/                  # URL routing
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── contact.py
│   │   ├── account.py
│   │   ├── opportunity.py
│   │   ├── campaign.py
│   │   └── activity.py
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── lead_service.py
│   │   ├── opportunity_service.py
│   │   ├── campaign_service.py
│   │   └── analytics_service.py
│   ├── utils/                 # Utilities
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── validators.py
│   ├── migrations/            # Database migrations
│   └── tests/                 # Test files
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_views.py
│       └── test_services.py
│
└── frontend/                  # React Frontend
    ├── public/                # Static assets
    ├── src/                   # Source code
    │   ├── components/        # React components
    │   ├── pages/             # Page components
    │   ├── services/          # API services
    │   ├── hooks/             # Custom hooks
    │   ├── utils/             # Utilities
    │   ├── types/             # TypeScript types
    │   └── styles/            # Styles
    ├── package.json           # Node dependencies
    ├── tsconfig.json          # TypeScript config
    ├── vite.config.ts         # Vite config
    └── tailwind.config.js     # Tailwind config
```

## API Endpoints

### Lead Management
- `GET /api/leads/` - List leads
- `POST /api/leads/` - Create lead
- `GET /api/leads/{id}/` - Get lead
- `PUT /api/leads/{id}/` - Update lead
- `DELETE /api/leads/{id}/` - Delete lead

### Customer Management
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer
- `PUT /api/customers/{id}/` - Update customer

### Opportunity Pipeline
- `GET /api/opportunities/` - List opportunities
- `POST /api/opportunities/` - Create opportunity
- `PUT /api/opportunities/{id}/stage/` - Update opportunity stage

### Campaign Management
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/` - Create campaign
- `POST /api/campaigns/{id}/launch/` - Launch campaign

# FMS Module - Financial Management System

Financial Management System module for the enterprise platform.

## Features

- Chart of accounts management
- General ledger and journal entries
- Accounts payable and receivable
- Bank reconciliation
- Financial reporting
- Budget management
- Tax management
- Multi-currency support
- Fixed asset management
- Audit trail

## Structure

```
fms/
├── backend/                    # Django Backend
│   ├── __init__.py
│   ├── settings.py            # FMS-specific settings
│   ├── urls.py                # FMS URL configuration
│   ├── wsgi.py                # WSGI configuration
│   ├── asgi.py                # ASGI configuration
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── chart_of_accounts.py # Chart of accounts model
│   │   ├── journal.py         # Journal entry model
│   │   ├── ledger.py          # General ledger model
│   │   ├── account.py         # Account model
│   │   ├── transaction.py     # Transaction model
│   │   ├── invoice.py         # Invoice model
│   │   ├── payment.py         # Payment model
│   │   ├── budget.py          # Budget model
│   │   ├── tax.py             # Tax model
│   │   └── asset.py           # Fixed asset model
│   ├── serializers/           # API serializers
│   │   ├── __init__.py
│   │   ├── chart_of_accounts.py
│   │   ├── journal.py
│   │   ├── ledger.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── budget.py
│   │   ├── tax.py
│   │   └── asset.py
│   ├── views/                 # API views
│   │   ├── __init__.py
│   │   ├── chart_of_accounts.py
│   │   ├── journal.py
│   │   ├── ledger.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── budget.py
│   │   ├── tax.py
│   │   └── asset.py
│   ├── urls/                  # URL routing
│   │   ├── __init__.py
│   │   ├── chart_of_accounts.py
│   │   ├── journal.py
│   │   ├── ledger.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── budget.py
│   │   ├── tax.py
│   │   └── asset.py
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── accounting_service.py
│   │   ├── journal_service.py
│   │   ├── reconciliation_service.py
│   │   ├── reporting_service.py
│   │   └── tax_service.py
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

### Chart of Accounts
- `GET /api/chart-of-accounts/` - List chart of accounts
- `POST /api/chart-of-accounts/` - Create account
- `GET /api/chart-of-accounts/{id}/` - Get account
- `PUT /api/chart-of-accounts/{id}/` - Update account

### Journal Entries
- `GET /api/journal-entries/` - List journal entries
- `POST /api/journal-entries/` - Create journal entry
- `GET /api/journal-entries/{id}/` - Get journal entry
- `POST /api/journal-entries/{id}/post/` - Post journal entry

### Transactions
- `GET /api/transactions/` - List transactions
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction

### Financial Reports
- `GET /api/reports/trial-balance/` - Trial balance
- `GET /api/reports/income-statement/` - Income statement
- `GET /api/reports/balance-sheet/` - Balance sheet
- `GET /api/reports/cash-flow/` - Cash flow statement

# UI Canon - Design System

Centralized UI component library and design system for the enterprise platform.

## Features

- Component library
- Design tokens
- Theme system
- Pattern library
- Accessibility guidelines
- Responsive design utilities

## Structure

```
ui-canon/
├── components/              # Reusable UI components
│   ├── forms/              # Form components
│   ├── tables/             # Table components
│   ├── modals/             # Modal components
│   ├── navigation/         # Navigation components
│   ├── feedback/           # Feedback components (alerts, toasts)
│   └── layout/             # Layout components
├── tokens/                 # Design tokens
│   ├── colors.ts           # Color tokens
│   ├── typography.ts       # Typography tokens
│   ├── spacing.ts          # Spacing tokens
│   └── shadows.ts          # Shadow tokens
├── themes/                 # Theme configurations
│   ├── light.ts            # Light theme
│   ├── dark.ts             # Dark theme
│   └── index.ts            # Theme exports
├── patterns/               # UI patterns
│   ├── templates/          # Page templates
│   ├── layouts/            # Layout patterns
│   └── flows/              # User flow patterns
├── utils/                  # UI utilities
│   ├── helpers.ts          # Helper functions
│   ├── hooks.ts            # Custom React hooks
│   └── constants.ts        # UI constants
└── styles/                 # Global styles
    ├── globals.css         # Global CSS
    ├── components.css      # Component styles
    └── utilities.css       # Utility classes
```

## Usage

Import components and utilities from the UI canon in any module:

```typescript
import { Button, DataTable, Modal } from '@/common/ui-canon';
import { colors, spacing } from '@/common/ui-canon/tokens';

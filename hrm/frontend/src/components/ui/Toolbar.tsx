import React from 'react'
import { 
  Plus, 
  Edit, 
  Eye, 
  Trash2, 
  X, 
  RefreshCw, 
  Copy, 
  Check, 
  LogOut,
  Save,
  FileText,
  Filter,
  Search,
  Download,
  Upload
} from 'lucide-react'

interface ToolbarButton {
  id: string
  icon: React.ComponentType<{ className?: string }>
  label: string
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary' | 'danger'
}

interface ToolbarProps {
  title?: string
  buttons: ToolbarButton[]
  className?: string
}

export function Toolbar({ title, buttons, className = '' }: ToolbarProps) {
  return (
    <div className={`bg-[#f3f2f1] px-3 py-2 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1">
          {buttons.map((button) => {
            const Icon = button.icon
            const variantClasses = button.variant === 'primary' 
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : button.variant === 'danger'
              ? 'bg-red-500 text-white hover:bg-red-600'
              : 'bg-white text-gray-700 hover:bg-gray-50'
            
            return (
              <button
                key={button.id}
                onClick={button.onClick}
                disabled={button.disabled}
                className={`flex items-center justify-center w-9 h-9 transition-all duration-200 ease-out disabled:opacity-50 disabled:cursor-not-allowed group relative`}
                title={button.label}
              >
                <Icon className="w-4 h-4" />
                {/* Enhanced Tooltip */}
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gradient-to-r from-gray-900 to-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50">
                  {button.label}
                  <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                </div>
              </button>
            )
          })}
        </div>
        {title && (
          <div className="text-sm font-bold text-transparent bg-clip-text bg-gradient-to-r from-slate-700 to-slate-900 ml-6">
            {title}
          </div>
        )}
      </div>
    </div>
  )
}

// Predefined toolbar button sets for common operations
export const ToolbarButtons = {
  // Standard CRUD operations
  crud: (handlers: {
    onNew?: () => void
    onEdit?: () => void
    onView?: () => void
    onDelete?: () => void
  }): ToolbarButton[] => [
    {
      id: 'new',
      icon: Plus,
      label: 'New',
      onClick: handlers.onNew || (() => {}),
      variant: 'primary'
    },
    {
      id: 'edit',
      icon: Edit,
      label: 'Edit',
      onClick: handlers.onEdit || (() => {})
    },
    {
      id: 'view',
      icon: Eye,
      label: 'View',
      onClick: handlers.onView || (() => {})
    },
    {
      id: 'delete',
      icon: Trash2,
      label: 'Delete',
      onClick: handlers.onDelete || (() => {}),
      variant: 'danger'
    }
  ],

  // Data operations
  data: (handlers: {
    onRefresh?: () => void
    onClear?: () => void
    onExport?: () => void
    onImport?: () => void
  }): ToolbarButton[] => [
    {
      id: 'refresh',
      icon: RefreshCw,
      label: 'Refresh',
      onClick: handlers.onRefresh || (() => {})
    },
    {
      id: 'clear',
      icon: X,
      label: 'Clear',
      onClick: handlers.onClear || (() => {})
    },
    {
      id: 'export',
      icon: Download,
      label: 'Export',
      onClick: handlers.onExport || (() => {})
    },
    {
      id: 'import',
      icon: Upload,
      label: 'Import',
      onClick: handlers.onImport || (() => {})
    }
  ],

  // Search and filter
  search: (handlers: {
    onSearch?: () => void
    onFilter?: () => void
  }): ToolbarButton[] => [
    {
      id: 'search',
      icon: Search,
      label: 'Search',
      onClick: handlers.onSearch || (() => {})
    },
    {
      id: 'filter',
      icon: Filter,
      label: 'Filter',
      onClick: handlers.onFilter || (() => {})
    }
  ],

  // Form operations
  form: (handlers: {
    onSave?: () => void
    onCancel?: () => void
    onClone?: () => void
  }): ToolbarButton[] => [
    {
      id: 'save',
      icon: Save,
      label: 'Save',
      onClick: handlers.onSave || (() => {}),
      variant: 'primary'
    },
    {
      id: 'cancel',
      icon: X,
      label: 'Cancel',
      onClick: handlers.onCancel || (() => {})
    },
    {
      id: 'clone',
      icon: Copy,
      label: 'Clone',
      onClick: handlers.onClone || (() => {})
    }
  ],

  // Authorization operations
  auth: (handlers: {
    onAuthorize?: () => void
    onExit?: () => void
  }): ToolbarButton[] => [
    {
      id: 'authorize',
      icon: Check,
      label: 'Authorize',
      onClick: handlers.onAuthorize || (() => {}),
      variant: 'primary'
    },
    {
      id: 'exit',
      icon: LogOut,
      label: 'Exit',
      onClick: handlers.onExit || (() => {})
    }
  ]
}

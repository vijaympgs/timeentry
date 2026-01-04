import React from 'react'
import { Search, Filter, X, ChevronDown } from 'lucide-react'

interface FilterOption {
  value: string
  label: string
}

interface FilterField {
  name: string
  label: string
  type: 'select' | 'multiselect' | 'date' | 'daterange' | 'text'
  options?: FilterOption[]
  placeholder?: string
}

interface SearchFilterProps {
  searchValue: string
  onSearchChange: (value: string) => void
  filters: Record<string, any>
  onFilterChange: (field: string, value: any) => void
  filterFields: FilterField[]
  onClearFilters: () => void
  onSearch: () => void
  loading?: boolean
  placeholder?: string
  showAdvancedFilters?: boolean
  onToggleAdvancedFilters?: () => void
}

export function SearchFilter({
  searchValue,
  onSearchChange,
  filters,
  onFilterChange,
  filterFields,
  onClearFilters,
  onSearch,
  loading = false,
  placeholder = 'Search...',
  showAdvancedFilters = false,
  onToggleAdvancedFilters
}: SearchFilterProps) {
  const [isDropdownOpen, setIsDropdownOpen] = React.useState<string | null>(null)

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      onSearch()
    }
  }

  const hasActiveFilters = Object.values(filters).some(value => 
    value !== '' && value !== null && value !== undefined
  )

  const renderFilterField = (field: FilterField) => {
    const value = filters[field.name] || ''

    switch (field.type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => onFilterChange(field.name, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">{field.placeholder || `Select ${field.label}`}</option>
            {field.options?.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )

      case 'multiselect':
        return (
          <div className="relative">
            <button
              type="button"
              onClick={() => setIsDropdownOpen(isDropdownOpen === field.name ? null : field.name)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-left focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {Array.isArray(value) && value.length > 0 
                ? `${value.length} selected`
                : field.placeholder || `Select ${field.label}`
              }
              <ChevronDown className="absolute right-2 top-2.5 h-4 w-4" />
            </button>
            
            {isDropdownOpen === field.name && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
                {field.options?.map(option => (
                  <label
                    key={option.value}
                    className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={Array.isArray(value) && value.includes(option.value)}
                      onChange={(e) => {
                        const currentValue = Array.isArray(value) ? value : []
                        if (e.target.checked) {
                          onFilterChange(field.name, [...currentValue, option.value])
                        } else {
                          onFilterChange(field.name, currentValue.filter(v => v !== option.value))
                        }
                      }}
                      className="mr-2 h-4 w-4 text-blue-600 rounded border-gray-300"
                    />
                    {option.label}
                  </label>
                ))}
              </div>
            )}
          </div>
        )

      case 'date':
        return (
          <input
            type="date"
            value={value}
            onChange={(e) => onFilterChange(field.name, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )

      case 'daterange':
        return (
          <div className="flex gap-2">
            <input
              type="date"
              value={value?.start || ''}
              onChange={(e) => onFilterChange(field.name, { ...value, start: e.target.value })}
              placeholder="Start date"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="date"
              value={value?.end || ''}
              onChange={(e) => onFilterChange(field.name, { ...value, end: e.target.value })}
              placeholder="End date"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        )

      case 'text':
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => onFilterChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )

      default:
        return null
    }
  }

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 space-y-4">
      {/* Quick Filters */}
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[300px]">
          <label className="block text-xs font-medium text-gray-700 mb-1">
            Search
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder={placeholder}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        {filterFields.slice(0, 3).map(field => (
          <div key={field.name} className="min-w-[180px]">
            <label className="block text-xs font-medium text-gray-700 mb-1">
              {field.label}
            </label>
            {renderFilterField(field)}
          </div>
        ))}

        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:text-red-700 self-end"
          >
            <X className="h-4 w-4" />
            Clear Filters
          </button>
        )}
      </div>

      {/* Advanced Filters */}
      {showAdvancedFilters && filterFields.length > 3 && (
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-sm font-medium text-gray-900">Advanced Filters</h4>
            <button
              onClick={onToggleAdvancedFilters}
              className="text-sm text-blue-600 hover:text-blue-700"
            >
              {onToggleAdvancedFilters ? 'Hide' : 'Show'}
            </button>
          </div>
          
          {onToggleAdvancedFilters && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filterFields.slice(3).map(field => (
                <div key={field.name}>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    {field.label}
                  </label>
                  {renderFilterField(field)}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Filter Summary */}
      {hasActiveFilters && (
        <div className="flex flex-wrap gap-2 border-t border-gray-200 pt-4">
          <span className="text-xs font-medium text-gray-500">Active filters:</span>
          {Object.entries(filters).map(([key, value]) => {
            if (!value || (Array.isArray(value) && value.length === 0)) return null
            
            const field = filterFields.find(f => f.name === key)
            if (!field) return null

            const getDisplayValue = () => {
              if (Array.isArray(value)) {
                return `${value.length} selected`
              }
              if (typeof value === 'object' && value !== null) {
                return `${value.start || ''} - ${value.end || ''}`
              }
              return String(value)
            }

            return (
              <span
                key={key}
                className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
              >
                {field.label}: {getDisplayValue()}
                <button
                  onClick={() => onFilterChange(key, field.type === 'multiselect' ? [] : '')}
                  className="hover:text-blue-600"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            )
          })}
        </div>
      )}
    </div>
  )
}

// Quick filter component for common filters
interface QuickFilterProps {
  label: string
  options: FilterOption[]
  value: string
  onChange: (value: string) => void
  className?: string
}

export function QuickFilter({ label, options, value, onChange, className = '' }: QuickFilterProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-sm font-medium text-gray-700">{label}:</span>
      <div className="flex gap-1">
        {options.map(option => (
          <button
            key={option.value}
            onClick={() => onChange(value === option.value ? '' : option.value)}
            className={`px-3 py-1 text-xs font-medium rounded-full transition-colors ${
              value === option.value
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  )
}

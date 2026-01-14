import React from 'react'

interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'number' | 'tel' | 'date' | 'select' | 'textarea' | 'file' | 'checkbox'
  placeholder?: string
  required?: boolean
  options?: { value: string; label: string }[]
  validation?: {
    min?: number
    max?: number
    pattern?: RegExp
    message?: string
  }
  disabled?: boolean
  rows?: number // for textarea
}

interface FormProps {
  fields: FormField[]
  data: Record<string, any>
  onChange: (field: string, value: any) => void
  onSubmit: (data: Record<string, any>) => void
  onCancel?: () => void
  loading?: boolean
  errors?: Record<string, string>
  submitText?: string
  cancelText?: string
  layout?: 'vertical' | 'horizontal' | 'grid'
  hideButtons?: boolean
}

export function Form({
  fields,
  data,
  onChange,
  onSubmit,
  onCancel,
  loading = false,
  errors = {},
  submitText = 'Submit',
  cancelText = 'Cancel',
  layout = 'vertical',
  hideButtons = false
}: FormProps) {
  const [formErrors, setFormErrors] = React.useState<Record<string, string>>({})

  const validateField = (field: FormField, value: any): string | null => {
    if (field.required && (!value || value.toString().trim() === '')) {
      return `${field.label} is required`
    }

    if (field.validation && value) {
      const { min, max, pattern, message } = field.validation
      
      if (min && value.toString().length < min) {
        return message || `${field.label} must be at least ${min} characters`
      }
      
      if (max && value.toString().length > max) {
        return message || `${field.label} must not exceed ${max} characters`
      }
      
      if (pattern && !pattern.test(value.toString())) {
        return message || `${field.label} format is invalid`
      }
    }

    return null
  }

  const handleFieldChange = (field: FormField, value: any) => {
    onChange(field.name, value)
    
    const error = validateField(field, value)
    setFormErrors(prev => {
      const newErrors = { ...prev }
      if (error) {
        newErrors[field.name] = error
      } else {
        delete newErrors[field.name]
      }
      return newErrors
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const newErrors: Record<string, string> = {}
    let isValid = true

    fields.forEach(field => {
      const error = validateField(field, data[field.name])
      if (error) {
        newErrors[field.name] = error
        isValid = false
      }
    })

    setFormErrors(newErrors)

    if (isValid) {
      onSubmit(data)
    }
  }

  const renderField = (field: FormField) => {
    const error = formErrors[field.name] || errors[field.name]
    const hasError = !!error

    const fieldClasses = `input ${hasError ? 'border-red-500 focus:ring-red-500' : ''}`

    const commonProps = {
      id: field.name,
      value: data[field.name] || '',
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
        handleFieldChange(field, e.target.value),
      disabled: field.disabled || loading,
      className: fieldClasses,
      placeholder: field.placeholder
    }

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            {...commonProps}
            rows={field.rows || 4}
          />
        )

      case 'select':
        return (
          <select {...commonProps}>
            <option value="">Select {field.label}</option>
            {field.options?.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )

      case 'file':
        return (
          <input
            {...commonProps}
            type="file"
            onChange={(e) => handleFieldChange(field, e.target.files?.[0])}
          />
        )

      case 'checkbox':
        return (
          <input
            id={field.name}
            type="checkbox"
            checked={data[field.name] || false}
            onChange={(e) => handleFieldChange(field, e.target.checked)}
            disabled={field.disabled || loading}
            className={`h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 ${
              hasError ? 'border-red-500' : ''
            }`}
          />
        )

      default:
        return (
          <input
            {...commonProps}
            type={field.type}
          />
        )
    }
  }

  const getLayoutClasses = () => {
    switch (layout) {
      case 'horizontal':
        return 'grid grid-cols-1 md:grid-cols-2 gap-6'
      case 'grid':
        return 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
      default:
        return 'space-y-6'
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className={getLayoutClasses()}>
        {fields.map(field => {
          const error = formErrors[field.name] || errors[field.name]
          const hasError = !!error

          return (
            <div key={field.name} className={layout === 'vertical' ? 'space-y-2' : ''}>
              <label
                htmlFor={field.name}
                className={`block text-sm font-medium ${
                  hasError ? 'text-red-700' : 'text-gray-700'
                }`}
              >
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </label>
              
              {renderField(field)}
              
              {hasError && (
                <p className="text-sm text-red-600 mt-1">{error}</p>
              )}
            </div>
          )
        })}
      </div>

      {!hideButtons && (
        <div className="flex items-center justify-end gap-4 pt-6 border-t border-gray-200">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="btn btn-outline"
            >
              {cancelText}
            </button>
          )}
          
          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
          >
            {loading ? 'Submitting...' : submitText}
          </button>
        </div>
      )}
    </form>
  )
}

// Form section component for organizing forms
interface FormSectionProps {
  title: string
  description?: string
  children: React.ReactNode
}

export function FormSection({ title, description, children }: FormSectionProps) {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-medium text-gray-900">{title}</h3>
        {description && (
          <p className="text-sm text-gray-500 mt-1">{description}</p>
        )}
      </div>
      <div className="bg-white p-6 rounded-lg border border-gray-200">
        {children}
      </div>
    </div>
  )
}

// Form group component for related fields
interface FormGroupProps {
  title?: string
  children: React.ReactNode
  className?: string
}

export function FormGroup({ title, children, className = '' }: FormGroupProps) {
  return (
    <div className={`space-y-4 ${className}`}>
      {title && (
        <h4 className="text-sm font-medium text-gray-900">{title}</h4>
      )}
      {children}
    </div>
  )
}

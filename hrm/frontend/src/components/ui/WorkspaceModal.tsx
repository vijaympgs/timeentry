import React from 'react'
import { X, Save, RotateCcw, LogOut } from 'lucide-react'

interface WorkspaceModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  showCloseButton?: boolean
  closeOnBackdropClick?: boolean
  closeOnEscape?: boolean
  className?: string
  workspaceIdentifier?: string
}

export function WorkspaceModal({
  isOpen,
  onClose,
  title,
  children,
  showCloseButton = true,
  closeOnBackdropClick = true,
  closeOnEscape = true,
  className = '',
  workspaceIdentifier = 'C'
}: WorkspaceModalProps) {
  const modalRef = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && closeOnEscape && isOpen) {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, closeOnEscape, onClose])

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && closeOnBackdropClick) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* No Backdrop - Keep sidebar and header visible */}
      {/* <div
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={handleBackdropClick}
      /> */}

      {/* Workspace Container - Uses full Primary Workspace (C) area */}
      <div className="absolute inset-0 flex">
        {/* Left margin for Sidebar (B) */}
        <div className="w-64 flex-shrink-0" />
        
        {/* Top margin for App Header (A) */}
        <div className="flex-1 flex flex-col">
          <div className="h-16 flex-shrink-0" />
          
          {/* Workspace Modal Content */}
          <div className="flex-1 relative">
            {/* Top Header */}
            <div className="absolute top-0 left-0 right-0 z-10 bg-white border-b border-gray-200 px-4 py-2">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="text-xs text-gray-500 mb-1">
                    Employee Management {'>'} Employee Records
                  </div>
                  {title && (
                    <h2 className="text-sm font-semibold text-gray-900">
                      {title} <span className="ml-2 px-2 py-1 bg-gray-600 text-white text-xs rounded">New</span>
                    </h2>
                  )}
                </div>
                {showCloseButton && (
                  <button
                    onClick={onClose}
                    className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            </div>

            {/* Main Content Area */}
            <div className="h-full bg-white overflow-y-auto pt-16">
              <div className="px-6 py-4">
                {children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Workspace Modal Footer component
interface WorkspaceModalFooterProps {
  children: React.ReactNode
  className?: string
}

export function WorkspaceModalFooter({ children, className = '' }: WorkspaceModalFooterProps) {
  return (
    <div className={`flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50 ${className}`}>
      {children}
    </div>
  )
}

// Workspace Modal Body component
interface WorkspaceModalBodyProps {
  children: React.ReactNode
  className?: string
}

export function WorkspaceModalBody({ children, className = '' }: WorkspaceModalBodyProps) {
  return (
    <div className={`flex-1 overflow-y-auto px-6 py-4 ${className}`}>
      {children}
    </div>
  )
}

// Workspace Form Modal wrapper
interface WorkspaceFormModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  onSubmit: () => void
  onClear?: () => void
  submitText?: string
  cancelText?: string
  clearText?: string
  loading?: boolean
  submitDisabled?: boolean
  workspaceIdentifier?: string
}

export function WorkspaceFormModal({
  isOpen,
  onClose,
  title,
  children,
  onSubmit,
  onClear,
  submitText = 'Save',
  cancelText = 'Exit',
  clearText = 'Clear',
  loading = false,
  submitDisabled = false,
  workspaceIdentifier = 'C'
}: WorkspaceFormModalProps) {
  return (
    <WorkspaceModal 
      isOpen={isOpen} 
      onClose={onClose} 
      title={title} 
      workspaceIdentifier={workspaceIdentifier}
    >
      <div className="h-full flex flex-col">
        {/* Form Toolbar */}
        <div className="bg-gradient-to-r from-slate-50 to-gray-100 border-b border-slate-200 px-3 py-2 shadow-sm">
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={() => onSubmit()}
              disabled={loading || submitDisabled}
              className="flex items-center justify-center w-9 h-9 bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 shadow-md hover:shadow-lg border-blue-600 transform hover:scale-105 transition-all duration-200 ease-out disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none group relative rounded-lg"
              title="Save"
            >
              <Save className="w-4 h-4" />
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gradient-to-r from-gray-900 to-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50 shadow-lg">
                Save
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
              </div>
            </button>
            
            {onClear && (
              <button
                type="button"
                onClick={onClear}
                disabled={loading}
                className="flex items-center justify-center w-9 h-9 bg-gradient-to-r from-white to-gray-50 text-gray-700 hover:from-gray-50 hover:to-gray-100 border-gray-300 shadow-sm hover:shadow-md transform hover:scale-105 transition-all duration-200 ease-out disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none group relative rounded-lg"
                title="Clear"
              >
                <RotateCcw className="w-4 h-4" />
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gradient-to-r from-gray-900 to-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50 shadow-lg">
                  Clear
                  <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                </div>
              </button>
            )}
            
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="flex items-center justify-center w-9 h-9 bg-gradient-to-r from-white to-gray-50 text-gray-700 hover:from-gray-50 hover:to-gray-100 border-gray-300 shadow-sm hover:shadow-md transform hover:scale-105 transition-all duration-200 ease-out disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none group relative rounded-lg"
              title="Exit"
            >
              <LogOut className="w-4 h-4" />
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gradient-to-r from-gray-900 to-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50 shadow-lg">
                Exit
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
              </div>
            </button>
          </div>
        </div>
        
        <form onSubmit={(e) => { e.preventDefault(); onSubmit(); }} className="flex-1 flex flex-col">
          <WorkspaceModalBody>
            {children}
          </WorkspaceModalBody>
        </form>
      </div>
    </WorkspaceModal>
  )
}

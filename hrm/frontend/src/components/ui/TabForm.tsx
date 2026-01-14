import React, { useState } from 'react'

interface TabConfig {
  id: string
  label: string
  icon: React.ElementType
  component: React.ComponentType<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onSubmit: (data: Record<string, any>) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string>; hideButtons?: boolean }>
}

interface TabFormProps {
  tabs: TabConfig[]
  data: Record<string, any>
  onChange: (field: string, value: any) => void
  onSubmit: (data: Record<string, any>) => void
  onCancel: () => void
  loading?: boolean
  errors?: Record<string, string>
  submitText?: string
  cancelText?: string
  hideButtons?: boolean
  verticalTabs?: boolean
}

export function TabForm({ tabs, data, onChange, onSubmit, onCancel, loading = false, errors = {}, submitText = 'Submit', cancelText = 'Cancel', hideButtons, verticalTabs = false }: TabFormProps) {
  const [activeTab, setActiveTab] = useState(tabs[0]?.id || '')

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(data)
  }

  return (
    <div className={`w-full bg-white rounded-none shadow-sm border border-[#e5e7eb] ${verticalTabs ? 'flex' : ''}`}>
      {verticalTabs ? (
        <>
          {/* Vertical Tab Navigation */}
          <div className="w-64 border-r border-[#e5e7eb] bg-[#fafafa]">
            <nav className="p-2" aria-label="Tabs">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium transition-all duration-180 rounded-none ${
                      activeTab === tab.id
                        ? 'bg-white text-nexus-primary-700 border-r-2 border-nexus-primary-500 shadow-sm'
                        : 'text-gray-600 hover:text-nexus-primary-600 hover:bg-nexus-gray-50'
                    }`}
                  >
                    <Icon className="h-4 w-4 flex-shrink-0" />
                    <span className="font-sans text-left">{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content - Vertical Layout */}
          <div className="flex-1 p-6 bg-white overflow-y-auto">
            {ActiveComponent && (
              <ActiveComponent
                data={data}
                onChange={onChange}
                onSubmit={onSubmit}
                onCancel={onCancel}
                loading={loading}
                errors={errors}
                hideButtons={hideButtons}
              />
            )}
          </div>
        </>
      ) : (
        <>
          {/* Horizontal Tab Navigation - UI Canon Compliant */}
          <div className="border-b border-[#e5e7eb] bg-[#fafafa]">
            <nav className="flex space-x-1 p-1" aria-label="Tabs">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-4 py-3 text-sm font-medium transition-all duration-180 rounded-none ${
                      activeTab === tab.id
                        ? 'bg-white text-nexus-primary-700 border-b-2 border-nexus-primary-500 shadow-sm'
                        : 'text-gray-600 hover:text-nexus-primary-600 hover:bg-nexus-gray-50'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="font-sans">{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content - Horizontal Layout */}
          <div className="p-6 bg-white">
            {ActiveComponent && (
              <ActiveComponent
                data={data}
                onChange={onChange}
                onSubmit={onSubmit}
                onCancel={onCancel}
                loading={loading}
                errors={errors}
                hideButtons={hideButtons}
              />
            )}
          </div>
        </>
      )}

      {/* Form Actions - Only show if hideButtons is false or undefined */}
      {!hideButtons && (
        <div className={`px-6 py-4 bg-gray-50 border-t border-[#e5e7eb] ${verticalTabs ? 'ml-64' : ''}`}>
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-none hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-nexus-primary-500 focus:border-nexus-primary-500"
            >
              {cancelText}
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-nexus-primary-600 border border-transparent rounded-none hover:bg-nexus-primary-700 focus:outline-none focus:ring-2 focus:ring-nexus-primary-500 focus:ring-offset-2"
            >
              {submitText}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

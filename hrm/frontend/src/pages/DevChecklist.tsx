import React, { useState } from 'react'
import { CheckSquare, ClipboardList, Users, Palette, Database, TestTube, Rocket, Shield } from 'lucide-react'

interface ChecklistItem {
  id: string
  title: string
  items: {
    id: string
    label: string
    checked: boolean
    critical: boolean
  }[]
}

interface ChecklistSection {
  id: string
  title: string
  icon: React.ElementType
  color: string
  description: string
  items: ChecklistItem[]
}

export const DevChecklist: React.FC = () => {
  const [checklistData, setChecklistData] = useState<ChecklistSection[]>([
    {
      id: 'ui-foundation',
      title: 'UI Foundation & Olivine UI Canon Compliance',
      icon: Palette,
      color: 'text-purple-600',
      description: 'Typography, visual identity, layout structure, and accessibility compliance',
      items: [
        {
          id: 'typography',
          title: 'Typography & Visual Identity',
          items: [
            { id: 'font-implementation', label: 'Font Implementation: Use Inter font for UI/body text, JetBrains Mono for IDs/data', checked: false, critical: true },
            { id: 'font-sizes', label: 'Font Sizes: Apply text-sm for fields, text-xs for labels per governance', checked: false, critical: true },
            { id: 'color-tokens', label: 'Color Tokens: Implement nexus color palette consistently', checked: false, critical: true },
            { id: 'nexus-primary', label: 'nexus-primary-600 (#6d4de6) for primary actions/links', checked: false, critical: true },
            { id: 'nexus-primary-hover', label: 'nexus-primary-700 (#5d3dcb) for hover states', checked: false, critical: true },
            { id: 'nexus-gray-bg', label: 'nexus-gray-50 (#fafafa) for page backgrounds', checked: false, critical: true },
            { id: 'nexus-gray-panel', label: 'nexus-gray-100 (#f5f5f5) for panel backgrounds', checked: false, critical: true },
            { id: 'nexus-gray-text', label: 'nexus-gray-900 (#212121) for heavy text', checked: false, critical: true },
            { id: 'nexus-error', label: 'nexus-error-600 (#db2777) for validation errors', checked: false, critical: true },
            { id: 'nexus-success', label: 'nexus-success-600 (#059669) for success states', checked: false, critical: true },
          ]
        },
        {
          id: 'layout-structure',
          title: 'Layout Structure & Components',
          items: [
            { id: 'fixed-header', label: 'Fixed Header: Implement top-fixed header (h-16) with branding and user info', checked: false, critical: true },
            { id: 'sidebar-navigation', label: 'Sidebar Navigation: Create fixed left sidebar (w-64) with module menu', checked: false, critical: true },
            { id: 'main-content', label: 'Main Content Area: Configure main content with proper margins (ml-64 mt-16)', checked: false, critical: true },
            { id: 'transaction-toolbar', label: 'Transaction Toolbar: Add fixed toolbar with Save/Cancel/Reset/Workflow actions', checked: false, critical: true },
            { id: 'shape-system', label: 'Shape System: Apply rounded-none for inputs, rounded-sm for cards/buttons', checked: false, critical: true },
            { id: 'shadow-system', label: 'Shadow System: Use shadow-nexus-sm for cards, shadow-2xl for modals', checked: false, critical: true },
          ]
        },
        {
          id: 'responsive-accessibility',
          title: 'Responsive Design & Accessibility',
          items: [
            { id: 'mobile-compatibility', label: 'Mobile Compatibility: Ensure responsive design for mobile/tablet', checked: false, critical: true },
            { id: 'accessibility-compliance', label: 'Accessibility Compliance: Achieve WCAG 2.1 AA standards', checked: false, critical: true },
            { id: 'keyboard-navigation', label: 'Keyboard Navigation: Implement proper tab order and keyboard shortcuts', checked: false, critical: true },
            { id: 'screen-reader', label: 'Screen Reader Support: Add ARIA labels and semantic HTML', checked: false, critical: true },
            { id: 'color-contrast', label: 'Color Contrast: Verify sufficient contrast ratios per guidelines', checked: false, critical: true },
          ]
        }
      ]
    },
    {
      id: 'crud-operations',
      title: 'CRUD Operations Functionality',
      icon: Users,
      color: 'text-blue-600',
      description: 'Create, Read, Update, Delete operations with proper validation and error handling',
      items: [
        {
          id: 'create-operations',
          title: 'Create Operations',
          items: [
            { id: 'form-implementation', label: 'Form Implementation: Build forms based on Django model fields', checked: false, critical: true },
            { id: 'client-validation', label: 'Client-Side Validation: Add real-time form validation', checked: false, critical: true },
            { id: 'server-validation', label: 'Server-Side Validation: Implement backend validation rules', checked: false, critical: true },
            { id: 'error-handling', label: 'Error Handling: Display validation errors clearly', checked: false, critical: true },
            { id: 'success-feedback', label: 'Success Feedback: Show success messages/tokens after creation', checked: false, critical: true },
            { id: 'loading-states', label: 'Loading States: Implement loading indicators during submission', checked: false, critical: true },
          ]
        },
        {
          id: 'read-operations',
          title: 'Read Operations',
          items: [
            { id: 'data-grid', label: 'Data Grid Implementation: Create responsive data tables with sorting/filtering', checked: false, critical: true },
            { id: 'search-functionality', label: 'Search Functionality: Add search bars with real-time filtering', checked: false, critical: true },
            { id: 'pagination', label: 'Pagination: Implement pagination for large datasets', checked: false, critical: true },
            { id: 'data-display', label: 'Data Display: Format data appropriately (dates, numbers, etc.)', checked: false, critical: true },
            { id: 'empty-states', label: 'Empty States: Design empty state screens with helpful messages', checked: false, critical: true },
            { id: 'loading-skeletons', label: 'Loading Skeletons: Add skeleton screens during data loading', checked: false, critical: true },
          ]
        },
        {
          id: 'update-operations',
          title: 'Update Operations',
          items: [
            { id: 'edit-forms', label: 'Edit Forms: Implement edit functionality with pre-populated data', checked: false, critical: true },
            { id: 'inline-editing', label: 'Inline Editing: Add inline editing capabilities where appropriate', checked: false, critical: false },
            { id: 'batch-updates', label: 'Batch Updates: Support bulk update operations', checked: false, critical: false },
            { id: 'change-tracking', label: 'Change Tracking: Track and display field changes', checked: false, critical: true },
            { id: 'conflict-resolution', label: 'Conflict Resolution: Handle concurrent edit conflicts', checked: false, critical: true },
            { id: 'audit-trail', label: 'Audit Trail: Log all update operations', checked: false, critical: true },
          ]
        },
        {
          id: 'delete-operations',
          title: 'Delete Operations',
          items: [
            { id: 'delete-confirmation', label: 'Delete Confirmation: Implement confirmation dialogs with impact details', checked: false, critical: true },
            { id: 'soft-delete', label: 'Soft Delete: Use soft delete with audit trail where required', checked: false, critical: true },
            { id: 'batch-delete', label: 'Batch Delete: Support bulk deletion with proper warnings', checked: false, critical: true },
            { id: 'cascade-handling', label: 'Cascade Handling: Handle related record dependencies', checked: false, critical: true },
            { id: 'recovery-options', label: 'Recovery Options: Provide undo/recovery mechanisms', checked: false, critical: false },
            { id: 'cleanup-processes', label: 'Cleanup Processes: Implement proper data cleanup', checked: false, critical: true },
          ]
        }
      ]
    },
    {
      id: 'django-persistence',
      title: 'Django Persistence Verification',
      icon: Database,
      color: 'text-green-600',
      description: 'Model compliance, database operations, and API integration',
      items: [
        {
          id: 'model-compliance',
          title: 'Model Compliance',
          items: [
            { id: 'domain-ownership', label: 'Domain Ownership: Verify models belong to correct HRM domain', checked: false, critical: true },
            { id: 'company-references', label: 'Company References: Use lazy string reference: \'domain.Company\'', checked: false, critical: true },
            { id: 'audit-fields', label: 'Audit Fields: Ensure created_at, updated_at, created_by_user_id present', checked: false, critical: true },
            { id: 'indexes-constraints', label: 'Indexes & Constraints: Verify proper database indexes and constraints', checked: false, critical: true },
            { id: 'relationships', label: 'Relationships: Check foreign key relationships are properly defined', checked: false, critical: true },
            { id: 'validation-rules', label: 'Validation Rules: Implement model-level validation per BBP specifications', checked: false, critical: true },
          ]
        },
        {
          id: 'database-operations',
          title: 'Database Operations',
          items: [
            { id: 'migration-testing', label: 'Migration Testing: Verify migrations create and apply correctly', checked: false, critical: true },
            { id: 'crud-endpoints', label: 'CRUD Endpoints: Test all create, read, update, delete endpoints', checked: false, critical: true },
            { id: 'data-integrity', label: 'Data Integrity: Ensure no data loss during operations', checked: false, critical: true },
            { id: 'performance', label: 'Performance: Verify query performance with proper indexes', checked: false, critical: true },
            { id: 'transaction-safety', label: 'Transaction Safety: Ensure atomic transactions for complex operations', checked: false, critical: true },
            { id: 'backup-safety', label: 'Backup Safety: Verify data backup and recovery procedures', checked: false, critical: true },
          ]
        },
        {
          id: 'api-integration',
          title: 'API Integration',
          items: [
            { id: 'serializer-validation', label: 'Serializer Validation: Test serializer validation rules', checked: false, critical: true },
            { id: 'permission-checks', label: 'Permission Checks: Verify proper authentication and authorization', checked: false, critical: true },
            { id: 'error-responses', label: 'Error Responses: Test proper error handling and status codes', checked: false, critical: true },
            { id: 'data-formatting', label: 'Data Formatting: Ensure consistent API response formats', checked: false, critical: true },
            { id: 'rate-limiting', label: 'Rate Limiting: Implement appropriate rate limiting', checked: false, critical: true },
            { id: 'api-documentation', label: 'API Documentation: Maintain accurate API documentation', checked: false, critical: true },
          ]
        }
      ]
    },
    {
      id: 'testing-quality',
      title: 'Testing & Quality Assurance',
      icon: TestTube,
      color: 'text-orange-600',
      description: 'Unit testing, integration testing, and user acceptance testing',
      items: [
        {
          id: 'unit-testing',
          title: 'Unit Testing',
          items: [
            { id: 'model-tests', label: 'Model Tests: Test all model methods and validations', checked: false, critical: true },
            { id: 'view-tests', label: 'View Tests: Test all CRUD endpoints with various scenarios', checked: false, critical: true },
            { id: 'serializer-tests', label: 'Serializer Tests: Test serializer validation and data transformation', checked: false, critical: true },
            { id: 'utility-tests', label: 'Utility Tests: Test helper functions and utilities', checked: false, critical: true },
            { id: 'form-tests', label: 'Form Tests: Test form validation and processing', checked: false, critical: true },
            { id: 'service-tests', label: 'Service Tests: Test business logic in service layers', checked: false, critical: true },
          ]
        },
        {
          id: 'integration-testing',
          title: 'Integration Testing',
          items: [
            { id: 'end-to-end-workflows', label: 'End-to-End Workflows: Test complete user journeys', checked: false, critical: true },
            { id: 'api-integration', label: 'API Integration: Test frontend-backend integration', checked: false, critical: true },
            { id: 'database-integration', label: 'Database Integration: Test data persistence and retrieval', checked: false, critical: true },
            { id: 'cross-module-testing', label: 'Cross-Module Testing: Verify no cross-app imports or dependencies', checked: false, critical: true },
            { id: 'permission-testing', label: 'Permission Testing: Test role-based access control', checked: false, critical: true },
            { id: 'performance-testing', label: 'Performance Testing: Test under load conditions', checked: false, critical: true },
          ]
        },
        {
          id: 'user-acceptance-testing',
          title: 'User Acceptance Testing',
          items: [
            { id: 'usability-testing', label: 'Usability Testing: Verify intuitive user interface', checked: false, critical: true },
            { id: 'workflow-testing', label: 'Workflow Testing: Test real-world usage scenarios', checked: false, critical: true },
            { id: 'browser-compatibility', label: 'Browser Compatibility: Test across supported browsers', checked: false, critical: true },
            { id: 'device-testing', label: 'Device Testing: Test on various screen sizes', checked: false, critical: true },
            { id: 'accessibility-testing', label: 'Accessibility Testing: Verify screen reader compatibility', checked: false, critical: true },
            { id: 'error-scenario-testing', label: 'Error Scenario Testing: Test error handling and recovery', checked: false, critical: true },
          ]
        }
      ]
    },
    {
      id: 'deployment-monitoring',
      title: 'Deployment & Monitoring',
      icon: Rocket,
      color: 'text-indigo-600',
      description: 'Production readiness, environment configuration, and monitoring setup',
      items: [
        {
          id: 'production-readiness',
          title: 'Production Readiness',
          items: [
            { id: 'environment-configuration', label: 'Environment Configuration: Set up production settings', checked: false, critical: true },
            { id: 'database-configuration', label: 'Database Configuration: Configure production database connections', checked: false, critical: true },
            { id: 'static-files', label: 'Static Files: Configure static file serving and CDN', checked: false, critical: true },
            { id: 'security-headers', label: 'Security Headers: Implement security headers and HTTPS', checked: false, critical: true },
            { id: 'performance-optimization', label: 'Performance Optimization: Enable caching and compression', checked: false, critical: true },
            { id: 'backup-procedures', label: 'Backup Procedures: Implement automated backup systems', checked: false, critical: true },
          ]
        },
        {
          id: 'monitoring-logging',
          title: 'Monitoring & Logging',
          items: [
            { id: 'error-logging', label: 'Error Logging: Configure comprehensive error logging', checked: false, critical: true },
            { id: 'performance-monitoring', label: 'Performance Monitoring: Set up application performance monitoring', checked: false, critical: true },
            { id: 'user-analytics', label: 'User Analytics: Implement user behavior tracking', checked: false, critical: true },
            { id: 'health-checks', label: 'Health Checks: Configure application health endpoints', checked: false, critical: true },
            { id: 'alert-systems', label: 'Alert Systems: Set up alerting for critical issues', checked: false, critical: true },
            { id: 'audit-logging', label: 'Audit Logging: Maintain comprehensive audit trails', checked: false, critical: true },
          ]
        }
      ]
    },
    {
      id: 'governance-compliance',
      title: 'Governance Compliance',
      icon: Shield,
      color: 'text-red-600',
      description: 'Platform.cline compliance, quality gates, and governance validation',
      items: [
        {
          id: 'platform-cline-compliance',
          title: 'Platform.cline Compliance',
          items: [
            { id: 'governance-rules', label: 'Governance Rules: Follow 01_governance.md rules strictly', checked: false, critical: true },
            { id: 'development-stability', label: 'Development Stability: Follow 02_development_guide.md best practices', checked: false, critical: true },
            { id: 'domain-ownership', label: 'Domain Ownership: Maintain proper HRM domain boundaries', checked: false, critical: true },
            { id: 'mergeability-contract', label: 'Mergeability Contract: Ensure COPY→PASTE→RUN works', checked: false, critical: true },
            { id: 'no-cross-app-imports', label: 'No Cross-App Imports: Verify complete module isolation', checked: false, critical: true },
            { id: 'ui-canon-compliance', label: 'UI Canon Compliance: Follow Olivine UI canon exactly', checked: false, critical: true },
          ]
        },
        {
          id: 'quality-gates',
          title: 'Quality Gates',
          items: [
            { id: 'code-review', label: 'Code Review: Complete peer review process', checked: false, critical: true },
            { id: 'security-review', label: 'Security Review: Pass security vulnerability assessment', checked: false, critical: true },
            { id: 'performance-review', label: 'Performance Review: Meet performance benchmarks', checked: false, critical: true },
            { id: 'documentation-review', label: 'Documentation Review: Ensure complete documentation', checked: false, critical: true },
            { id: 'testing-coverage', label: 'Testing Coverage: Achieve >80% test coverage', checked: false, critical: true },
            { id: 'deployment-approval', label: 'Deployment Approval: Get deployment approval from stakeholders', checked: false, critical: true },
          ]
        }
      ]
    }
  ])

  const handleItemCheck = (sectionId: string, itemId: string, itemSubId: string) => {
    setChecklistData(prev => prev.map(section => {
      if (section.id === sectionId) {
        return {
          ...section,
          items: section.items.map(item => {
            if (item.id === itemId) {
              return {
                ...item,
                items: item.items.map(subItem => {
                  if (subItem.id === itemSubId) {
                    return { ...subItem, checked: !subItem.checked }
                  }
                  return subItem
                })
              }
            }
            return item
          })
        }
      }
      return section
    }))
  }

  const calculateProgress = (items: ChecklistItem[]) => {
    const totalItems = items.reduce((acc, item) => acc + item.items.length, 0)
    const checkedItems = items.reduce((acc, item) => 
      acc + item.items.filter(subItem => subItem.checked).length, 0
    )
    return totalItems > 0 ? Math.round((checkedItems / totalItems) * 100) : 0
  }

  const getCriticalItems = (items: ChecklistItem[]) => {
    return items.reduce((acc, item) => 
      acc + item.items.filter(subItem => subItem.critical && !subItem.checked).length, 0
    )
  }

  const overallProgress = Math.round(
    checklistData.reduce((acc, section) => acc + calculateProgress(section.items), 0) / checklistData.length
  )

  const totalCriticalItems = checklistData.reduce((acc, section) => acc + getCriticalItems(section.items), 0)

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 -mx-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Development Checklist</h1>
            <p className="text-sm text-gray-500 mt-1">
              Comprehensive UI development checklist for HRM module implementation
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900">{overallProgress}%</div>
              <div className="text-xs text-gray-500">Overall Progress</div>
            </div>
            {totalCriticalItems > 0 && (
              <div className="text-right">
                <div className="text-lg font-semibold text-red-600">{totalCriticalItems}</div>
                <div className="text-xs text-gray-500">Critical Items</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Overall Completion</span>
          <span className="text-sm text-gray-500">{overallProgress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${overallProgress}%` }}
          />
        </div>
      </div>

      {/* Checklist Sections */}
      <div className="space-y-6">
        {checklistData.map((section) => {
          const Icon = section.icon
          const sectionProgress = calculateProgress(section.items)
          const criticalItems = getCriticalItems(section.items)

          return (
            <div key={section.id} className="bg-white rounded-lg border border-gray-200">
              {/* Section Header */}
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div className={`p-2 rounded-lg bg-gray-50 ${section.color}`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <div>
                      <h2 className="text-lg font-semibold text-gray-900">{section.title}</h2>
                      <p className="text-sm text-gray-500 mt-1">{section.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-gray-900">{sectionProgress}%</div>
                    {criticalItems > 0 && (
                      <div className="text-xs text-red-600">{criticalItems} critical</div>
                    )}
                  </div>
                </div>
              </div>

              {/* Section Content */}
              <div className="p-6 space-y-6">
                {section.items.map((item) => (
                  <div key={item.id}>
                    <h3 className="text-md font-medium text-gray-900 mb-4">{item.title}</h3>
                    <div className="space-y-3">
                      {item.items.map((subItem) => (
                        <div key={subItem.id} className="flex items-start gap-3">
                          <input
                            type="checkbox"
                            id={`${section.id}-${item.id}-${subItem.id}`}
                            checked={subItem.checked}
                            onChange={() => handleItemCheck(section.id, item.id, subItem.id)}
                            className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <label 
                            htmlFor={`${section.id}-${item.id}-${subItem.id}`}
                            className="flex-1 text-sm text-gray-700 cursor-pointer"
                          >
                            <span className={subItem.checked ? 'line-through text-gray-400' : ''}>
                              {subItem.label}
                            </span>
                            {subItem.critical && (
                              <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                Critical
                              </span>
                            )}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <ClipboardList className="h-6 w-6 text-blue-600" />
          <h3 className="text-lg font-semibold text-blue-900">Development Summary</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <div className="text-2xl font-bold text-blue-600">{overallProgress}%</div>
            <div className="text-sm text-gray-600">Overall Progress</div>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <div className="text-2xl font-bold text-red-600">{totalCriticalItems}</div>
            <div className="text-sm text-gray-600">Critical Items Remaining</div>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <div className="text-2xl font-bold text-green-600">
              {checklistData.length}
            </div>
            <div className="text-sm text-gray-600">Sections Completed</div>
          </div>
        </div>
      </div>
    </div>
  )
}

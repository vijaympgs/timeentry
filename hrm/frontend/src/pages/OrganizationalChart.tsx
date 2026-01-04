import React, { useState, useEffect } from 'react'
import { ChevronRight, ChevronDown, Plus, Edit, Trash2, Users, Building, User } from 'lucide-react'

// Types
interface OrganizationalUnit {
  id: string
  name: string
  code: string
  unit_type: string
  level: number
  is_active: boolean
  parent_unit_id: string | null
  manager_id: string | null
  children: OrganizationalUnit[]
  employee_count: number
  positions?: Position[]
}

interface Position {
  id: string
  title: string
  position_code: string
  job_grade: string
  is_manager_position: boolean
  headcount: number
  filled_count: number
  vacancy_count: number
  employees: Employee[]
}

interface Employee {
  id: string
  name: string
  assignment_type: string
  is_primary: boolean
}

const OrganizationalChart: React.FC = () => {
  const [data, setData] = useState<OrganizationalUnit[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  const [selectedUnit, setSelectedUnit] = useState<OrganizationalUnit | null>(null)
  const [viewType, setViewType] = useState<'tree' | 'box' | 'list'>('tree')

  // Olivine UI Canon colors
  const nexusColors = {
    primary: '#6d4de6',
    primaryHover: '#5d3dcb',
    gray50: '#fafafa',
    gray100: '#f5f5f5',
    gray200: '#e5e7eb',
    gray300: '#d1d5db',
    gray600: '#4b5563',
    gray700: '#374151',
    gray900: '#212121',
    success: '#059669',
    error: '#db2777'
  }

  useEffect(() => {
    fetchOrganizationalChart()
  }, [])

  const fetchOrganizationalChart = async () => {
    try {
      setLoading(true)
      // Call real API to get org chart from Employee Records
      const response = await fetch(`http://localhost:8000/api/organizational-chart/chart/`)
      if (!response.ok) {
        throw new Error('Failed to fetch organizational chart')
      }
      
      const orgData = await response.json()
      
      // Transform employee hierarchy to tree structure for display
      const transformEmployeeData = (hierarchy: any[]): OrganizationalUnit[] => {
        return hierarchy.map(emp => ({
          id: emp.id,
          name: emp.name,
          code: emp.employee_id,
          unit_type: emp.is_manager ? 'manager' : 'employee',
          level: emp.level,
          is_active: true,
          parent_unit_id: null,
          manager_id: null,
          employee_count: 1,
          children: transformEmployeeData(emp.direct_reports || [])
        }))
      }
      
      setData(transformEmployeeData(orgData.hierarchy || []))
    } catch (err) {
      setError('Failed to load organizational chart')
    } finally {
      setLoading(false)
    }
  }

  const toggleNode = (nodeId: string) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId)
    } else {
      newExpanded.add(nodeId)
    }
    setExpandedNodes(newExpanded)
  }

  const getUnitTypeIcon = (unitType: string) => {
    switch (unitType) {
      case 'company':
        return <Building className="w-4 h-4" />
      case 'department':
        return <Users className="w-4 h-4" />
      case 'team':
        return <User className="w-4 h-4" />
      default:
        return <Building className="w-4 h-4" />
    }
  }

  const getUnitTypeColor = (unitType: string) => {
    switch (unitType) {
      case 'company':
        return nexusColors.primary
      case 'department':
        return nexusColors.success
      case 'team':
        return nexusColors.gray600
      default:
        return nexusColors.gray600
    }
  }

  const renderTreeNode = (unit: OrganizationalUnit, level: number = 0) => {
    const isExpanded = expandedNodes.has(unit.id)
    const hasChildren = unit.children && unit.children.length > 0
    const indent = level * 24

    return (
      <div key={unit.id} className="select-none">
        <div
          className="flex items-center py-2 px-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100"
          style={{ paddingLeft: `${indent + 12}px` }}
          onClick={() => {
            if (hasChildren) toggleNode(unit.id)
            setSelectedUnit(unit)
          }}
        >
          {hasChildren && (
            <div className="mr-2">
              {isExpanded ? (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronRight className="w-4 h-4 text-gray-500" />
              )}
            </div>
          )}
          
          <div
            className="mr-2 p-1 rounded"
            style={{ backgroundColor: `${getUnitTypeColor(unit.unit_type)}20` }}
          >
            {getUnitTypeIcon(unit.unit_type)}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <div>
                <span className="font-medium text-sm" style={{ color: nexusColors.gray900 }}>
                  {unit.name}
                </span>
                <span className="ml-2 text-xs" style={{ color: nexusColors.gray600 }}>
                  ({unit.code})
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-xs px-2 py-1 rounded" style={{ 
                  backgroundColor: `${getUnitTypeColor(unit.unit_type)}20`,
                  color: getUnitTypeColor(unit.unit_type)
                }}>
                  {unit.unit_type}
                </span>
                <span className="text-xs" style={{ color: nexusColors.gray600 }}>
                  {unit.employee_count} employees
                </span>
              </div>
            </div>
          </div>
        </div>
        
        {hasChildren && isExpanded && (
          <div>
            {unit.children.map(child => renderTreeNode(child, level + 1))}
          </div>
        )}
      </div>
    )
  }

  const renderTreeView = () => (
    <div className="bg-white rounded-sm shadow-nexus-sm">
      <div className="border-b border-gray-200 p-4">
        <h3 className="text-lg font-semibold" style={{ color: nexusColors.gray900 }}>
          Organizational Hierarchy
        </h3>
      </div>
      <div className="max-h-96 overflow-y-auto">
        {data.length > 0 ? (
          data.map(unit => renderTreeNode(unit))
        ) : (
          <div className="p-8 text-center" style={{ color: nexusColors.gray600 }}>
            No organizational units found
          </div>
        )}
      </div>
    </div>
  )

  const renderBoxView = () => (
    <div className="bg-white rounded-sm shadow-nexus-sm p-6">
      <h3 className="text-lg font-semibold mb-4" style={{ color: nexusColors.gray900 }}>
        Box Chart View
      </h3>
      <div className="text-center py-8" style={{ color: nexusColors.gray600 }}>
        Box chart view coming soon
      </div>
    </div>
  )

  const renderListView = () => (
    <div className="bg-white rounded-sm shadow-nexus-sm">
      <div className="border-b border-gray-200 p-4">
        <h3 className="text-lg font-semibold" style={{ color: nexusColors.gray900 }}>
          List View
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Code
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Level
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Employees
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map(unit => (
              <tr key={unit.id} className="hover:bg-gray-50">
                <td className="px-4 py-2 text-sm" style={{ color: nexusColors.gray900 }}>
                  {unit.name}
                </td>
                <td className="px-4 py-2 text-sm" style={{ color: nexusColors.gray600 }}>
                  {unit.code}
                </td>
                <td className="px-4 py-2 text-sm">
                  <span className="text-xs px-2 py-1 rounded" style={{ 
                    backgroundColor: `${getUnitTypeColor(unit.unit_type)}20`,
                    color: getUnitTypeColor(unit.unit_type)
                  }}>
                    {unit.unit_type}
                  </span>
                </td>
                <td className="px-4 py-2 text-sm" style={{ color: nexusColors.gray600 }}>
                  {unit.level}
                </td>
                <td className="px-4 py-2 text-sm" style={{ color: nexusColors.gray600 }}>
                  {unit.employee_count}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2" style={{ borderColor: nexusColors.primary }}></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-sm p-4">
        <div className="flex">
          <div className="text-sm" style={{ color: nexusColors.error }}>
            {error}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6" style={{ backgroundColor: nexusColors.gray50 }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: nexusColors.gray900 }}>
            Organizational Chart
          </h1>
          <p className="text-sm mt-1" style={{ color: nexusColors.gray600 }}>
            Manage your company's organizational structure
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* View Type Selector */}
          <div className="flex bg-white rounded-sm border border-gray-200">
            <button
              onClick={() => setViewType('tree')}
              className={`px-3 py-2 text-sm font-medium rounded-sm ${
                viewType === 'tree' 
                  ? 'text-white' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              style={{ 
                backgroundColor: viewType === 'tree' ? nexusColors.primary : 'transparent'
              }}
            >
              Tree
            </button>
            <button
              onClick={() => setViewType('box')}
              className={`px-3 py-2 text-sm font-medium rounded-sm ${
                viewType === 'box' 
                  ? 'text-white' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              style={{ 
                backgroundColor: viewType === 'box' ? nexusColors.primary : 'transparent'
              }}
            >
              Box
            </button>
            <button
              onClick={() => setViewType('list')}
              className={`px-3 py-2 text-sm font-medium rounded-sm ${
                viewType === 'list' 
                  ? 'text-white' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              style={{ 
                backgroundColor: viewType === 'list' ? nexusColors.primary : 'transparent'
              }}
            >
              List
            </button>
          </div>
          
          {/* Action Buttons */}
          <button
            className="flex items-center px-4 py-2 text-sm font-medium text-white rounded-sm hover:opacity-90"
            style={{ backgroundColor: nexusColors.primary }}
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Unit
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tree View */}
        <div className="lg:col-span-2">
          {viewType === 'tree' && renderTreeView()}
          {viewType === 'box' && renderBoxView()}
          {viewType === 'list' && renderListView()}
        </div>

        {/* Details Panel */}
        <div className="lg:col-span-1">
          {selectedUnit ? (
            <div className="bg-white rounded-sm shadow-nexus-sm p-6">
              <h3 className="text-lg font-semibold mb-4" style={{ color: nexusColors.gray900 }}>
                Unit Details
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-medium" style={{ color: nexusColors.gray600 }}>
                    Name
                  </label>
                  <p className="text-sm" style={{ color: nexusColors.gray900 }}>
                    {selectedUnit.name}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium" style={{ color: nexusColors.gray600 }}>
                    Code
                  </label>
                  <p className="text-sm" style={{ color: nexusColors.gray900 }}>
                    {selectedUnit.code}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium" style={{ color: nexusColors.gray600 }}>
                    Type
                  </label>
                  <p className="text-sm">
                    <span className="text-xs px-2 py-1 rounded" style={{ 
                      backgroundColor: `${getUnitTypeColor(selectedUnit.unit_type)}20`,
                      color: getUnitTypeColor(selectedUnit.unit_type)
                    }}>
                      {selectedUnit.unit_type}
                    </span>
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium" style={{ color: nexusColors.gray600 }}>
                    Level
                  </label>
                  <p className="text-sm" style={{ color: nexusColors.gray900 }}>
                    {selectedUnit.level}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium" style={{ color: nexusColors.gray600 }}>
                    Employees
                  </label>
                  <p className="text-sm" style={{ color: nexusColors.gray900 }}>
                    {selectedUnit.employee_count}
                  </p>
                </div>
                
                <div className="pt-4 border-t border-gray-200">
                  <div className="flex space-x-2">
                    <button
                      className="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium text-white rounded-sm"
                      style={{ backgroundColor: nexusColors.primary }}
                    >
                      <Edit className="w-4 h-4 mr-2" />
                      Edit
                    </button>
                    <button
                      className="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium text-white rounded-sm"
                      style={{ backgroundColor: nexusColors.error }}
                    >
                      <Trash2 className="w-4 h-4 mr-2" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-sm shadow-nexus-sm p-6">
              <div className="text-center py-8" style={{ color: nexusColors.gray600 }}>
                Select a unit to view details
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default OrganizationalChart

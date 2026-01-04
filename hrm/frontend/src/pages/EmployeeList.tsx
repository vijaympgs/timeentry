import React, { useState, useEffect } from 'react'
import { DataTable, SearchFilter, FormModal, ConfirmModal, WorkspaceFormModal, Toolbar, ToolbarButtons } from '../components/ui'
import { EmployeeForm } from './EmployeeForm'
import { Users, Plus, Edit, Trash2, Eye, Download, Upload, Filter } from 'lucide-react'

interface Employee {
  id: string
  employeeId: string
  firstName: string
  lastName: string
  email: string
  phone: string
  department: string
  position: string
  status: 'Active' | 'Inactive' | 'On Leave'
  hireDate: string
  salary: number
  manager: string
  location: string
}

export const EmployeeList: React.FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(false)
  const [searchValue, setSearchValue] = useState('')
  const [filters, setFilters] = useState<Record<string, any>>({})
  const [selectedEmployees, setSelectedEmployees] = useState<Employee[]>([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [showBulkDeleteModal, setShowBulkDeleteModal] = useState(false)
  const [currentEmployee, setCurrentEmployee] = useState<Employee | null>(null)
  const [formLoading, setFormLoading] = useState(false)
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
    total: 0
  })


  useEffect(() => {
    loadEmployees()
  }, [searchValue, filters, pagination.current])

  const loadEmployees = async () => {
    setLoading(true)
    try {
      // Call real API to get employee data
      const response = await fetch('http://localhost:8000/api/employees/')
      
      if (!response.ok) {
        throw new Error('Failed to fetch employees')
      }
          
      const data = await response.json()
          
      // Transform API data to match Employee interface
      const transformedEmployees: Employee[] = data.map((emp: any) => ({
        id: emp.id,
        employeeId: emp.employee_number,
        firstName: emp.first_name,
        lastName: emp.last_name,
        email: emp.work_email,
        phone: emp.work_phone || emp.mobile_phone,
        department: emp.department_name || 'Unassigned',
        position: emp.position_title,
        status: emp.is_active ? 'Active' : 'Inactive',
        hireDate: emp.hire_date,
        salary: parseFloat(emp.annual_salary) || 0,
        manager: emp.manager_name || 'None',
        location: 'Office' // Can be added to model if needed
      }))

      // Apply search filter
      let filteredEmployees = transformedEmployees
      if (searchValue) {
        filteredEmployees = filteredEmployees.filter(emp =>
          emp.firstName.toLowerCase().includes(searchValue.toLowerCase()) ||
          emp.lastName.toLowerCase().includes(searchValue.toLowerCase()) ||
          emp.email.toLowerCase().includes(searchValue.toLowerCase()) ||
          emp.employeeId.toLowerCase().includes(searchValue.toLowerCase())
        )
      }

      // Apply other filters
      if (filters.department) {
        filteredEmployees = filteredEmployees.filter(emp => emp.department === filters.department)
      }

      if (filters.status) {
        filteredEmployees = filteredEmployees.filter(emp => emp.status === filters.status)
      }

      // Client-side pagination
      const startIndex = (pagination.current - 1) * pagination.pageSize
      const endIndex = startIndex + pagination.pageSize
      const paginatedEmployees = filteredEmployees.slice(startIndex, endIndex)

      setEmployees(paginatedEmployees)
      setPagination(prev => ({ ...prev, total: filteredEmployees.length }))
    } catch (error) {
      console.error('Failed to load employees:', error)
      setEmployees([])
    } finally {
      setLoading(false)
    }
  }

  const handleAddEmployee = () => {
    setCurrentEmployee(null)
    setShowAddModal(true)
  }

  const handleEditEmployee = (employee: Employee) => {
    setCurrentEmployee(employee)
    setShowEditModal(true)
  }

  const handleDeleteEmployee = (employee: Employee) => {
    setCurrentEmployee(employee)
    setShowDeleteModal(true)
  }

  const handleViewEmployee = (employee: Employee) => {
    // Navigate to employee profile page
    console.log('View employee:', employee)
  }

  const handleBulkDelete = () => {
    if (selectedEmployees.length > 0) {
      setShowBulkDeleteModal(true)
    }
  }

  const confirmDelete = () => {
    if (currentEmployee) {
      setEmployees(prev => prev.filter(emp => emp.id !== currentEmployee.id))
      setShowDeleteModal(false)
      setCurrentEmployee(null)
    }
  }

  const confirmBulkDelete = () => {
    const deletedIds = selectedEmployees.map(emp => emp.id)
    setEmployees(prev => prev.filter(emp => !deletedIds.includes(emp.id)))
    setSelectedEmployees([])
    setShowBulkDeleteModal(false)
  }

  const handleExport = () => {
    // Export functionality
    console.log('Export employees')
  }

  const handleImport = () => {
    // Import functionality
    console.log('Import employees')
  }

  const columns = [
    {
      key: 'employeeId',
      title: 'ID',
      dataIndex: 'employeeId' as keyof Employee,
      sortable: true,
      width: '80px'
    },
    {
      key: 'name',
      title: 'Name',
      dataIndex: 'firstName' as keyof Employee,
      sortable: true,
      render: (value: any, record: Employee) => (
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-xs font-medium text-blue-600">
              {record.firstName.charAt(0)}{record.lastName.charAt(0)}
            </span>
          </div>
          <div>
            <div className="font-medium text-gray-900">
              {record.firstName} {record.lastName}
            </div>
            <div className="text-xs text-gray-500">{record.email}</div>
          </div>
        </div>
      )
    },
    {
      key: 'department',
      title: 'Department',
      dataIndex: 'department' as keyof Employee,
      sortable: true,
      width: '140px'
    },
    {
      key: 'position',
      title: 'Position',
      dataIndex: 'position' as keyof Employee,
      sortable: true,
      width: '180px'
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status' as keyof Employee,
      sortable: true,
      width: '100px',
      render: (value: string) => {
        const statusColors = {
          'Active': 'bg-green-100 text-green-800',
          'Inactive': 'bg-red-100 text-red-800',
          'On Leave': 'bg-yellow-100 text-yellow-800'
        }
        return (
          <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${statusColors[value as keyof typeof statusColors]}`}>
            {value}
          </span>
        )
      }
    },
    {
      key: 'hireDate',
      title: 'DOJ',
      dataIndex: 'hireDate' as keyof Employee,
      sortable: true,
      width: '120px'
    },
  ]

  const filterFields = [
    {
      name: 'department',
      label: 'Department',
      type: 'select' as const,
      options: [
        { value: 'Engineering', label: 'Engineering' },
        { value: 'HR', label: 'HR' },
        { value: 'Finance', label: 'Finance' },
        { value: 'Marketing', label: 'Marketing' },
        { value: 'Sales', label: 'Sales' }
      ]
    },
    {
      name: 'status',
      label: 'Status',
      type: 'select' as const,
      options: [
        { value: 'Active', label: 'Active' },
        { value: 'Inactive', label: 'Inactive' },
        { value: 'On Leave', label: 'On Leave' }
      ]
    },
    {
      name: 'location',
      label: 'Location',
      type: 'select' as const,
      options: [
        { value: 'New York', label: 'New York' },
        { value: 'San Francisco', label: 'San Francisco' },
        { value: 'Remote', label: 'Remote' }
      ]
    }
  ]

  return (
    <div className="h-full flex flex-col">
      {/* Page Title */}
      <div className="bg-white px-2 py-1">
        <h1 className="text-lg font-semibold text-gray-900">Employee Records</h1>
      </div>

      {/* VB.NET Style Toolbar */}
      <Toolbar
        buttons={[
          ...ToolbarButtons.crud({
            onNew: handleAddEmployee,
            onEdit: () => currentEmployee && handleEditEmployee(currentEmployee),
            onView: () => currentEmployee && handleViewEmployee(currentEmployee),
            onDelete: () => currentEmployee && handleDeleteEmployee(currentEmployee)
          }),
          ...ToolbarButtons.data({
            onRefresh: loadEmployees,
            onClear: () => {
              setFilters({})
              setSearchValue('')
              setSelectedEmployees([])
            },
            onExport: handleExport,
            onImport: handleImport
          })
        ]}
      />

      {/* Search and Filters - Match toolbar left margin */}
      <div className="px-2 py-1">
        <SearchFilter
          searchValue={searchValue}
          onSearchChange={setSearchValue}
          filters={filters}
          onFilterChange={(field, value) => setFilters(prev => ({ ...prev, [field]: value }))}
          filterFields={filterFields}
          onClearFilters={() => setFilters({})}
          onSearch={loadEmployees}
          loading={loading}
          placeholder="Search by name, email, or employee ID..."
        />
      </div>

      {/* Bulk Actions */}
      {selectedEmployees.length > 0 && (
        <div className="mx-2 mb-1 bg-blue-50 border border-blue-200 rounded p-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-blue-600" />
              <span className="text-xs font-medium text-blue-900">
                {selectedEmployees.length} employee{selectedEmployees.length > 1 ? 's' : ''} selected
              </span>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setSelectedEmployees([])}
                className="text-xs text-blue-600 hover:text-blue-700"
              >
                Clear Selection
              </button>
              <button
                onClick={handleBulkDelete}
                className="btn bg-red-600 text-white hover:bg-red-700 text-xs px-2 py-1"
              >
                <Trash2 className="h-3 w-3 mr-1" />
                Delete Selected
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Employee Table - Match toolbar left margin */}
      <div className="px-2 pb-2">
        <DataTable
          data={employees}
          columns={columns}
          onRowClick={handleViewEmployee}
          selectable={true}
          onSelectionChange={setSelectedEmployees}
          loading={loading}
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: pagination.total,
            onChange: (page, pageSize) => setPagination(prev => ({ ...prev, current: page, pageSize }))
          }}
        />
      </div>

      {/* Add Employee Modal */}
      <WorkspaceFormModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Employee"
        onSubmit={() => {}}
        onClear={() => {
          // Clear form logic here
          console.log('Clear form')
        }}
        loading={formLoading}
        workspaceIdentifier="C"
      >
        <EmployeeForm
          onSubmit={(data) => {
            setFormLoading(true)
            setTimeout(() => {
              const newEmployee = {
                id: Date.now().toString(),
                employeeId: data.employeeNumber,
                firstName: data.firstName,
                lastName: data.lastName,
                email: data.workEmail,
                phone: data.workPhone,
                department: data.departmentName,
                position: data.positionTitle,
                status: data.employmentStatus === 'ACTIVE' ? 'Active' as const : 
                       data.employmentStatus === 'ON_LEAVE' ? 'On Leave' as const : 
                       data.employmentStatus === 'TERMINATED' ? 'Inactive' as const : 'Active' as const,
                hireDate: data.hireDate,
                salary: parseInt(data.annualSalary) || 0,
                manager: data.managerName,
                location: data.workLocationName
              }
              setEmployees(prev => [...prev, newEmployee])
              setFormLoading(false)
              setShowAddModal(false)
            }, 1000)
          }}
          onCancel={() => setShowAddModal(false)}
          loading={formLoading}
        />
      </WorkspaceFormModal>

      {/* Edit Employee Modal */}
      <FormModal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        title="Edit Employee"
        onSubmit={() => {}}
        size="full"
        loading={formLoading}
      >
        <EmployeeForm
          employee={currentEmployee}
          onSubmit={(data) => {
            setFormLoading(true)
            setTimeout(() => {
              if (currentEmployee) {
                const updatedEmployee = {
                  ...currentEmployee,
                  employeeId: data.employeeNumber,
                  firstName: data.firstName,
                  lastName: data.lastName,
                  email: data.workEmail,
                  phone: data.workPhone,
                  department: data.departmentName,
                  position: data.positionTitle,
                  hireDate: data.hireDate,
                  salary: parseInt(data.annualSalary) || 0,
                  manager: data.managerName,
                  location: data.workLocationName
                }
                setEmployees(prev => prev.map(emp => emp.id === currentEmployee.id ? updatedEmployee : emp))
              }
              setFormLoading(false)
              setShowEditModal(false)
            }, 1000)
          }}
          onCancel={() => setShowEditModal(false)}
          loading={formLoading}
        />
      </FormModal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={confirmDelete}
        title="Delete Employee"
        message={`Are you sure you want to delete ${currentEmployee?.firstName} ${currentEmployee?.lastName}? This action cannot be undone.`}
        variant="danger"
      />

      {/* Bulk Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={showBulkDeleteModal}
        onClose={() => setShowBulkDeleteModal(false)}
        onConfirm={confirmBulkDelete}
        title="Delete Selected Employees"
        message={`Are you sure you want to delete ${selectedEmployees.length} selected employees? This action cannot be undone.`}
        variant="danger"
      />
    </div>
  )
}

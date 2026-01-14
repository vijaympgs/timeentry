import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Users, Search, Edit3, Trash2, Plus, Eye, User } from "lucide-react";
import { MasterToolbar, MasterMode } from "../components/ui/MasterToolbar";
import { EmployeeForm } from "./EmployeeForm";
import { employeeService, EmployeeListItem, EmployeeFilters, EmployeeDetail, EmployeeCreateData, EmployeeUpdateData } from "../services/employeeService";
import { useConfirmDialog } from "../components/ui/ConfirmDialog";
import { useLoadingState, LoadingSpinner, ErrorState, EmptyState } from "../components/ui/LoadingStates";

export const EmployeeRecords: React.FC = () => {
  const navigate = useNavigate();
  
  // State Management (Bootstrap-aligned naming)
  const [employees, setEmployees] = useState<EmployeeListItem[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<MasterMode>('VIEW');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [editingEmployee, setEditingEmployee] = useState<any>(null);
  const [useVerticalTabs, setUseVerticalTabs] = useState(true); // Config for vertical tabs
  const [filters, setFilters] = useState<EmployeeFilters>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [pagination, setPagination] = useState({
    currentPage: 1,
    pageSize: 10,
    totalCount: 0,
    hasNext: false,
    hasPrevious: false
  });

  // Hooks
  const { confirm, ConfirmDialog } = useConfirmDialog();
  const { isLoading, error, success, execute, reset } = useLoadingState();

  // Data Loading Function
  const loadData = async (page: number = 1) => {
    await execute(async () => {
      const resp = await employeeService.getEmployees(
        {
          ...filters,
          search: searchTerm || undefined,
        },
        page,
        pagination.pageSize
      );
      setEmployees(resp?.results || []);
      setPagination({
        currentPage: page,
        pageSize: pagination.pageSize,
        totalCount: resp?.count || 0,
        hasNext: !!resp?.next,
        hasPrevious: !!resp?.previous
      });
    }, {
      errorMessage: 'Failed to load employee records'
    });
  };

  // Pagination Handlers
  const handlePageChange = (newPage: number) => {
    loadData(newPage);
  };

  const handlePreviousPage = () => {
    if (pagination.currentPage > 1) {
      loadData(pagination.currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (pagination.hasNext) {
      loadData(pagination.currentPage + 1);
    }
  };

  const handlePageSizeChange = (newPageSize: number) => {
    setPagination(prev => ({ ...prev, pageSize: newPageSize }));
    loadData(1); // Reset to first page when changing page size
  };

  // Lifecycle Hooks
  useEffect(() => {
    loadData();
  }, [filters, searchTerm]);

  // Auto-select first record when data loads
  useEffect(() => {
    if (employees.length > 0 && !selectedId) {
      setSelectedId(employees[0].id);
    }
  }, [employees, selectedId]);

  // Toolbar Mode Management
  const getToolbarMode = (): MasterMode => {
    if (showForm) {
      return editingId ? 'EDIT' : 'CREATE';
    }
    // Employee Records Listing should use LIST mode (internally maps to VIEW)
    return 'VIEW'; // This will be shown as LIST in the toolbar display
  };

  // Navigation Handlers
  const handleFirstRecord = () => {
    if (pagination.currentPage > 1) {
      loadData(1);
      setSelectedId(employees[0]?.id || null);
    }
  };

  const handlePreviousRecord = () => {
    if (pagination.hasPrevious) {
      loadData(pagination.currentPage - 1);
      setSelectedId(employees[employees.length - 1]?.id || null);
    }
  };

  const handleNextRecord = () => {
    if (pagination.hasNext) {
      loadData(pagination.currentPage + 1);
      setSelectedId(employees[0]?.id || null);
    }
  };

  const handleLastRecord = () => {
    if (pagination.hasNext) {
      loadData(Math.ceil(pagination.totalCount / pagination.pageSize));
      setSelectedId(employees[employees.length - 1]?.id || null);
    }
  };

  // Workflow Handlers
  const handleAuthorize = async () => {
    if (!selectedId) return;
    
    const confirmed = await confirm({
      title: 'Authorize Employee',
      message: 'Are you sure you want to authorize this employee record?',
      confirmText: 'Authorize',
      cancelText: 'Cancel',
      type: 'warning'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate authorization API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
    }, {
      successMessage: 'Employee authorized successfully',
      errorMessage: 'Failed to authorize employee'
    });
  };

  const handleSubmit = async () => {
    if (!selectedId) return;
    
    const confirmed = await confirm({
      title: 'Submit Employee',
      message: 'Are you sure you want to submit this employee record for approval?',
      confirmText: 'Submit',
      cancelText: 'Cancel',
      type: 'info'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate submission API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
    }, {
      successMessage: 'Employee submitted for approval',
      errorMessage: 'Failed to submit employee'
    });
  };

  const handleReject = async () => {
    if (!selectedId) return;
    
    const confirmed = await confirm({
      title: 'Reject Employee',
      message: 'Are you sure you want to reject this employee record?',
      confirmText: 'Reject',
      cancelText: 'Cancel',
      type: 'danger'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate rejection API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
    }, {
      successMessage: 'Employee record rejected',
      errorMessage: 'Failed to reject employee'
    });
  };

  const handleAmend = async () => {
    if (!selectedId) return;
    
    const confirmed = await confirm({
      title: 'Amend Employee',
      message: 'Are you sure you want to amend this employee record?',
      confirmText: 'Amend',
      cancelText: 'Cancel',
      type: 'warning'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate amendment API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
    }, {
      successMessage: 'Employee record amended',
      errorMessage: 'Failed to amend employee'
    });
  };

  // Utility Handlers
  const handlePrint = () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    // Create print content
    const printContent = `
      EMPLOYEE RECORD
      ================
      Employee ID: ${employee.employee_number}
      Name: ${employee.first_name} ${employee.last_name}
      Email: ${employee.work_email}
      Department: ${employee.department_name}
      Position: ${employee.position_title}
      Status: ${employee.employment_status}
      Hire Date: ${new Date(employee.hire_date).toLocaleDateString()}
      
      Printed on: ${new Date().toLocaleString()}
    `;

    // Create print window
    const printWindow = window.open('', '', 'width=800,height=600');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Employee Record - ${employee.first_name} ${employee.last_name}</title>
            <style>
              body { font-family: monospace; white-space: pre-wrap; padding: 20px; }
            </style>
          </head>
          <body>${printContent}</body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  const handleEmail = () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    const subject = encodeURIComponent(`Employee Record: ${employee.first_name} ${employee.last_name}`);
    const body = encodeURIComponent(`
Employee Details:
- ID: ${employee.employee_number}
- Name: ${employee.first_name} ${employee.last_name}
- Email: ${employee.work_email}
- Department: ${employee.department_name}
- Position: ${employee.position_title}
- Status: ${employee.employment_status}
- Hire Date: ${new Date(employee.hire_date).toLocaleDateString()}

Please review the attached employee record.
    `);

    window.open(`mailto:?subject=${subject}&body=${body}`);
  };

  const handleClone = async () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    const confirmed = await confirm({
      title: 'Clone Employee',
      message: `Are you sure you want to create a clone of ${employee.first_name} ${employee.last_name}?`,
      confirmText: 'Clone',
      cancelText: 'Cancel',
      type: 'info'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate cloning API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
      loadData(); // Refresh to show cloned record
    }, {
      successMessage: 'Employee cloned successfully',
      errorMessage: 'Failed to clone employee'
    });
  };

  const handleGenerate = () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    // Generate report data
    const reportData = {
      employee: employee,
      generatedAt: new Date().toISOString(),
      reportType: 'Employee Record Summary'
    };

    // Create and download JSON report
    const dataStr = JSON.stringify(reportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `employee-record-${employee.employee_number}-${Date.now()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Tool Handlers
  const handleNotes = async () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    const confirmed = await confirm({
      title: 'Add Notes',
      message: `Add notes for ${employee.first_name} ${employee.last_name}?`,
      confirmText: 'Add Notes',
      cancelText: 'Cancel',
      type: 'info'
    });

    if (!confirmed) return;

    await execute(async () => {
      // Simulate notes API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      reset();
    }, {
      successMessage: 'Notes added successfully',
      errorMessage: 'Failed to add notes'
    });
  };

  const handleAttach = () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    if (!employee) return;

    // Create file input for attachment
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.accept = '.pdf,.doc,.docx,.jpg,.jpeg,.png';
    
    input.onchange = async (e) => {
      const files = (e.target as HTMLInputElement).files;
      if (!files || files.length === 0) return;

      await execute(async () => {
        // Simulate file upload
        await new Promise(resolve => setTimeout(resolve, 2000));
        reset();
      }, {
        successMessage: `${files.length} file(s) attached successfully`,
        errorMessage: 'Failed to attach files'
      });
    };
    
    input.click();
  };

  const handleHelp = () => {
    const helpContent = `
EMPLOYEE RECORDS HELP

Navigation:
• Use arrow keys or toolbar buttons to navigate between records
• Click on any record to select it
• Use search and filters to find specific employees

Actions:
• New: Create a new employee record
• Edit: Modify selected employee information
• Delete: Remove selected employee (with confirmation)
• Print: Print employee record
• Email: Send employee information via email
• Clone: Create a copy of selected employee
• Generate: Export employee data as JSON

Keyboard Shortcuts:
• F2: New Employee
• F3: Edit Employee
• F4: Delete Employee
• F5: Clear/Reset
• F7: View Employee
• F8: Save
• F9: Refresh
• F10: Authorize
• Ctrl+F: Search
• Ctrl+E: Export
• Ctrl+I: Import

For more help, contact the system administrator.
    `;

    const helpWindow = window.open('', '', 'width=600,height=400,scrollbars=yes');
    if (helpWindow) {
      helpWindow.document.write(`
        <html>
          <head>
            <title>Employee Records Help</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; white-space: pre-wrap; }
              h1 { color: #333; }
            </style>
          </head>
          <body><pre>${helpContent}</pre></body>
        </html>
      `);
      helpWindow.document.close();
    }
  };

  // Main Action Handler
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'new':
        setEditingId(null);
        setViewMode('CREATE');
        setShowForm(true);
        break;
      case 'edit':
        if (selectedId) {
          setEditingId(selectedId);
          setViewMode('EDIT');
          setShowForm(true);
        }
        break;
      case 'view':
        if (selectedId) {
          handleView(selectedId);
        }
        break;
      case 'profile':
        if (selectedId) {
          navigate(`/hrm/profile-view/${selectedId}`);
        }
        break;
      case 'delete':
        if (selectedId) {
          handleDelete();
        }
        break;
      case 'refresh':
        loadData();
        break;
      case 'search':
        // Focus on search input
        document.getElementById('employee-search')?.focus();
        break;
      case 'exit':
        // Return to employee listing
        setShowForm(false);
        setEditingId(null);
        setViewMode('VIEW');
        break;
      case 'save':
        // Trigger save from modal - this will be handled by the EmployeeForm component
        const form = document.querySelector('form[data-employee-form]') as HTMLFormElement;
        if (form) {
          const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
          form.dispatchEvent(submitEvent);
        }
        break;
      case 'cancel':
        setViewMode('VIEW');
        setShowForm(false);
        setEditingId(null);
        break;
      // Navigation Actions
      case 'first':
        handleFirstRecord();
        break;
      case 'prev':
        handlePreviousRecord();
        break;
      case 'next':
        handleNextRecord();
        break;
      case 'last':
        handleLastRecord();
        break;
      // Workflow Actions
      case 'authorize':
        handleAuthorize();
        break;
      case 'submit':
        handleSubmit();
        break;
      case 'reject':
        handleReject();
        break;
      case 'amend':
        handleAmend();
        break;
      // Utility Actions
      case 'print':
        handlePrint();
        break;
      case 'email':
        handleEmail();
        break;
      case 'clone':
        handleClone();
        break;
      case 'generate':
        handleGenerate();
        break;
      // Tool Actions
      case 'notes':
        handleNotes();
        break;
      case 'attach':
        handleAttach();
        break;
      case 'help':
        handleHelp();
        break;
      default:
        console.log('Unknown action:', action);
    }
  };

  const handleCreate = () => {
    setEditingId(null);
    setViewMode('CREATE');
    setShowForm(true);
  };

  const handleView = async (id: string) => {
    // First select the record if not already selected
    setSelectedId(id);
    
    setEditingId(id);
    setViewMode('VIEW_FORM');
    try {
      const employee = await employeeService.getEmployee(id);
      setEditingEmployee(employee);
      setShowForm(true);
    } catch (err) {
      reset();
      console.error(err);
    }
  };

  const handleEdit = async (id: string) => {
    setEditingId(id);
    setViewMode('EDIT');
    try {
      const employee = await employeeService.getEmployee(id);
      setEditingEmployee(employee);
      setShowForm(true);
    } catch (err) {
      reset();
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!selectedId) return;
    
    const employee = employees.find(emp => emp.id === selectedId);
    const employeeName = employee?.full_name || 'Unknown';
    
    const confirmed = await confirm({
      title: 'Delete Employee',
      message: `Are you sure you want to delete ${employeeName}? This action cannot be undone.`,
      confirmText: 'Delete',
      cancelText: 'Cancel',
      type: 'danger'
    });

    if (!confirmed) return;

    await execute(async () => {
      await employeeService.deleteEmployee(selectedId);
      setSelectedId(null);
      loadData();
    }, {
      successMessage: 'Employee deleted successfully',
      errorMessage: 'Failed to delete employee'
    });
  };

  const handleModalClose = (shouldRefresh?: boolean) => {
    setShowForm(false);
    setEditingId(null);
    setViewMode('VIEW');
    if (shouldRefresh) {
      loadData();
    }
  };

  const handleFilterChange = (key: keyof EmployeeFilters, value: any) => {
    setFilters({ ...filters, [key]: value || undefined });
  };

  const handleSearch = () => {
    setFilters({ ...filters, search: searchTerm || undefined });
  };

  const handleRowSelect = (id: string) => {
    setSelectedId(prev => prev === id ? null : id);
  };

  const handleSelectAll = () => {
    // For single selection mode, this doesn't apply
    // Keeping for compatibility but not used in single selection mode
  };

  // Helper Functions
  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      ACTIVE: 'bg-green-100 text-green-800',
      INACTIVE: 'bg-gray-100 text-gray-800',
      ON_LEAVE: 'bg-yellow-100 text-yellow-800',
      TERMINATED: 'bg-red-100 text-red-800',
    };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
        {status}
      </span>
    );
  };

  // Loading State
  if (isLoading && employees.length === 0) {
    return <LoadingSpinner size="lg" />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Confirmation Dialog */}
      <ConfirmDialog />
      
      {/* Master Toolbar */}
      <MasterToolbar 
        viewId="HRM_EMPLOYEE_MASTER" 
        mode={getToolbarMode()} 
        onAction={handleToolbarAction}
        hasSelection={!!selectedId}
      />

      {/* Page Header with Filters */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-6 py-3">
          {/* Line 1: Title and Controls */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Users className="w-8 h-8 text-blue-600" />
              <h1 className="text-lg font-bold text-gray-900">Employee Records</h1>
            </div>
            
            {/* Search and Filters in Header */}
            <div className="flex items-center space-x-3">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  id="employee-search"
                  type="text"
                  placeholder="Search employees..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                  className="pl-10 pr-4 py-2 w-64 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              {/* Department Filter */}
              <select
                value={filters.department_name || ''}
                onChange={(e) => handleFilterChange('department_name', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Departments</option>
                <option value="Engineering">Engineering</option>
                <option value="HR">Human Resources</option>
                <option value="Finance">Finance</option>
                <option value="Marketing">Marketing</option>
                <option value="Sales">Sales</option>
                <option value="Operations">Operations</option>
              </select>
              
              {/* Status Filter */}
              <select
                value={filters.employment_status || ''}
                onChange={(e) => handleFilterChange('employment_status', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Status</option>
                <option value="ACTIVE">Active</option>
                <option value="INACTIVE">Inactive</option>
                <option value="ON_LEAVE">On Leave</option>
                <option value="TERMINATED">Terminated</option>
              </select>
              
              {/* Record Count */}
              <div className="text-sm text-gray-600 font-medium">
                {pagination.totalCount}
              </div>
              
              {/* Pagination Controls in Header */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handlePreviousPage}
                  disabled={!pagination.hasPrevious}
                  className="px-3 py-1 text-sm border border-gray-300 rounded-md bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {"<"}
                </button>
                <span className="text-sm text-gray-700">
                  Page {pagination.currentPage}
                </span>
                <button
                  onClick={handleNextPage}
                  disabled={!pagination.hasNext}
                  className="px-3 py-1 text-sm border border-gray-300 rounded-md bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {">"}
                </button>
                <select
                  value={pagination.pageSize}
                  onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                  className="text-sm border border-gray-300 rounded-md"
                >
                  <option value={10}>10</option>
                  <option value={20}>20</option>
                  <option value={50}>50</option>
                  <option value={100}>100</option>
                </select>
              </div>
            </div>
          </div>
          
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="mx-6 mt-4 bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-sm text-red-600">{error}</div>
        </div>
      )}

      {/* Data Table */}
      <div className="bg-white overflow-hidden" style={{ maxHeight: 'calc(100vh - 300px)', overflowY: 'auto' }}>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-[#f3f2f1]">
              <tr>
                <th className="px-4 py-2 text-left">
                  {/* Single selection mode - no select all checkbox */}
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Department
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Position
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Hire Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {employees.map((employee) => (
              <tr 
                  key={employee.id} 
                  className={selectedId === employee.id ? 'bg-blue-50' : 'cursor-pointer hover:bg-gray-50'}
                  onClick={() => handleRowSelect(employee.id)}
              >
                  <td className="px-4 py-2 whitespace-nowrap">
                    <input
                      type="radio"
                      checked={selectedId === employee.id}
                      onChange={() => handleRowSelect(employee.id)}
                      className="border-gray-300"
                    />
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-mono text-gray-900">
                    {employee.employee_number}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {employee.first_name || employee.last_name ? 
                        `${employee.first_name || ''} ${employee.last_name || ''}`.trim() : 
                        'N/A'}
                    </div>
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                    {employee.work_email}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                    {employee.department_name}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                    {employee.position_title}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap">
                    {getStatusBadge(employee.employment_status)}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                    {new Date(employee.hire_date).toLocaleDateString('en-US', { 
                      month: 'numeric', 
                      day: 'numeric', 
                      year: 'numeric' 
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>


      {/* Empty State */}
      {employees.length === 0 && !isLoading && (
        <EmptyState
          title="No employees found"
          message="Get started by creating your first employee record."
          action={{
            text: "Add Employee",
            onClick: handleCreate
          }}
          icon={<Users className="mx-auto h-12 w-12 text-gray-400" />}
        />
      )}

      {/* Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-30 overflow-y-auto h-full w-full z-50">
          <div className="flex h-full pt-16 pb-8"> {/* Account for header (64px) and status bar (32px) */}
            {/* Sidebar space preserved */}
            <div className="w-64 flex-shrink-0"></div>
            
            {/* Full primary workspace */}
            <div className="flex-1 bg-white overflow-hidden flex flex-col">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">
                  {viewMode === 'VIEW_FORM' ? 'View Employee' : editingId ? 'Edit Employee' : 'Add New Employee'}
                </h3>
              </div>
              <div className="px-6 py-4 border-b border-gray-200">
                {viewMode === 'VIEW_FORM' ? (
                  <MasterToolbar 
                    viewId="HRM_EMPLOYEE_MASTER"
                    mode="VIEW_FORM"
                    onAction={handleToolbarAction}
                    hasSelection={false}
                  />
                ) : (
                  <MasterToolbar 
                    viewId="HRM_EMPLOYEE_MASTER"
                    mode={viewMode}
                    onAction={handleToolbarAction}
                    hasSelection={false}
                  />
                )}
              </div>
              <div className="p-6 overflow-y-auto flex-1">
                <EmployeeForm
                  employee={editingEmployee}
                  onSubmit={async (data: any) => {
                    await execute(async () => {
                      if (editingId) {
                        await employeeService.updateEmployee(editingId, data);
                      } else {
                        await employeeService.createEmployee(data);
                      }
                      handleModalClose(true);
                    }, {
                      successMessage: 'Employee saved successfully',
                      errorMessage: 'Failed to save employee'
                    });
                  }}
                  onCancel={() => handleModalClose()}
                  onToolbarAction={handleToolbarAction}
                  mode={viewMode === 'VIEW_FORM' ? 'CREATE' : viewMode as 'EDIT' | 'CREATE'}
                  hideButtons={true}
                  verticalTabs={useVerticalTabs}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

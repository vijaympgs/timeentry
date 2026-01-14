/**
 * Employee Service - Real API Integration
 * Following T1 Complex Master Template specifications
 * Replaces mock service with actual backend API calls
 */

// TypeScript Interfaces matching backend serializers
export interface EmployeeListItem {
  id: string;
  company_code: string;
  company_name?: string;
  employee_number: string;
  first_name: string;
  last_name: string;
  full_name: string;
  work_email: string;
  personal_email?: string;
  work_phone?: string;
  mobile_phone?: string;
  department_name: string;
  position_title: string;
  employment_status: 'ACTIVE' | 'ON_LEAVE' | 'TERMINATED' | 'RETIREMENT' | 'CONTRACT_END' | 'SUSPENDED';
  employment_type: 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'INTERN' | 'TEMPORARY' | 'SEASONAL' | 'CONSULTANT' | 'FREELANCER';
  is_active: boolean;
  hire_date: string;
  age?: number;
  years_of_service?: number;
  created_at: string;
  updated_at: string;
}

export interface EmployeeDetail extends EmployeeListItem {
  national_id?: string;
  social_security_number?: string;
  passport_number?: string;
  middle_name?: string;
  preferred_name?: string;
  name_prefix?: string;
  name_suffix?: string;
  gender: 'MALE' | 'FEMALE' | 'NON_BINARY' | 'PREFER_NOT_TO_SAY';
  date_of_birth: string;
  marital_status: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'SEPARATED' | 'WIDOWED' | 'DOMESTIC_PARTNERSHIP';
  home_phone?: string;
  original_hire_date?: string;
  job_category?: string;
  job_level?: string;
  job_family?: string;
  work_location_name?: string;
  remote_work_eligible: boolean;
  remote_work_percentage: number;
  manager_name?: string;
  hr_business_partner_name?: string;
  salary_grade?: string;
  salary_step?: string;
  annual_salary?: number;
  hourly_rate?: number;
  currency: string;
  pay_frequency: 'HOURLY' | 'WEEKLY' | 'BI_WEEKLY' | 'SEMI_MONTHLY' | 'MONTHLY' | 'ANNUAL';
  benefits_eligibility_date?: string;
  benefits_package_name?: string;
  health_insurance_eligible: boolean;
  dental_insurance_eligible: boolean;
  vision_insurance_eligible: boolean;
  retirement_plan_eligible: boolean;
  life_insurance_eligible: boolean;
  primary_emergency_contact_name?: string;
  primary_emergency_contact_relationship?: string;
  primary_emergency_contact_phone?: string;
  secondary_emergency_contact_name?: string;
  secondary_emergency_contact_relationship?: string;
  secondary_emergency_contact_phone?: string;
  is_confidential: boolean;
  is_key_employee: boolean;
  is_high_potential: boolean;
  termination_date?: string;
  termination_reason?: string;
  rehire_eligible: boolean;
  username: string;
  role: string;
  addresses?: EmployeeAddress[];
}

export interface EmployeeAddress {
  id: string;
  company_code: string;
  employee: string;
  address_type: 'HOME' | 'WORK' | 'MAILING' | 'TEMPORARY';
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_primary: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface EmployeeFilters {
  company_code?: string;
  department_name?: string;
  position_title?: string;
  employment_status?: string;
  employment_type?: string;
  is_active?: boolean;
  gender?: string;
  job_level?: string;
  search?: string;
  ordering?: string;
}

export interface EmployeeCreateData {
  employee_number: string;
  national_id?: string;
  social_security_number?: string;
  passport_number?: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  preferred_name?: string;
  name_prefix?: string;
  name_suffix?: string;
  gender: 'MALE' | 'FEMALE' | 'NON_BINARY' | 'PREFER_NOT_TO_SAY';
  date_of_birth: string;
  marital_status: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'SEPARATED' | 'WIDOWED' | 'DOMESTIC_PARTNERSHIP';
  work_email: string;
  personal_email?: string;
  work_phone?: string;
  mobile_phone?: string;
  home_phone?: string;
  hire_date: string;
  original_hire_date?: string;
  employment_status: 'ACTIVE' | 'ON_LEAVE' | 'TERMINATED' | 'RETIREMENT' | 'CONTRACT_END' | 'SUSPENDED';
  employment_type: 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'INTERN' | 'TEMPORARY' | 'SEASONAL' | 'CONSULTANT' | 'FREELANCER';
  position_title: string;
  department_name: string;
  job_category?: string;
  job_level?: string;
  job_family?: string;
  work_location_name?: string;
  remote_work_eligible: boolean;
  remote_work_percentage: number;
  manager_name?: string;
  hr_business_partner_name?: string;
  salary_grade?: string;
  salary_step?: string;
  annual_salary?: number;
  hourly_rate?: number;
  currency: string;
  pay_frequency: 'HOURLY' | 'WEEKLY' | 'BI_WEEKLY' | 'SEMI_MONTHLY' | 'MONTHLY' | 'ANNUAL';
  benefits_eligibility_date?: string;
  benefits_package_name?: string;
  health_insurance_eligible: boolean;
  dental_insurance_eligible: boolean;
  vision_insurance_eligible: boolean;
  retirement_plan_eligible: boolean;
  life_insurance_eligible: boolean;
  primary_emergency_contact_name?: string;
  primary_emergency_contact_relationship?: string;
  primary_emergency_contact_phone?: string;
  secondary_emergency_contact_name?: string;
  secondary_emergency_contact_relationship?: string;
  secondary_emergency_contact_phone?: string;
  is_active: boolean;
  is_confidential: boolean;
  is_key_employee: boolean;
  is_high_potential: boolean;
  username: string;
  role: string;
}

export interface EmployeeUpdateData extends Partial<EmployeeCreateData> {
  // All fields except employee_number and work_email can be updated
}

export interface EmployeeStatistics {
  total_employees: number;
  active_employees: number;
  inactive_employees: number;
  by_department: Record<string, number>;
  by_status: Record<string, number>;
  by_employment_type: Record<string, number>;
}

// API Client Configuration
const API_BASE_URL = 'http://localhost:8000/api/hrm/api/v1/';

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Helper function for API calls
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.error || errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// Employee Service Implementation
export const employeeService = {
  /**
   * Get all employees with optional filtering and pagination
   * Following T1 specifications for list operations
   */
  getEmployees: async (filters?: EmployeeFilters, page: number = 1, pageSize: number = 20): Promise<{ results: EmployeeListItem[]; count: number; next?: string; previous?: string }> => {
    const params = new URLSearchParams();
    
    if (filters?.company_code) params.append('company_code', filters.company_code);
    if (filters?.department_name) params.append('department_name', filters.department_name);
    if (filters?.position_title) params.append('position_title', filters.position_title);
    if (filters?.employment_status) params.append('employment_status', filters.employment_status);
    if (filters?.employment_type) params.append('employment_type', filters.employment_type);
    if (filters?.is_active !== undefined) params.append('is_active', filters.is_active.toString());
    if (filters?.gender) params.append('gender', filters.gender);
    if (filters?.job_level) params.append('job_level', filters.job_level);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.ordering) params.append('ordering', filters.ordering);
    
    // Add pagination
    params.append('page', page.toString());
    params.append('page_size', pageSize.toString());
    
    const queryString = params.toString();
    const endpoint = `employees/${queryString ? `?${queryString}` : ''}`;
    
    return apiCall<{ results: EmployeeListItem[]; count: number; next?: string; previous?: string }>(endpoint);
  },

  /**
   * Get single employee by ID
   * Following T1 specifications for detail operations
   */
  getEmployee: async (id: string): Promise<EmployeeDetail> => {
    return apiCall<EmployeeDetail>(`employees/${id}/`);
  },

  /**
   * Create new employee
   * Following T1 specifications for create operations
   */
  createEmployee: async (data: EmployeeCreateData): Promise<EmployeeDetail> => {
    return apiCall<EmployeeDetail>('employees/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update existing employee
   * Following T1 specifications for update operations
   */
  updateEmployee: async (id: string, data: EmployeeUpdateData): Promise<EmployeeDetail> => {
    return apiCall<EmployeeDetail>(`employees/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete employee
   * Following T1 specifications for delete operations
   */
  deleteEmployee: async (id: string): Promise<void> => {
    await apiCall<void>(`employees/${id}/`, {
      method: 'DELETE',
    });
  },

  /**
   * Get only active employees
   * Following T1 specifications for filtered views
   */
  getActiveEmployees: async (): Promise<EmployeeListItem[]> => {
    return apiCall<EmployeeListItem[]>('employees/active/');
  },

  /**
   * Get employees by department
   * Following T1 specifications for advanced filtering
   */
  getEmployeesByDepartment: async (department: string): Promise<EmployeeListItem[]> => {
    return apiCall<EmployeeListItem[]>(`employees/by_department/?department=${encodeURIComponent(department)}`);
  },

  /**
   * Get employees by status
   * Following T1 specifications for advanced filtering
   */
  getEmployeesByStatus: async (status: string): Promise<EmployeeListItem[]> => {
    return apiCall<EmployeeListItem[]>(`employees/by_status/?status=${encodeURIComponent(status)}`);
  },

  /**
   * Advanced search with multiple criteria
   * Following T1 specifications for complex filtering
   */
  searchEmployees: async (criteria: {
    name?: string;
    email?: string;
    department?: string;
    position?: string;
    is_active?: boolean;
  }): Promise<EmployeeListItem[]> => {
    const params = new URLSearchParams();
    
    if (criteria.name) params.append('name', criteria.name);
    if (criteria.email) params.append('email', criteria.email);
    if (criteria.department) params.append('department', criteria.department);
    if (criteria.position) params.append('position', criteria.position);
    if (criteria.is_active !== undefined) params.append('is_active', criteria.is_active.toString());

    const queryString = params.toString();
    return apiCall<EmployeeListItem[]>(`employees/search_advanced/${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Bulk update employee status
   * Following T1 specifications for bulk operations
   */
  bulkUpdateStatus: async (employeeIds: string[], newStatus: string): Promise<{ message: string; count: number }> => {
    return apiCall<{ message: string; count: number }>('employees/bulk_update_status/', {
      method: 'POST',
      body: JSON.stringify({
        employee_ids: employeeIds,
        status: newStatus,
      }),
    });
  },

  /**
   * Bulk activate employees
   * Following T1 specifications for bulk operations
   */
  bulkActivateEmployees: async (employeeIds: string[]): Promise<{ message: string; count: number }> => {
    return apiCall<{ message: string; count: number }>('employees/bulk_activate/', {
      method: 'POST',
      body: JSON.stringify({
        employee_ids: employeeIds,
      }),
    });
  },

  /**
   * Bulk deactivate employees
   * Following T1 specifications for bulk operations
   */
  bulkDeactivateEmployees: async (employeeIds: string[]): Promise<{ message: string; count: number }> => {
    return apiCall<{ message: string; count: number }>('employees/bulk_deactivate/', {
      method: 'POST',
      body: JSON.stringify({
        employee_ids: employeeIds,
      }),
    });
  },

  /**
   * Get employee addresses
   * Following T1 specifications for nested resource management
   */
  getEmployeeAddresses: async (employeeId: string): Promise<EmployeeAddress[]> => {
    return apiCall<EmployeeAddress[]>(`employees/${employeeId}/addresses/`);
  },

  /**
   * Create employee address
   * Following T1 specifications for nested resource management
   */
  createEmployeeAddress: async (employeeId: string, addressData: Omit<EmployeeAddress, 'id' | 'company_code' | 'employee' | 'created_at' | 'updated_at'>): Promise<EmployeeAddress> => {
    return apiCall<EmployeeAddress>(`employees/${employeeId}/addresses/`, {
      method: 'POST',
      body: JSON.stringify(addressData),
    });
  },

  /**
   * Update employee addresses
   * Following T1 specifications for nested resource management
   */
  updateEmployeeAddresses: async (employeeId: string, addresses: Omit<EmployeeAddress, 'id' | 'company_code' | 'employee' | 'created_at' | 'updated_at'>[]): Promise<EmployeeAddress[]> => {
    return apiCall<EmployeeAddress[]>(`employees/${employeeId}/addresses/`, {
      method: 'PUT',
      body: JSON.stringify({ addresses }),
    });
  },

  /**
   * Delete employee addresses
   * Following T1 specifications for nested resource management
   */
  deleteEmployeeAddresses: async (employeeId: string): Promise<void> => {
    await apiCall<void>(`employees/${employeeId}/addresses/`, {
      method: 'DELETE',
    });
  },

  /**
   * Get employee statistics
   * Following T1 specifications for analytics
   */
  getEmployeeStatistics: async (): Promise<EmployeeStatistics> => {
    return apiCall<EmployeeStatistics>('employees/statistics/');
  },

  /**
   * Get organizational hierarchy data for org chart
   */
  getHierarchy: async (): Promise<{
    hierarchy: OrgChartNode[];
    total_employees: number;
    levels: number;
  }> => {
    // Add cache-busting parameter
    const timestamp = new Date().getTime();
    return apiCall(`employees/hierarchy/?_t=${timestamp}`);
  },

  /**
   * Get employee profile data
   * Following Profile View specifications
   */
  getProfile: async (employeeId: string): Promise<any> => {
    return apiCall(`profiles/${employeeId}/`);
  },

  /**
   * Update employee profile
   * Following Profile View specifications
   */
  updateProfile: async (profileId: string, profileData: any): Promise<any> => {
    return apiCall(`profiles/${profileId}/`, {
      method: 'PATCH',
      body: JSON.stringify(profileData),
    });
  },

  /**
   * Get employee skills
   * Following Profile View specifications
   */
  getSkills: async (employeeId: string): Promise<any[]> => {
    return apiCall(`profiles/${employeeId}/skills/`);
  },

  /**
   * Get employee documents
   * Following Profile View specifications
   */
  getDocuments: async (employeeId: string): Promise<any[]> => {
    return apiCall(`profiles/${employeeId}/documents/`);
  },

  /**
   * Get employee by ID (alias for getEmployee)
   */
  getById: async (id: string): Promise<EmployeeDetail> => {
    return employeeService.getEmployee(id);
  },

  /**
   * Update employee manager
   * Following drag-and-drop reassignment specifications
   */
  updateManager: async (employeeId: string, managerId: string | null): Promise<any> => {
    return apiCall(`employees/${employeeId}/`, {
      method: 'PATCH',
      body: JSON.stringify({
        manager: managerId
      }),
    });
  },
};

export default employeeService;

// Additional interface for org chart nodes
export interface OrgChartNode {
  id: string;
  employee_number: string;
  first_name: string;
  last_name: string;
  full_name: string;
  position_title: string;
  department_name: string;
  work_email: string;
  manager_name: string;
  is_active: boolean;
  children: OrgChartNode[];
}

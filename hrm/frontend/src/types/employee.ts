export interface EmployeeRecord {
  id: string;
  employee_number?: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  work_email?: string;
  department_name?: string;
  position_title?: string;
  manager_name?: string;
  is_active?: boolean;
  [key: string]: any;
}

export interface EmployeeProfile {
  id: string;
  [key: string]: any;
}

export interface EmployeeSkill {
  id: string;
  [key: string]: any;
}

export interface EmployeeDocument {
  id: string;
  [key: string]: any;
}

// HRM Frontend TypeScript Types

export interface Employee {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  department?: string;
  position?: string;
  hireDate: string;
  status: 'active' | 'inactive' | 'terminated';
  avatar?: string;
}

export interface Department {
  id: string;
  name: string;
  description?: string;
  manager?: string;
  employeeCount: number;
}

export interface AttendanceRecord {
  id: string;
  employeeId: string;
  date: string;
  checkIn?: string;
  checkOut?: string;
  breakTime?: number;
  totalHours?: number;
  status: 'present' | 'absent' | 'late' | 'half-day';
}

export interface LeaveRequest {
  id: string;
  employeeId: string;
  leaveType: 'annual' | 'sick' | 'personal' | 'maternity' | 'paternity';
  startDate: string;
  endDate: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  approvedBy?: string;
  approvedAt?: string;
}

export interface PayrollRecord {
  id: string;
  employeeId: string;
  payPeriod: string;
  basicSalary: number;
  allowances: number;
  deductions: number;
  netSalary: number;
  status: 'draft' | 'processed' | 'paid';
}

export interface PerformanceReview {
  id: string;
  employeeId: string;
  reviewerId: string;
  reviewPeriod: string;
  overallRating: number;
  goals: Goal[];
  feedback: string;
  status: 'draft' | 'submitted' | 'approved';
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  targetDate: string;
  progress: number;
  status: 'not_started' | 'in_progress' | 'completed' | 'overdue';
}

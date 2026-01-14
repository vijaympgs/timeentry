import React, { useState } from 'react'
import { Form, FormGroup } from '../components/ui'
import { TabForm } from '../components/ui/TabForm'
import { User, Building, DollarSign, Phone, User as UserIcon, Shield, Home, Settings, Users, Briefcase, UserCheck } from 'lucide-react'

// PageContainer Component (UI Canon)
const PageContainer: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => {
  return (
    <div className="min-h-screen bg-[#fafafa]">
      <div className="px-6 py-3 border-b border-[#edebe9] bg-white">
        <h1 className="text-xl font-semibold text-[#201f1e]">{title}</h1>
      </div>
      <div className="flex-1 overflow-auto p-6">
        {children}
      </div>
    </div>
  )
}

// Input Component (UI Canon)
const Input: React.FC<{
  id?: string
  label?: string
  required?: boolean
  type?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  error?: string
  className?: string
}> = ({ id, label, required, type = 'text', placeholder, value, onChange, error, className = '' }) => {
  return (
    <div className="space-y-1">
      {label && (
        <label htmlFor={id} className="block text-sm font-semibold text-olivine-text">
          {label}
          {required && <span className="text-red-600">*</span>}
        </label>
      )}
      <input
        id={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        className={`w-full rounded-none px-3 py-2 border border-[#e5e7eb] bg-white text-[#201f1e] placeholder:text-[#605e5c] focus:outline-none focus:ring-2 focus:ring-nexus-primary-500 focus:border-nexus-primary-500 ${className}`}
      />
      {error && (
        <p className="text-xs text-nexus-error-600 mt-1">{error}</p>
      )}
    </div>
  )
}

// Select Component (UI Canon)
const Select: React.FC<{
  id?: string
  label?: string
  required?: boolean
  value?: string
  onChange?: (value: string) => void
  options: { value: string; label: string }[]
  error?: string
  className?: string
}> = ({ id, label, required, value, onChange, options, error, className = '' }) => {
  return (
    <div className="space-y-1">
      {label && (
        <label htmlFor={id} className="block text-sm font-semibold text-olivine-text">
          {label}
          {required && <span className="text-red-600">*</span>}
        </label>
      )}
      <select
        id={id}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        className={`w-full rounded-none px-3 py-2 border border-[#e5e7eb] bg-white text-[#201f1e] placeholder:text-[#605e5c] focus:outline-none focus:ring-2 focus:ring-nexus-primary-500 focus:border-nexus-primary-500 ${className}`}
      >
        <option value="">Select...</option>
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="text-xs text-nexus-error-600 mt-1">{error}</p>
      )}
    </div>
  )
}

// Checkbox Component (UI Canon)
const Checkbox: React.FC<{
  id?: string
  label?: string
  checked?: boolean
  onChange?: (checked: boolean) => void
  className?: string
}> = ({ id, label, checked, onChange, className = '' }) => {
  return (
    <div className="flex items-center gap-2">
      <input
        id={id}
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange?.(e.target.checked)}
        className="h-4 w-4 rounded-none border border-[#e5e7eb] text-nexus-primary-600 focus:ring-2 focus:ring-nexus-primary-500"
      />
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-[#201f1e]">
          {label}
        </label>
      )}
    </div>
  )
}

// Button Component (UI Canon)
const Button: React.FC<{
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  type?: 'button' | 'submit'
  onClick?: () => void
  className?: string
  disabled?: boolean
}> = ({ children, variant = 'primary', type = 'button', onClick, className = '', disabled = false }) => {
  const baseClasses = "px-4 py-2 text-sm font-medium transition-colors duration-180 rounded-none"
  const variantClasses = {
    primary: "bg-nexus-primary-600 hover:bg-nexus-primary-700 text-white",
    secondary: "bg-[#f3f2f1] text-[#323130] hover:bg-[#edebe9]"
  }
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
    >
      {children}
    </button>
  )
}

interface EmployeeFormData {
  // Employee Identification
  employeeNumber: string
  nationalId: string
  socialSecurityNumber: string
  passportNumber: string
  // Personal Information
  firstName: string
  lastName: string
  middleName: string
  preferredName: string
  namePrefix: string
  nameSuffix: string
  gender: string
  dateOfBirth: string
  maritalStatus: string
  // Contact Information
  workEmail: string
  personalEmail: string
  workPhone: string
  mobilePhone: string
  homePhone: string
  // Employment Details
  hireDate: string
  originalHireDate: string
  employmentStatus: string
  employmentType: string
  // Position Information
  positionTitle: string
  departmentName: string
  jobCategory: string
  jobLevel: string
  jobFamily: string
  workLocationName: string
  remoteWorkEligible: boolean
  remoteWorkPercentage: number
  // Hierarchy Information
  manager: string
  hierarchyLevel: number
  managerName: string
  hrBusinessPartnerName: string
  // Compensation Information
  salaryGrade: string
  salaryStep: string
  annualSalary: string
  hourlyRate: string
  currency: string
  payFrequency: string
  // Benefits Information
  benefitsEligibilityDate: string
  benefitsPackageName: string
  healthInsuranceEligible: boolean
  dentalInsuranceEligible: boolean
  visionInsuranceEligible: boolean
  retirementPlanEligible: boolean
  lifeInsuranceEligible: boolean
  // Emergency Contacts
  primaryEmergencyContactName: string
  primaryEmergencyContactRelationship: string
  primaryEmergencyContactPhone: string
  secondaryEmergencyContactName: string
  secondaryEmergencyContactRelationship: string
  secondaryEmergencyContactPhone: string
  // Status Information
  isActive: boolean
  isConfidential: boolean
  isKeyEmployee: boolean
  isHighPotential: boolean
  terminationDate: string
  terminationReason: string
  rehireEligible: boolean
  // Address Information
  addressLine1: string
  addressLine2: string
  city: string
  state: string
  postalCode: string
  country: string
  addressType: string
  isPrimaryAddress: boolean
  // System Access
  username: string
  role: string
  departmentAccess: string[]
}

interface EmployeeFormProps {
  employee?: any
  onSubmit: (data: EmployeeFormData) => void
  onCancel: () => void
  loading?: boolean
  hideButtons?: boolean
  verticalTabs?: boolean
  // MasterToolbar integration props
  onToolbarAction?: (action: string) => void
  mode?: 'CREATE' | 'EDIT'
}

export const EmployeeForm: React.FC<EmployeeFormProps> = ({
  employee,
  onSubmit,
  onCancel,
  loading = false,
  hideButtons = false,
  verticalTabs = false,
  onToolbarAction,
  mode = 'CREATE'
}) => {
  const [formData, setFormData] = useState<EmployeeFormData>({
    // Employee Identification
    employeeNumber: employee?.employee_number || '',
    nationalId: employee?.national_id || '',
    socialSecurityNumber: employee?.social_security_number || '',
    passportNumber: employee?.passport_number || '',
    // Personal Information
    firstName: employee?.first_name || '',
    lastName: employee?.last_name || '',
    middleName: employee?.middle_name || '',
    preferredName: employee?.preferred_name || '',
    namePrefix: employee?.name_prefix || '',
    nameSuffix: employee?.name_suffix || '',
    gender: employee?.gender || '',
    dateOfBirth: employee?.date_of_birth || '',
    maritalStatus: employee?.marital_status || '',
    // Contact Information
    workEmail: employee?.work_email || '',
    personalEmail: employee?.personal_email || '',
    workPhone: employee?.work_phone || '',
    mobilePhone: employee?.mobile_phone || '',
    homePhone: employee?.home_phone || '',
    // Employment Details
    hireDate: employee?.hire_date || '',
    originalHireDate: employee?.original_hire_date || '',
    employmentStatus: employee?.employment_status || 'ACTIVE',
    employmentType: employee?.employment_type || 'FULL_TIME',
    // Position Information
    positionTitle: employee?.position_title || '',
    departmentName: employee?.department_name || '',
    jobCategory: employee?.job_category || '',
    jobLevel: employee?.job_level || '',
    jobFamily: employee?.job_family || '',
    workLocationName: employee?.work_location_name || '',
    remoteWorkEligible: employee?.remote_work_eligible || false,
    remoteWorkPercentage: employee?.remote_work_percentage || 0,
    // Hierarchy Information
    manager: employee?.manager || '',
    hierarchyLevel: employee?.hierarchy_level || 0,
    managerName: employee?.manager_name || '',
    hrBusinessPartnerName: employee?.hr_business_partner_name || '',
    // Compensation Information
    salaryGrade: employee?.salary_grade || '',
    salaryStep: employee?.salary_step || '',
    annualSalary: employee?.annual_salary || '',
    hourlyRate: employee?.hourly_rate || '',
    currency: employee?.currency || 'USD',
    payFrequency: employee?.pay_frequency || 'MONTHLY',
    // Benefits Information
    benefitsEligibilityDate: employee?.benefits_eligibility_date || '',
    benefitsPackageName: employee?.benefits_package_name || '',
    healthInsuranceEligible: employee?.health_insurance_eligible || false,
    dentalInsuranceEligible: employee?.dental_insurance_eligible || false,
    visionInsuranceEligible: employee?.vision_insurance_eligible || false,
    retirementPlanEligible: employee?.retirement_plan_eligible || false,
    lifeInsuranceEligible: employee?.life_insurance_eligible || false,
    // Emergency Contacts
    primaryEmergencyContactName: employee?.primary_emergency_contact_name || '',
    primaryEmergencyContactRelationship: employee?.primary_emergency_contact_relationship || '',
    primaryEmergencyContactPhone: employee?.primary_emergency_contact_phone || '',
    secondaryEmergencyContactName: employee?.secondary_emergency_contact_name || '',
    secondaryEmergencyContactRelationship: employee?.secondary_emergency_contact_relationship || '',
    secondaryEmergencyContactPhone: employee?.secondary_emergency_contact_phone || '',
    // Status Information
    isActive: employee?.is_active !== undefined ? employee.is_active : true,
    isConfidential: employee?.is_confidential || false,
    isKeyEmployee: employee?.is_key_employee || false,
    isHighPotential: employee?.is_high_potential || false,
    terminationDate: employee?.termination_date || '',
    terminationReason: employee?.termination_reason || '',
    rehireEligible: employee?.rehire_eligible !== undefined ? employee.rehire_eligible : true,
    // Address Information
    addressLine1: employee?.address_line_1 || '',
    addressLine2: employee?.address_line_2 || '',
    city: employee?.city || '',
    state: employee?.state || '',
    postalCode: employee?.postal_code || '',
    country: employee?.country || 'United States',
    addressType: employee?.address_type || 'HOME',
    isPrimaryAddress: employee?.is_primary_address !== undefined ? employee.is_primary_address : true,
    // System Access
    username: employee?.username || '',
    role: employee?.role || 'Employee',
    departmentAccess: employee?.department_access || []
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  // Employee Identification Fields
  const identificationFields = [
    {
      name: 'employeeNumber',
      label: 'Employee Number',
      type: 'text' as const,
      required: true,
      validation: {
        pattern: /^EMP\d{3,}$/,
        message: 'Employee ID must start with EMP followed by numbers'
      }
    },
    {
      name: 'nationalId',
      label: 'National ID',
      type: 'text' as const,
      required: false
    },
    {
      name: 'socialSecurityNumber',
      label: 'Social Security Number',
      type: 'text' as const,
      required: false,
      validation: {
        pattern: /^\d{3}-\d{2}-\d{4}$/,
        message: 'Please enter a valid SSN format (XXX-XX-XXXX)'
      }
    },
    {
      name: 'passportNumber',
      label: 'Passport Number',
      type: 'text' as const,
      required: false
    }
  ]

  // Personal Information Fields
  const personalInfoFields = [
    {
      name: 'namePrefix',
      label: 'Name Prefix',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select Prefix' },
        { value: 'Mr.', label: 'Mr.' },
        { value: 'Mrs.', label: 'Mrs.' },
        { value: 'Ms.', label: 'Ms.' },
        { value: 'Dr.', label: 'Dr.' },
        { value: 'Prof.', label: 'Prof.' }
      ]
    },
    {
      name: 'firstName',
      label: 'First Name',
      type: 'text' as const,
      required: true,
      validation: { min: 2, message: 'First name must be at least 2 characters' }
    },
    {
      name: 'middleName',
      label: 'Middle Name',
      type: 'text' as const,
      required: false
    },
    {
      name: 'lastName',
      label: 'Last Name',
      type: 'text' as const,
      required: true,
      validation: { min: 2, message: 'Last name must be at least 2 characters' }
    },
    {
      name: 'preferredName',
      label: 'Preferred Name',
      type: 'text' as const,
      required: false
    },
    {
      name: 'nameSuffix',
      label: 'Name Suffix',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select Suffix' },
        { value: 'Jr.', label: 'Jr.' },
        { value: 'Sr.', label: 'Sr.' },
        { value: 'II', label: 'II' },
        { value: 'III', label: 'III' },
        { value: 'IV', label: 'IV' }
      ]
    },
    {
      name: 'gender',
      label: 'Gender',
      type: 'select' as const,
      required: true,
      options: [
        { value: '', label: 'Select Gender' },
        { value: 'MALE', label: 'Male' },
        { value: 'FEMALE', label: 'Female' },
        { value: 'NON_BINARY', label: 'Non-Binary' },
        { value: 'PREFER_NOT_TO_SAY', label: 'Prefer not to say' }
      ]
    },
    {
      name: 'dateOfBirth',
      label: 'Date of Birth',
      type: 'date' as const,
      required: true
    },
    {
      name: 'maritalStatus',
      label: 'Marital Status',
      type: 'select' as const,
      required: true,
      options: [
        { value: '', label: 'Select Status' },
        { value: 'SINGLE', label: 'Single' },
        { value: 'MARRIED', label: 'Married' },
        { value: 'DIVORCED', label: 'Divorced' },
        { value: 'SEPARATED', label: 'Separated' },
        { value: 'WIDOWED', label: 'Widowed' },
        { value: 'DOMESTIC_PARTNERSHIP', label: 'Domestic Partnership' }
      ]
    }
  ]

  // Contact Information Fields
  const contactFields = [
    {
      name: 'workEmail',
      label: 'Work Email',
      type: 'email' as const,
      required: true,
      validation: {
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: 'Please enter a valid email address'
      }
    },
    {
      name: 'personalEmail',
      label: 'Personal Email',
      type: 'email' as const,
      required: false,
      validation: {
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: 'Please enter a valid email address'
      }
    },
    {
      name: 'workPhone',
      label: 'Work Phone',
      type: 'tel' as const,
      required: false,
      validation: {
        pattern: /^\+?[\d\s\-\(\)]+$/,
        message: 'Please enter a valid phone number'
      }
    },
    {
      name: 'mobilePhone',
      label: 'Mobile Phone',
      type: 'tel' as const,
      required: false,
      validation: {
        pattern: /^\+?[\d\s\-\(\)]+$/,
        message: 'Please enter a valid phone number'
      }
    },
    {
      name: 'homePhone',
      label: 'Home Phone',
      type: 'tel' as const,
      required: false,
      validation: {
        pattern: /^\+?[\d\s\-\(\)]+$/,
        message: 'Please enter a valid phone number'
      }
    }
  ]

  // Address Information Fields
  const addressFields = [
    {
      name: 'addressType',
      label: 'Address Type',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'HOME', label: 'Home' },
        { value: 'WORK', label: 'Work' },
        { value: 'MAILING', label: 'Mailing' },
        { value: 'TEMPORARY', label: 'Temporary' }
      ]
    },
    {
      name: 'addressLine1',
      label: 'Address Line 1',
      type: 'text' as const,
      required: true
    },
    {
      name: 'addressLine2',
      label: 'Address Line 2',
      type: 'text' as const,
      required: false
    },
    {
      name: 'city',
      label: 'City',
      type: 'text' as const,
      required: true
    },
    {
      name: 'state',
      label: 'State/Province',
      type: 'text' as const,
      required: true
    },
    {
      name: 'postalCode',
      label: 'ZIP/Postal Code',
      type: 'text' as const,
      required: true,
      validation: {
        pattern: /^\d{5}(-\d{4})?$/,
        message: 'Please enter a valid ZIP code'
      }
    },
    {
      name: 'country',
      label: 'Country',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'United States', label: 'United States' },
        { value: 'Canada', label: 'Canada' },
        { value: 'United Kingdom', label: 'United Kingdom' },
        { value: 'Australia', label: 'Australia' },
        { value: 'Germany', label: 'Germany' },
        { value: 'France', label: 'France' },
        { value: 'India', label: 'India' },
        { value: 'China', label: 'China' },
        { value: 'Japan', label: 'Japan' }
      ]
    },
    {
      name: 'isPrimaryAddress',
      label: 'Primary Address',
      type: 'checkbox' as const,
      required: false
    }
  ]

  // Employment Details Fields
  const employmentFields = [
    {
      name: 'hireDate',
      label: 'Hire Date',
      type: 'date' as const,
      required: true
    },
    {
      name: 'originalHireDate',
      label: 'Original Hire Date',
      type: 'date' as const,
      required: false
    },
    {
      name: 'employmentStatus',
      label: 'Employment Status',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'ACTIVE', label: 'Active' },
        { value: 'ON_LEAVE', label: 'On Leave' },
        { value: 'TERMINATED', label: 'Terminated' },
        { value: 'RETIREMENT', label: 'Retirement' },
        { value: 'CONTRACT_END', label: 'Contract End' },
        { value: 'SUSPENDED', label: 'Suspended' }
      ]
    },
    {
      name: 'employmentType',
      label: 'Employment Type',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'FULL_TIME', label: 'Full Time' },
        { value: 'PART_TIME', label: 'Part Time' },
        { value: 'CONTRACT', label: 'Contract' },
        { value: 'INTERN', label: 'Intern' },
        { value: 'TEMPORARY', label: 'Temporary' },
        { value: 'SEASONAL', label: 'Seasonal' },
        { value: 'CONSULTANT', label: 'Consultant' },
        { value: 'FREELANCER', label: 'Freelancer' }
      ]
    }
  ]

  // Position Information Fields
  const positionFields = [
    {
      name: 'positionTitle',
      label: 'Position Title',
      type: 'text' as const,
      required: true
    },
    {
      name: 'departmentName',
      label: 'Department',
      type: 'select' as const,
      required: true,
      options: [
        { value: '', label: 'Select Department' },
        { value: 'Engineering', label: 'Engineering' },
        { value: 'HR', label: 'Human Resources' },
        { value: 'Finance', label: 'Finance' },
        { value: 'Marketing', label: 'Marketing' },
        { value: 'Sales', label: 'Sales' },
        { value: 'Operations', label: 'Operations' },
        { value: 'Customer Support', label: 'Customer Support' }
      ]
    },
    {
      name: 'jobCategory',
      label: 'Job Category',
      type: 'text' as const,
      required: false
    },
    {
      name: 'jobLevel',
      label: 'Job Level',
      type: 'text' as const,
      required: false
    },
    {
      name: 'jobFamily',
      label: 'Job Family',
      type: 'text' as const,
      required: false
    },
    {
      name: 'workLocationName',
      label: 'Work Location',
      type: 'select' as const,
      required: true,
      options: [
        { value: '', label: 'Select Location' },
        { value: 'New York Office', label: 'New York Office' },
        { value: 'San Francisco Office', label: 'San Francisco Office' },
        { value: 'Remote', label: 'Remote' },
        { value: 'Chicago Office', label: 'Chicago Office' },
        { value: 'London Office', label: 'London Office' }
      ]
    },
    {
      name: 'remoteWorkEligible',
      label: 'Remote Work Eligible',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'remoteWorkPercentage',
      label: 'Remote Work Percentage',
      type: 'number' as const,
      required: false,
      validation: { min: 0, max: 100, message: 'Must be between 0 and 100' }
    }
  ]

  // Manager Information Fields
  const managerFields = [
    {
      name: 'manager',
      label: 'Reporting Manager',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select Manager' },
        { value: 'Jane Smith', label: 'Jane Smith - Engineering Manager' },
        { value: 'Mike Johnson', label: 'Mike Johnson - HR Director' },
        { value: 'Sarah Williams', label: 'Sarah Williams - CFO' }
      ]
    },
    {
      name: 'hierarchyLevel',
      label: 'Hierarchy Level',
      type: 'number' as const,
      required: true,
      validation: { min: 0, message: 'Hierarchy level must be 0 or greater' }
    },
    {
      name: 'managerName',
      label: 'Manager Name (Display)',
      type: 'text' as const,
      required: false
    },
    {
      name: 'hrBusinessPartnerName',
      label: 'HR Business Partner',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select HR Partner' },
        { value: 'Mike Johnson', label: 'Mike Johnson - HR Director' },
        { value: 'Sarah Williams', label: 'Sarah Williams - HR Business Partner' },
        { value: 'John Davis', label: 'John Davis - HR Manager' }
      ]
    }
  ]

  // Compensation Information Fields
  const compensationFields = [
    {
      name: 'salaryGrade',
      label: 'Salary Grade',
      type: 'text' as const,
      required: false
    },
    {
      name: 'salaryStep',
      label: 'Salary Step',
      type: 'text' as const,
      required: false
    },
    {
      name: 'annualSalary',
      label: 'Annual Salary',
      type: 'text' as const,
      required: false,
      validation: {
        pattern: /^\d+$/,
        message: 'Salary must be a valid number'
      }
    },
    {
      name: 'hourlyRate',
      label: 'Hourly Rate',
      type: 'text' as const,
      required: false,
      validation: {
        pattern: /^\d+\.?\d*$/,
        message: 'Hourly rate must be a valid number'
      }
    },
    {
      name: 'currency',
      label: 'Currency',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'USD', label: 'USD - US Dollar' },
        { value: 'EUR', label: 'EUR - Euro' },
        { value: 'GBP', label: 'GBP - British Pound' },
        { value: 'CAD', label: 'CAD - Canadian Dollar' },
        { value: 'AUD', label: 'AUD - Australian Dollar' }
      ]
    },
    {
      name: 'payFrequency',
      label: 'Pay Frequency',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'HOURLY', label: 'Hourly' },
        { value: 'WEEKLY', label: 'Weekly' },
        { value: 'BI_WEEKLY', label: 'Bi-weekly' },
        { value: 'SEMI_MONTHLY', label: 'Semi-monthly' },
        { value: 'MONTHLY', label: 'Monthly' },
        { value: 'ANNUAL', label: 'Annual' }
      ]
    }
  ]

  // Benefits Information Fields
  const benefitsFields = [
    {
      name: 'benefitsEligibilityDate',
      label: 'Benefits Eligibility Date',
      type: 'date' as const,
      required: false
    },
    {
      name: 'benefitsPackageName',
      label: 'Benefits Package',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select Package' },
        { value: 'Basic', label: 'Basic' },
        { value: 'Standard', label: 'Standard' },
        { value: 'Standard Plus', label: 'Standard Plus' },
        { value: 'Premium', label: 'Premium' },
        { value: 'Executive', label: 'Executive' }
      ]
    },
    {
      name: 'healthInsuranceEligible',
      label: 'Health Insurance Eligible',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'dentalInsuranceEligible',
      label: 'Dental Insurance Eligible',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'visionInsuranceEligible',
      label: 'Vision Insurance Eligible',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'retirementPlanEligible',
      label: 'Retirement Plan Eligible',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'lifeInsuranceEligible',
      label: 'Life Insurance Eligible',
      type: 'checkbox' as const,
      required: false
    }
  ]

  // Emergency Contact Fields
  const emergencyContactFields = [
    {
      name: 'primaryEmergencyContactName',
      label: 'Primary Emergency Contact Name',
      type: 'text' as const,
      required: true
    },
    {
      name: 'primaryEmergencyContactRelationship',
      label: 'Primary Contact Relationship',
      type: 'select' as const,
      required: true,
      options: [
        { value: '', label: 'Select Relationship' },
        { value: 'Spouse', label: 'Spouse' },
        { value: 'Parent', label: 'Parent' },
        { value: 'Sibling', label: 'Sibling' },
        { value: 'Child', label: 'Child' },
        { value: 'Friend', label: 'Friend' },
        { value: 'Other', label: 'Other' }
      ]
    },
    {
      name: 'primaryEmergencyContactPhone',
      label: 'Primary Emergency Contact Phone',
      type: 'tel' as const,
      required: true,
      validation: {
        pattern: /^\+?[\d\s\-\(\)]+$/,
        message: 'Please enter a valid phone number'
      }
    },
    {
      name: 'secondaryEmergencyContactName',
      label: 'Secondary Emergency Contact Name',
      type: 'text' as const,
      required: false
    },
    {
      name: 'secondaryEmergencyContactRelationship',
      label: 'Secondary Contact Relationship',
      type: 'select' as const,
      required: false,
      options: [
        { value: '', label: 'Select Relationship' },
        { value: 'Spouse', label: 'Spouse' },
        { value: 'Parent', label: 'Parent' },
        { value: 'Sibling', label: 'Sibling' },
        { value: 'Child', label: 'Child' },
        { value: 'Friend', label: 'Friend' },
        { value: 'Other', label: 'Other' }
      ]
    },
    {
      name: 'secondaryEmergencyContactPhone',
      label: 'Secondary Emergency Contact Phone',
      type: 'tel' as const,
      required: false,
      validation: {
        pattern: /^\+?[\d\s\-\(\)]+$/,
        message: 'Please enter a valid phone number'
      }
    }
  ]

  // Status Information Fields
  const statusFields = [
    {
      name: 'isActive',
      label: 'Active Employee',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'isConfidential',
      label: 'Confidential Employee',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'isKeyEmployee',
      label: 'Key Employee',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'isHighPotential',
      label: 'High Potential Employee',
      type: 'checkbox' as const,
      required: false
    },
    {
      name: 'terminationDate',
      label: 'Termination Date',
      type: 'date' as const,
      required: false
    },
    {
      name: 'terminationReason',
      label: 'Termination Reason',
      type: 'text' as const,
      required: false
    },
    {
      name: 'rehireEligible',
      label: 'Rehire Eligible',
      type: 'checkbox' as const,
      required: false
    }
  ]

  const systemAccessFields = [
    {
      name: 'username',
      label: 'System Username',
      type: 'text' as const,
      required: true,
      validation: {
        min: 3,
        pattern: /^[a-zA-Z0-9_]+$/,
        message: 'Username must be at least 3 characters and contain only letters, numbers, and underscores'
      }
    },
    {
      name: 'role',
      label: 'System Role',
      type: 'select' as const,
      required: true,
      options: [
        { value: 'Employee', label: 'Employee' },
        { value: 'Manager', label: 'Manager' },
        { value: 'HR Admin', label: 'HR Admin' },
        { value: 'Finance Admin', label: 'Finance Admin' },
        { value: 'System Admin', label: 'System Admin' }
      ]
    }
  ]

  const handleSubmit = (data: Record<string, any>) => {
    // Validate required fields
    const newErrors: Record<string, string> = {}
    if (!data.firstName) newErrors.firstName = 'First name is required'
    if (!data.lastName) newErrors.lastName = 'Last name is required'
    if (!data.workEmail) newErrors.workEmail = 'Work email is required'
    if (!data.employeeNumber) newErrors.employeeNumber = 'Employee number is required'
    if (!data.departmentName) newErrors.departmentName = 'Department is required'
    if (!data.positionTitle) newErrors.positionTitle = 'Position is required'
    if (!data.hireDate) newErrors.hireDate = 'Hire date is required'
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    setErrors({})
    onSubmit(data as EmployeeFormData)
  }

  // MasterToolbar integration handler
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'save':
        handleSubmit(formData)
        break
      case 'cancel':
        onCancel()
        break
      case 'clear':
        // Clear form data
        setFormData({
          // Reset all fields to empty/default values
          employeeNumber: '',
          nationalId: '',
          socialSecurityNumber: '',
          passportNumber: '',
          firstName: '',
          lastName: '',
          middleName: '',
          preferredName: '',
          namePrefix: '',
          nameSuffix: '',
          gender: '',
          dateOfBirth: '',
          maritalStatus: '',
          workEmail: '',
          personalEmail: '',
          workPhone: '',
          mobilePhone: '',
          homePhone: '',
          hireDate: '',
          originalHireDate: '',
          employmentStatus: 'ACTIVE',
          employmentType: 'FULL_TIME',
          positionTitle: '',
          departmentName: '',
          jobCategory: '',
          jobLevel: '',
          jobFamily: '',
          workLocationName: '',
          remoteWorkEligible: false,
          remoteWorkPercentage: 0,
          manager: '',
          hierarchyLevel: 0,
          managerName: '',
          hrBusinessPartnerName: '',
          salaryGrade: '',
          salaryStep: '',
          annualSalary: '',
          hourlyRate: '',
          currency: 'USD',
          payFrequency: 'MONTHLY',
          benefitsEligibilityDate: '',
          benefitsPackageName: '',
          healthInsuranceEligible: false,
          dentalInsuranceEligible: false,
          visionInsuranceEligible: false,
          retirementPlanEligible: false,
          lifeInsuranceEligible: false,
          primaryEmergencyContactName: '',
          primaryEmergencyContactRelationship: '',
          primaryEmergencyContactPhone: '',
          secondaryEmergencyContactName: '',
          secondaryEmergencyContactRelationship: '',
          secondaryEmergencyContactPhone: '',
          isActive: true,
          isConfidential: false,
          isKeyEmployee: false,
          isHighPotential: false,
          terminationDate: '',
          terminationReason: '',
          rehireEligible: true,
          addressLine1: '',
          addressLine2: '',
          city: '',
          state: '',
          postalCode: '',
          country: 'United States',
          addressType: 'HOME',
          isPrimaryAddress: true,
          username: '',
          role: 'Employee',
          departmentAccess: []
        })
        setErrors({})
        break
      case 'help':
        // Open help modal or navigate to help
        console.log('Help requested for Employee Form')
        break
      case 'notes':
        // Open notes modal
        console.log('Notes requested for Employee Form')
        break
      case 'attach':
        // Open attachment modal
        console.log('Attachments requested for Employee Form')
        break
      default:
        console.log('Unknown toolbar action:', action)
    }
  }

  // Tab Components
  const IdentificationTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Employee Identification</h3>
      <p className="md-body-medium text-gray-600">Unique identifiers for the employee</p>
      <Form
        fields={identificationFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const PersonalTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Personal Information</h3>
      <p className="md-body-medium text-gray-600">Basic personal information about the employee</p>
      <FormGroup title="Name Details">
        <Form
          fields={personalInfoFields.slice(0, 6)}
          data={data}
          onChange={onChange}
          onSubmit={() => {}}
          onCancel={onCancel}
          loading={loading}
          errors={errors}
          layout="horizontal"
          hideButtons={hideButtons}
        />
      </FormGroup>
      <FormGroup title="Personal Details">
        <Form
          fields={personalInfoFields.slice(6)}
          data={data}
          onChange={onChange}
          onSubmit={() => {}}
          onCancel={onCancel}
          loading={loading}
          errors={errors}
          layout="horizontal"
          hideButtons={hideButtons}
        />
      </FormGroup>
    </div>
  )

  const ContactTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Contact Information</h3>
      <p className="md-body-medium text-gray-600">Various ways to contact the employee</p>
      <Form
        fields={contactFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const AddressTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Address Information</h3>
      <p className="md-body-medium text-gray-600">Employee's residential and mailing address</p>
      <Form
        fields={addressFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const EmploymentTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Employment Details</h3>
      <p className="md-body-medium text-gray-600">Employment status and type information</p>
      <Form
        fields={employmentFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const PositionTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Position Information</h3>
      <p className="md-body-medium text-gray-600">Job details and work location</p>
      <Form
        fields={positionFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const ManagerTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Manager Information</h3>
      <p className="md-body-medium text-gray-600">Reporting structure and HR support</p>
      <Form
        fields={managerFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const CompensationTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Compensation Information</h3>
      <p className="md-body-medium text-gray-600">Salary and compensation details</p>
      <Form
        fields={compensationFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const BenefitsTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Benefits Information</h3>
      <p className="md-body-medium text-gray-600">Benefits eligibility and package details</p>
      <Form
        fields={benefitsFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const EmergencyTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Emergency Contacts</h3>
      <p className="md-body-medium text-gray-600">Contact information for emergency situations</p>
      <FormGroup title="Primary Emergency Contact">
        <Form
          fields={emergencyContactFields.slice(0, 3)}
          data={data}
          onChange={onChange}
          onSubmit={() => {}}
          onCancel={onCancel}
          loading={loading}
          errors={errors}
          layout="horizontal"
          hideButtons={hideButtons}
        />
      </FormGroup>
      <FormGroup title="Secondary Emergency Contact">
        <Form
          fields={emergencyContactFields.slice(3)}
          data={data}
          onChange={onChange}
          onSubmit={() => {}}
          onCancel={onCancel}
          loading={loading}
          errors={errors}
          layout="horizontal"
          hideButtons={hideButtons}
        />
      </FormGroup>
    </div>
  )

  const StatusTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">Status Information</h3>
      <p className="md-body-medium text-gray-600">Employee status and employment flags</p>
      <Form
        fields={statusFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const SystemTab: React.FC<{ data: Record<string, any>; onChange: (field: string, value: any) => void; onCancel: () => void; loading?: boolean; errors?: Record<string, string> }> = ({ data, onChange, onCancel, loading, errors }) => (
    <div className="space-y-6">
      <h3 className="md-title-large text-gray-900">System Access</h3>
      <p className="md-body-medium text-gray-600">User account and system permissions</p>
      <Form
        fields={systemAccessFields}
        data={data}
        onChange={onChange}
        onSubmit={() => {}}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        layout="horizontal"
        hideButtons={hideButtons}
      />
    </div>
  )

  const tabs = [
    {
      id: 'identification',
      label: 'Identification',
      icon: UserIcon,
      component: IdentificationTab
    },
    {
      id: 'personal',
      label: 'Personal',
      icon: User,
      component: PersonalTab
    },
    {
      id: 'contact',
      label: 'Contact',
      icon: Phone,
      component: ContactTab
    },
    {
      id: 'address',
      label: 'Address',
      icon: Home,
      component: AddressTab
    },
    {
      id: 'employment',
      label: 'Employment',
      icon: Briefcase,
      component: EmploymentTab
    },
    {
      id: 'position',
      label: 'Position',
      icon: Building,
      component: PositionTab
    },
    {
      id: 'manager',
      label: 'Manager',
      icon: Users,
      component: ManagerTab
    },
    {
      id: 'compensation',
      label: 'Compensation',
      icon: DollarSign,
      component: CompensationTab
    },
    {
      id: 'benefits',
      label: 'Benefits',
      icon: Shield,
      component: BenefitsTab
    },
    {
      id: 'emergency',
      label: 'Emergency',
      icon: Phone,
      component: EmergencyTab
    },
    {
      id: 'status',
      label: 'Status',
      icon: UserCheck,
      component: StatusTab
    },
    {
      id: 'system',
      label: 'System',
      icon: Settings,
      component: SystemTab
    }
  ]

  return (
    <div className="max-h-[80vh] overflow-y-auto pr-4">
      <TabForm
        tabs={tabs}
        data={formData}
        onChange={(field, value) => setFormData(prev => ({ ...prev, [field]: value }))}
        onSubmit={handleSubmit}
        onCancel={onCancel}
        loading={loading}
        errors={errors}
        submitText={employee ? 'Update Employee' : 'Create Employee'}
        cancelText='Cancel'
        hideButtons={true}
        verticalTabs={verticalTabs}
      />
    </div>
  )
}

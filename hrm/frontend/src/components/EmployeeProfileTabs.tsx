import React, { useState } from 'react'
import { 
  User, 
  Building, 
  Calendar, 
  DollarSign, 
  FileText, 
  Award, 
  Phone, 
  MapPin, 
  Shield, 
  History,
  FolderOpen,
  Star,
  Briefcase,
  Users,
  Settings
} from 'lucide-react'

interface Employee {
  id: string
  employeeNumber: string
  firstName: string
  lastName: string
  middleName: string
  preferredName: string
  namePrefix: string
  nameSuffix: string
  gender: string
  dateOfBirth: string
  maritalStatus: string
  workEmail: string
  personalEmail: string
  workPhone: string
  mobilePhone: string
  homePhone: string
  hireDate: string
  originalHireDate: string
  employmentStatus: string
  employmentType: string
  positionTitle: string
  departmentName: string
  jobCategory: string
  jobLevel: string
  jobFamily: string
  workLocationName: string
  remoteWorkEligible: boolean
  remoteWorkPercentage: number
  managerName: string
  hrBusinessPartnerName: string
  salaryGrade: string
  salaryStep: string
  annualSalary: string
  hourlyRate: string
  currency: string
  payFrequency: string
  benefitsEligibilityDate: string
  benefitsPackageName: string
  healthInsuranceEligible: boolean
  dentalInsuranceEligible: boolean
  visionInsuranceEligible: boolean
  retirementPlanEligible: boolean
  lifeInsuranceEligible: boolean
  primaryEmergencyContactName: string
  primaryEmergencyContactRelationship: string
  primaryEmergencyContactPhone: string
  secondaryEmergencyContactName: string
  secondaryEmergencyContactRelationship: string
  secondaryEmergencyContactPhone: string
  isActive: boolean
  isConfidential: boolean
  isKeyEmployee: boolean
  isHighPotential: boolean
  terminationDate: string
  terminationReason: string
  rehireEligible: boolean
  addressLine1: string
  addressLine2: string
  city: string
  state: string
  postalCode: string
  country: string
  addressType: string
  isPrimaryAddress: boolean
  username: string
  role: string
  departmentAccess: string[]
}

interface EmployeeProfileTabsProps {
  employee: Employee
}

interface TabConfig {
  id: string
  label: string
  icon: React.ElementType
  component: React.ComponentType<{ employee: Employee }>
}

const PersonalInfoTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Personal Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Employee Number</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.employeeNumber}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Full Name</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.namePrefix} {employee.firstName} {employee.middleName} {employee.lastName} {employee.nameSuffix}
            </p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Preferred Name</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.preferredName || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Gender</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.gender}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Date of Birth</label>
            <p className="md-body-medium text-gray-900 mt-1">{new Date(employee.dateOfBirth).toLocaleDateString()}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Marital Status</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.maritalStatus}</p>
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Contact Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Work Email</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.workEmail}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Personal Email</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.personalEmail || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Work Phone</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.workPhone || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Mobile Phone</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.mobilePhone || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Home Phone</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.homePhone || 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Address Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Address Information</h3>
        <div className="space-y-4">
          <div>
            <label className="md-label-medium text-gray-500">Address Type</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.addressType}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Address</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.addressLine1}
              {employee.addressLine2 && <br />}
              {employee.addressLine2}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="md-label-medium text-gray-500">City</label>
              <p className="md-body-medium text-gray-900 mt-1">{employee.city}</p>
            </div>
            <div>
              <label className="md-label-medium text-gray-500">State</label>
              <p className="md-body-medium text-gray-900 mt-1">{employee.state}</p>
            </div>
            <div>
              <label className="md-label-medium text-gray-500">Postal Code</label>
              <p className="md-body-medium text-gray-900 mt-1">{employee.postalCode}</p>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Country</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.country}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

const EmploymentTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  return (
    <div className="space-y-6">
      {/* Employment Details */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Employment Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Hire Date</label>
            <p className="md-body-medium text-gray-900 mt-1">{new Date(employee.hireDate).toLocaleDateString()}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Original Hire Date</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.originalHireDate ? new Date(employee.originalHireDate).toLocaleDateString() : 'N/A'}
            </p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Employment Status</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.employmentStatus === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                employee.employmentStatus === 'ON_LEAVE' ? 'bg-yellow-100 text-yellow-800' :
                employee.employmentStatus === 'TERMINATED' ? 'bg-red-100 text-red-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {employee.employmentStatus.replace('_', ' ')}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Employment Type</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.employmentType.replace('_', ' ')}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Is Active</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {employee.isActive ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Is Key Employee</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.isKeyEmployee ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.isKeyEmployee ? 'Key Employee' : 'Regular'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Position Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Position Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Position Title</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.positionTitle}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Department</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.departmentName}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Job Category</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.jobCategory || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Job Level</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.jobLevel || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Job Family</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.jobFamily || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Work Location</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.workLocationName}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Remote Work Eligible</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.remoteWorkEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.remoteWorkEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Remote Work Percentage</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.remoteWorkPercentage}%</p>
          </div>
        </div>
      </div>

      {/* Manager Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Manager Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Reporting Manager</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.managerName || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">HR Business Partner</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.hrBusinessPartnerName || 'N/A'}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

const CompensationTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  return (
    <div className="space-y-6">
      {/* Compensation Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Compensation Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Salary Grade</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.salaryGrade || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Salary Step</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.salaryStep || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Annual Salary</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.annualSalary ? `${employee.currency} ${parseFloat(employee.annualSalary).toLocaleString()}` : 'N/A'}
            </p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Hourly Rate</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.hourlyRate ? `${employee.currency} ${parseFloat(employee.hourlyRate).toFixed(2)}` : 'N/A'}
            </p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Currency</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.currency}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Pay Frequency</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.payFrequency.replace('_', ' ')}</p>
          </div>
        </div>
      </div>

      {/* Benefits Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Benefits Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Benefits Package</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.benefitsPackageName || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Benefits Eligibility Date</label>
            <p className="md-body-medium text-gray-900 mt-1">
              {employee.benefitsEligibilityDate ? new Date(employee.benefitsEligibilityDate).toLocaleDateString() : 'N/A'}
            </p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Health Insurance</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.healthInsuranceEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.healthInsuranceEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Dental Insurance</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.dentalInsuranceEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.dentalInsuranceEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Vision Insurance</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.visionInsuranceEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.visionInsuranceEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Retirement Plan</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.retirementPlanEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.retirementPlanEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Life Insurance</label>
            <div className="mt-1">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                employee.lifeInsuranceEligible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.lifeInsuranceEligible ? 'Eligible' : 'Not Eligible'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const EmergencyContactsTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  return (
    <div className="space-y-6">
      {/* Primary Emergency Contact */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Primary Emergency Contact</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Contact Name</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.primaryEmergencyContactName || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Relationship</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.primaryEmergencyContactRelationship || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Phone Number</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.primaryEmergencyContactPhone || 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Secondary Emergency Contact */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Secondary Emergency Contact</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="md-label-medium text-gray-500">Contact Name</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.secondaryEmergencyContactName || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Relationship</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.secondaryEmergencyContactRelationship || 'N/A'}</p>
          </div>
          <div>
            <label className="md-label-medium text-gray-500">Phone Number</label>
            <p className="md-body-medium text-gray-900 mt-1">{employee.secondaryEmergencyContactPhone || 'N/A'}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

const DocumentsTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  const [documents] = useState([
    { id: '1', name: 'Employment Contract', type: 'Contract', uploadDate: '2024-01-15', size: '2.3 MB' },
    { id: '2', name: 'Resume', type: 'Resume', uploadDate: '2024-01-10', size: '1.1 MB' },
    { id: '3', name: 'ID Proof', type: 'Identification', uploadDate: '2024-01-08', size: '0.8 MB' },
    { id: '4', name: 'Address Proof', type: 'Address', uploadDate: '2024-01-05', size: '1.5 MB' }
  ])

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="md-title-large text-gray-900">Employee Documents</h3>
          <button className="btn btn-primary">
            <FolderOpen className="h-4 w-4 mr-2" />
            Upload Document
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Document Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Upload Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {documents.map((doc) => (
                <tr key={doc.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <FileText className="h-4 w-4 text-gray-400 mr-2" />
                      <span className="text-sm font-medium text-gray-900">{doc.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      {doc.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(doc.uploadDate).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {doc.size}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900 mr-3">Download</button>
                    <button className="text-red-600 hover:text-red-900">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

const SkillsTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  const [skills] = useState([
    { id: '1', name: 'JavaScript', category: 'Technical', level: 'Advanced', yearsExperience: 5 },
    { id: '2', name: 'React', category: 'Technical', level: 'Advanced', yearsExperience: 4 },
    { id: '3', name: 'Project Management', category: 'Soft Skills', level: 'Intermediate', yearsExperience: 3 },
    { id: '4', name: 'Communication', category: 'Soft Skills', level: 'Advanced', yearsExperience: 8 }
  ])

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="md-title-large text-gray-900">Skills Inventory</h3>
          <button className="btn btn-primary">
            <Award className="h-4 w-4 mr-2" />
            Add Skill
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {skills.map((skill) => (
            <div key={skill.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="md-title-medium text-gray-900">{skill.name}</h4>
                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                  skill.level === 'Advanced' ? 'bg-green-100 text-green-800' :
                  skill.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {skill.level}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="md-label-small text-gray-500">Category:</span>
                  <span className="md-body-small text-gray-900">{skill.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="md-label-small text-gray-500">Experience:</span>
                  <span className="md-body-small text-gray-900">{skill.yearsExperience} years</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

const AuditTrailTab: React.FC<{ employee: Employee }> = ({ employee }) => {
  const [auditLogs] = useState([
    { id: '1', action: 'Employee Created', field: 'All', oldValue: 'N/A', newValue: 'New Employee', timestamp: '2024-01-15 09:00:00', user: 'HR Admin' },
    { id: '2', action: 'Position Updated', field: 'positionTitle', oldValue: 'Software Engineer', newValue: 'Senior Software Engineer', timestamp: '2024-06-01 14:30:00', user: 'Manager' },
    { id: '3', action: 'Salary Updated', field: 'annualSalary', oldValue: '85000', newValue: '95000', timestamp: '2024-07-01 10:15:00', user: 'HR Admin' },
    { id: '4', action: 'Status Updated', field: 'employmentStatus', oldValue: 'ACTIVE', newValue: 'ON_LEAVE', timestamp: '2024-08-01 09:00:00', user: 'HR Admin' }
  ])

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="md-title-large text-gray-900 mb-6">Audit Trail</h3>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Field</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Old Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">New Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {auditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      {log.action}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.field}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{log.oldValue}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.newValue}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.user}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export const EmployeeProfileTabs: React.FC<EmployeeProfileTabsProps> = ({ employee }) => {
  const [activeTab, setActiveTab] = useState('personal')

  const tabs: TabConfig[] = [
    {
      id: 'personal',
      label: 'Personal Information',
      icon: User,
      component: PersonalInfoTab
    },
    {
      id: 'employment',
      label: 'Employment',
      icon: Briefcase,
      component: EmploymentTab
    },
    {
      id: 'compensation',
      label: 'Compensation',
      icon: DollarSign,
      component: CompensationTab
    },
    {
      id: 'emergency',
      label: 'Emergency Contacts',
      icon: Phone,
      component: EmergencyContactsTab
    },
    {
      id: 'documents',
      label: 'Documents',
      icon: FileText,
      component: DocumentsTab
    },
    {
      id: 'skills',
      label: 'Skills',
      icon: Award,
      component: SkillsTab
    },
    {
      id: 'audit',
      label: 'Audit Trail',
      icon: History,
      component: AuditTrailTab
    }
  ]

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || PersonalInfoTab

  return (
    <div className="w-full">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`group relative min-w-0 flex-1 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </div>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        <ActiveComponent employee={employee} />
      </div>
    </div>
  )
}

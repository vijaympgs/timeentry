import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { User, Mail, Phone, MapPin, Building, Calendar, DollarSign, Edit, ArrowLeft } from 'lucide-react'
import { EmployeeProfileTabs } from '../components/EmployeeProfileTabs'

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

export const EmployeeProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [employee, setEmployee] = useState<Employee | null>(null)
  const [loading, setLoading] = useState(true)
  const [showEditModal, setShowEditModal] = useState(false)

  // Mock data - in real app, this would come from API
  const mockEmployees: Employee[] = [
    {
      id: '1',
      employeeNumber: 'EMP001',
      firstName: 'John',
      lastName: 'Doe',
      middleName: 'William',
      preferredName: 'John',
      namePrefix: 'Mr.',
      nameSuffix: '',
      gender: 'Male',
      dateOfBirth: '1990-05-15',
      maritalStatus: 'Married',
      workEmail: 'john.doe@company.com',
      personalEmail: 'john.doe.personal@gmail.com',
      workPhone: '+1-555-0123',
      mobilePhone: '+1-555-0124',
      homePhone: '+1-555-0125',
      hireDate: '2022-01-15',
      originalHireDate: '2022-01-15',
      employmentStatus: 'ACTIVE',
      employmentType: 'FULL_TIME',
      positionTitle: 'Senior Software Engineer',
      departmentName: 'Engineering',
      jobCategory: 'Technology',
      jobLevel: 'L4',
      jobFamily: 'Software Development',
      workLocationName: 'New York Office',
      remoteWorkEligible: true,
      remoteWorkPercentage: 50,
      managerName: 'Jane Smith',
      hrBusinessPartnerName: 'Mike Johnson',
      salaryGrade: 'G4',
      salaryStep: 'S2',
      annualSalary: '95000',
      hourlyRate: '45.67',
      currency: 'USD',
      payFrequency: 'BI_WEEKLY',
      benefitsEligibilityDate: '2022-02-01',
      benefitsPackageName: 'Standard Plus',
      healthInsuranceEligible: true,
      dentalInsuranceEligible: true,
      visionInsuranceEligible: true,
      retirementPlanEligible: true,
      lifeInsuranceEligible: true,
      primaryEmergencyContactName: 'Jane Doe',
      primaryEmergencyContactRelationship: 'Spouse',
      primaryEmergencyContactPhone: '+1-555-0126',
      secondaryEmergencyContactName: 'Robert Doe',
      secondaryEmergencyContactRelationship: 'Father',
      secondaryEmergencyContactPhone: '+1-555-0127',
      isActive: true,
      isConfidential: false,
      isKeyEmployee: false,
      isHighPotential: true,
      terminationDate: '',
      terminationReason: '',
      rehireEligible: true,
      addressLine1: '123 Main Street',
      addressLine2: 'Apt 4B',
      city: 'New York',
      state: 'NY',
      postalCode: '10001',
      country: 'United States',
      addressType: 'HOME',
      isPrimaryAddress: true,
      username: 'johndoe',
      role: 'Employee',
      departmentAccess: ['Engineering']
    },
    {
      id: '2',
      employeeNumber: 'EMP002',
      firstName: 'Jane',
      lastName: 'Smith',
      middleName: 'Marie',
      preferredName: 'Jane',
      namePrefix: 'Ms.',
      nameSuffix: '',
      gender: 'Female',
      dateOfBirth: '1985-08-22',
      maritalStatus: 'Married',
      workEmail: 'jane.smith@company.com',
      personalEmail: 'jane.smith.personal@gmail.com',
      workPhone: '+1-555-0130',
      mobilePhone: '+1-555-0131',
      homePhone: '+1-555-0132',
      hireDate: '2021-03-20',
      originalHireDate: '2021-03-20',
      employmentStatus: 'ACTIVE',
      employmentType: 'FULL_TIME',
      positionTitle: 'Engineering Manager',
      departmentName: 'Engineering',
      jobCategory: 'Management',
      jobLevel: 'M3',
      jobFamily: 'Engineering Management',
      workLocationName: 'New York Office',
      remoteWorkEligible: true,
      remoteWorkPercentage: 30,
      managerName: 'Mike Johnson',
      hrBusinessPartnerName: 'Sarah Williams',
      salaryGrade: 'M3',
      salaryStep: 'S1',
      annualSalary: '120000',
      hourlyRate: '57.69',
      currency: 'USD',
      payFrequency: 'BI_WEEKLY',
      benefitsEligibilityDate: '2021-04-01',
      benefitsPackageName: 'Executive',
      healthInsuranceEligible: true,
      dentalInsuranceEligible: true,
      visionInsuranceEligible: true,
      retirementPlanEligible: true,
      lifeInsuranceEligible: true,
      primaryEmergencyContactName: 'John Smith',
      primaryEmergencyContactRelationship: 'Husband',
      primaryEmergencyContactPhone: '+1-555-0133',
      secondaryEmergencyContactName: 'Mary Smith',
      secondaryEmergencyContactRelationship: 'Mother',
      secondaryEmergencyContactPhone: '+1-555-0134',
      isActive: true,
      isConfidential: false,
      isKeyEmployee: true,
      isHighPotential: true,
      terminationDate: '',
      terminationReason: '',
      rehireEligible: true,
      addressLine1: '456 Oak Avenue',
      addressLine2: '',
      city: 'New York',
      state: 'NY',
      postalCode: '10002',
      country: 'United States',
      addressType: 'HOME',
      isPrimaryAddress: true,
      username: 'janesmith',
      role: 'Manager',
      departmentAccess: ['Engineering', 'HR']
    }
  ]

  useEffect(() => {
    loadEmployee()
  }, [id])

  const loadEmployee = async () => {
    setLoading(true)
    // Simulate API call
    setTimeout(() => {
      const foundEmployee = mockEmployees.find(emp => emp.id === id)
      setEmployee(foundEmployee || null)
      setLoading(false)
    }, 500)
  }

  const handleEdit = () => {
    setShowEditModal(true)
  }

  const getStatusColor = (status: string) => {
    const statusColors = {
      'Active': 'bg-green-100 text-green-800',
      'Inactive': 'bg-red-100 text-red-800',
      'On Leave': 'bg-yellow-100 text-yellow-800'
    }
    return statusColors[status as keyof typeof statusColors] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!employee) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Employee Not Found</h2>
          <p className="text-gray-500 mb-6">The employee you're looking for doesn't exist.</p>
          <button
            onClick={() => navigate('/employees/records')}
            className="btn btn-primary"
          >
            Back to Employee List
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 -mx-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/employees/records')}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">Employee Profile</h1>
              <p className="text-sm text-gray-500 mt-1">View and manage employee information</p>
            </div>
          </div>
          <button
            onClick={handleEdit}
            className="btn btn-primary"
          >
            <Edit className="h-4 w-4 mr-2" />
            Edit Employee
          </button>
        </div>
      </div>

      {/* Tabbed Profile Content */}
      <EmployeeProfileTabs employee={employee} />

      {/* Edit Modal Placeholder */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Employee</h3>
            <p className="text-gray-500 mb-6">Edit functionality will be implemented here.</p>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowEditModal(false)}
                className="btn btn-outline"
              >
                Cancel
              </button>
              <button
                onClick={() => setShowEditModal(false)}
                className="btn btn-primary"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

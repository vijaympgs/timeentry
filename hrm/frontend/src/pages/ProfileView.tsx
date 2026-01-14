import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MasterToolbar, MasterMode } from '../components/ui/MasterToolbar';
import { EmployeeRecord, EmployeeProfile, EmployeeSkill, EmployeeDocument } from '../types/employee';
import { employeeService } from '../services/employeeService';

interface ProfileViewProps {
  employeeId?: string;
}

const ProfileView: React.FC<ProfileViewProps> = ({ employeeId: propEmployeeId }) => {
  const { id: urlEmployeeId } = useParams();
  const navigate = useNavigate();
  const employeeId = propEmployeeId || urlEmployeeId;
  
  const [employee, setEmployee] = useState<EmployeeRecord | null>(null);
  const [profile, setProfile] = useState<EmployeeProfile | null>(null);
  const [skills, setSkills] = useState<EmployeeSkill[]>([]);
  const [documents, setDocuments] = useState<EmployeeDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  // Determine toolbar mode
  const getMode = (): MasterMode => {
    if (!employeeId) return 'VIEW';
    if (isEditing) return 'EDIT';
    return 'VIEW_FORM';
  };

  // Load employee data
  useEffect(() => {
    if (employeeId) {
      loadEmployeeData();
    } else {
      setLoading(false);
    }
  }, [employeeId]);

  const loadEmployeeData = async () => {
    if (!employeeId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Load employee record
      const employeeData = await employeeService.getById(employeeId);
      setEmployee(employeeData);
      
      // Load related data
      const [profileData, skillsData, documentsData] = await Promise.all([
        employeeService.getProfile(employeeId),
        employeeService.getSkills(employeeId),
        employeeService.getDocuments(employeeId)
      ]);
      
      setProfile(profileData);
      setSkills(skillsData);
      setDocuments(documentsData);
    } catch (err: any) {
      setError(err.message || 'Failed to load employee data');
    } finally {
      setLoading(false);
    }
  };

  // Handle toolbar actions
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'edit':
        setIsEditing(true);
        break;
      case 'save':
        handleSave();
        break;
      case 'cancel':
        setIsEditing(false);
        break;
      case 'exit':
        navigate('/hrm/employee-records');
        break;
      case 'print':
        window.print();
        break;
      default:
        console.log('Action:', action);
    }
  };

  const handleSave = async () => {
    try {
      if (profile) {
        await employeeService.updateProfile(profile.id, profile);
        setIsEditing(false);
        // Reload data to get latest changes
        await loadEmployeeData();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to save profile');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="text-sm text-red-600">{error}</div>
      </div>
    );
  }

  if (!employee) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Employee not found</p>
      </div>
    );
  }

  return (
    <div className="page-container space-y-6">
      {/* Toolbar */}
      <MasterToolbar
        viewId="HRM_PROFILE_VIEW"
        mode={getMode()}
        onAction={handleToolbarAction}
        hasSelection={!!employeeId}
      />

      {/* Profile Header */}
      <div className="bg-white shadow-sm border border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
                <span className="text-xl font-semibold text-gray-600">
                  {employee.first_name?.[0]}{employee.last_name?.[0]}
                </span>
              </div>
              <div>
                <h1 className="text-xl font-semibold text-[#201f1e]">
                  {employee.first_name} {employee.last_name}
                </h1>
                <p className="text-sm text-[#605e5c]">
                  {employee.employee_number} • {employee.position?.title}
                </p>
              </div>
            </div>
            <div className="text-right">
              <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                {employee.status}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Profile Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Profile */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information */}
          <div className="bg-white shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-[#323130]">Personal Information</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    value={employee.first_name || ''}
                    disabled={!isEditing}
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={employee.last_name || ''}
                    disabled={!isEditing}
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={employee.email || ''}
                    disabled={!isEditing}
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Phone
                  </label>
                  <input
                    type="tel"
                    value={employee.phone || ''}
                    disabled={!isEditing}
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Job Information */}
          <div className="bg-white shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-[#323130]">Job Information</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Employee Number
                  </label>
                  <input
                    type="text"
                    value={employee.employee_number || ''}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Position
                  </label>
                  <input
                    type="text"
                    value={employee.position?.title || ''}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Department
                  </label>
                  <input
                    type="text"
                    value={employee.department?.name || ''}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm bg-gray-50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                    Hire Date
                  </label>
                  <input
                    type="date"
                    value={employee.hire_date || ''}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm bg-gray-50"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Skills */}
          <div className="bg-white shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-[#323130]">Skills</h2>
            </div>
            <div className="p-6">
              {skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <span
                      key={skill.id}
                      className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {skill.skill_name}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No skills recorded</p>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-white shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-[#323130]">Quick Actions</h2>
            </div>
            <div className="p-6 space-y-3">
              <button className="w-full px-3 py-2 text-sm font-medium text-[#0078d4] hover:bg-[#f3f9ff] rounded-sm border border-[#0078d4]">
                View Organization Chart
              </button>
              <button className="w-full px-3 py-2 text-sm font-medium text-[#0078d4] hover:bg-[#f3f9ff] rounded-sm border border-[#0078d4]">
                View Direct Reports
              </button>
              <button className="w-full px-3 py-2 text-sm font-medium text-[#0078d4] hover:bg-[#f3f9ff] rounded-sm border border-[#0078d4]">
                Performance History
              </button>
            </div>
          </div>

          {/* Documents */}
          <div className="bg-white shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-[#323130]">Documents</h2>
            </div>
            <div className="p-6">
              {documents.length > 0 ? (
                <div className="space-y-2">
                  {documents.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-2 border border-gray-200 rounded-sm">
                      <span className="text-sm text-[#323130]">{doc.document_name}</span>
                      <button className="text-xs text-[#0078d4] hover:underline">
                        View
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No documents uploaded</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileView;

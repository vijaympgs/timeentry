import React from 'react'
import { Users, Building, Calendar, TrendingUp, Award, Clock, DollarSign, AlertCircle, UserCheck, Briefcase, Target, Activity } from 'lucide-react'

export const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header - Dynamics 365 Style */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 -mx-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
            <p className="text-sm text-gray-500 mt-1">Welcome back! Here's your overview for today, {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
          </div>
          <div className="flex items-center gap-2">
            <button className="btn btn-outline btn-sm">Export Report</button>
            <button className="btn btn-primary btn-sm">Quick Actions</button>
          </div>
        </div>
      </div>

      {/* Key Metrics Cards - Dynamics 365 Style */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600 mb-1">Total Workforce</p>
              <p className="text-3xl font-bold text-gray-900 mb-2">1,234</p>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 text-green-600">
                  <TrendingUp className="h-3 w-3" />
                  <span className="text-xs font-medium">+12%</span>
                </div>
                <span className="text-xs text-gray-500">vs last month</span>
              </div>
            </div>
            <div className="h-12 w-12 bg-blue-50 rounded-lg flex items-center justify-center">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600 mb-1">Active Departments</p>
              <p className="text-3xl font-bold text-gray-900 mb-2">12</p>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 text-green-600">
                  <UserCheck className="h-3 w-3" />
                  <span className="text-xs font-medium">All operational</span>
                </div>
              </div>
            </div>
            <div className="h-12 w-12 bg-green-50 rounded-lg flex items-center justify-center">
              <Building className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600 mb-1">Open Positions</p>
              <p className="text-3xl font-bold text-gray-900 mb-2">28</p>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 text-orange-600">
                  <AlertCircle className="h-3 w-3" />
                  <span className="text-xs font-medium">5 urgent</span>
                </div>
                <span className="text-xs text-gray-500">need attention</span>
              </div>
            </div>
            <div className="h-12 w-12 bg-orange-50 rounded-lg flex items-center justify-center">
              <Briefcase className="h-6 w-6 text-orange-600" />
            </div>
          </div>
        </div>

        <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600 mb-1">Attendance Rate</p>
              <p className="text-3xl font-bold text-gray-900 mb-2">94.5%</p>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 text-green-600">
                  <TrendingUp className="h-3 w-3" />
                  <span className="text-xs font-medium">+2.3%</span>
                </div>
                <span className="text-xs text-gray-500">improvement</span>
              </div>
            </div>
            <div className="h-12 w-12 bg-purple-50 rounded-lg flex items-center justify-center">
              <Activity className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Additional Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">New Hires This Month</p>
              <p className="text-xl font-bold text-gray-900">18</p>
            </div>
            <UserCheck className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">Avg. Time to Hire</p>
              <p className="text-xl font-bold text-gray-900">24 days</p>
            </div>
            <Clock className="h-8 w-8 text-green-500" />
          </div>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">Training Completion</p>
              <p className="text-xl font-bold text-gray-900">87%</p>
            </div>
            <Target className="h-8 w-8 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activities - Enhanced */}
        <div className="lg:col-span-2 card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Activities</h3>
            <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
          </div>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
              <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Users className="h-5 w-5 text-blue-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">New employee onboarded</p>
                <p className="text-xs text-gray-500">John Doe joined as Software Engineer in Engineering department</p>
                <p className="text-xs text-gray-400 mt-1">2 hours ago</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
              <div className="h-10 w-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Award className="h-5 w-5 text-green-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Performance review completed</p>
                <p className="text-xs text-gray-500">Sarah Smith - Marketing Manager - Exceeded expectations</p>
                <p className="text-xs text-gray-400 mt-1">5 hours ago</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
              <div className="h-10 w-10 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Calendar className="h-5 w-5 text-orange-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Leave request approved</p>
                <p className="text-xs text-gray-500">Mike Johnson - Annual leave from Dec 20-22, 2024</p>
                <p className="text-xs text-gray-400 mt-1">1 day ago</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
              <div className="h-10 w-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                <DollarSign className="h-5 w-5 text-purple-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Payroll processed successfully</p>
                <p className="text-xs text-gray-500">Monthly payroll for 1,234 employees - Total: $2.4M</p>
                <p className="text-xs text-gray-400 mt-1">2 days ago</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions & Upcoming Events */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full btn btn-outline text-left justify-start">
                <Users className="h-4 w-4 mr-2" />
                Add New Employee
              </button>
              <button className="w-full btn btn-outline text-left justify-start">
                <Calendar className="h-4 w-4 mr-2" />
                Approve Leave Request
              </button>
              <button className="w-full btn btn-outline text-left justify-start">
                <Briefcase className="h-4 w-4 mr-2" />
                Post New Job
              </button>
              <button className="w-full btn btn-outline text-left justify-start">
                <Award className="h-4 w-4 mr-2" />
                Schedule Review
              </button>
            </div>
          </div>

          {/* Upcoming Events */}
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Upcoming Events</h3>
              <button className="text-sm text-blue-600 hover:text-blue-700">Calendar</button>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors">
                <div className="h-8 w-8 bg-red-100 rounded-full flex items-center justify-center">
                  <Clock className="h-4 w-4 text-red-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Team Meeting</p>
                  <p className="text-xs text-gray-500">Engineering • 10:00 AM</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors">
                <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Users className="h-4 w-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Interview Session</p>
                  <p className="text-xs text-gray-500">Senior Developer • 2:00 PM</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors">
                <div className="h-8 w-8 bg-green-100 rounded-full flex items-center justify-center">
                  <Award className="h-4 w-4 text-green-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Training Session</p>
                  <p className="text-xs text-gray-500">Leadership Program • Dec 15</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Alerts and Notifications - Enhanced */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Action Required</h3>
          <span className="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded">3 Pending</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border border-red-200 bg-red-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-red-900">Leave Approvals</p>
                <p className="text-xs text-red-700 mt-1">3 pending requests require approval</p>
                <button className="btn btn-primary btn-sm mt-3 w-full">Review Now</button>
              </div>
            </div>
          </div>

          <div className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-yellow-900">Contract Renewals</p>
                <p className="text-xs text-yellow-700 mt-1">5 contracts expiring this month</p>
                <button className="btn btn-outline btn-sm mt-3 w-full">View Details</button>
              </div>
            </div>
          </div>

          <div className="border border-blue-200 bg-blue-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-blue-900">Performance Reviews</p>
                <p className="text-xs text-blue-700 mt-1">Q4 reviews due by Dec 31</p>
                <button className="btn btn-outline btn-sm mt-3 w-full">Start Process</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

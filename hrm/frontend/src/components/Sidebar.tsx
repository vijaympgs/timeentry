import React, { useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { 
  Users, 
  Building, 
  Calendar, 
  FileText, 
  Settings, 
  BarChart3, 
  ChevronDown, 
  ChevronRight, 
  Award, 
  Clock, 
  DollarSign, 
  GraduationCap, 
  Cog, 
  TrendingUp, 
  Menu, 
  X,
  CheckSquare,
  ClipboardList 
} from 'lucide-react'

interface NavItem {
  id: string
  label: string
  subtitle?: string
  icon: string
  children?: NavItem[]
}

const menuConfig: NavItem[] = [
  {
    id: 'hrm',
    label: 'HRM',
    subtitle: 'Human Resource Management',
    icon: 'Users',
    children: [
      {
        id: 'dashboards',
        label: 'Dashboards & Reports',
        icon: 'BarChart3',
        children: [
          { id: 'hr-dashboard', label: 'HR Dashboard', icon: 'BarChart3' },
          { id: 'analytics', label: 'Analytics Reports', icon: 'BarChart3' },
          { id: 'compliance', label: 'Compliance Reports', icon: 'FileText' },
        ]
      },
      {
        id: 'employees',
        label: 'Employee Management',
        icon: 'Users',
        children: [
          { id: 'records', label: 'Employee Records', icon: 'Users' },
          { id: 'org-chart', label: 'Organizational Chart', icon: 'Building' },
          { id: 'profile', label: 'Profile View', icon: 'UserCircle' },
        ]
      },
      {
        id: 'talent',
        label: 'Talent & Onboarding',
        icon: 'Users',
        children: [
          { id: 'applications', label: 'Application Capture', icon: 'FileText' },
          { id: 'screening', label: 'Screening', icon: 'Users' },
          { id: 'interviews', label: 'Interview Scheduling', icon: 'Calendar' },
          { id: 'offers', label: 'Offer Management', icon: 'Award' },
          { id: 'onboarding', label: 'New Hire Setup', icon: 'Users' },
        ]
      },
      {
        id: 'compensation',
        label: 'Compensation & Payroll',
        icon: 'DollarSign',
        children: [
          { id: 'salary', label: 'Salary Structures', icon: 'DollarSign' },
          { id: 'tax', label: 'Tax Calculations', icon: 'FileText' },
          { id: 'payroll', label: 'Payroll Run', icon: 'DollarSign' },
        ]
      },
      {
        id: 'time-attendance',
        label: 'Time & Attendance',
        icon: 'Clock',
        children: [
          { id: 'clock', label: 'Clock-In-Out', icon: 'Clock' },
          { id: 'timesheets', label: 'Timesheets', icon: 'FileText' },
          { id: 'approvals', label: 'Approval Workflow', icon: 'Settings' },
        ]
      },
      {
        id: 'performance',
        label: 'Performance & Goals',
        icon: 'BarChart3',
        children: [
          { id: 'goals', label: 'Goal Setting', icon: 'BarChart3' },
          { id: 'reviews', label: 'Performance Reviews', icon: 'FileText' },
          { id: 'feedback', label: '360-Degree Feedback', icon: 'Users' },
          { id: 'development', label: 'Development Plans', icon: 'Award' },
        ]
      },
      {
        id: 'learning',
        label: 'Learning',
        icon: 'GraduationCap',
        children: [
          { id: 'programs', label: 'Training Programs', icon: 'GraduationCap' },
          { id: 'courses', label: 'Course Catalog', icon: 'FileText' },
          { id: 'certifications', label: 'Certifications', icon: 'Award' },
        ]
      },
      {
        id: 'engagement',
        label: 'Engagement',
        icon: 'Users',
        children: [
          { id: 'surveys', label: 'Surveys', icon: 'FileText' },
          { id: 'recognition', label: 'Recognition Programs', icon: 'Award' },
          { id: 'wellness', label: 'Wellness Programs', icon: 'Users' },
        ]
      },
      {
        id: 'workforce',
        label: 'Workforce Planning',
        icon: 'BarChart3',
        children: [
          { id: 'headcount', label: 'Headcount Planning', icon: 'Users' },
          { id: 'succession', label: 'Succession Planning', icon: 'BarChart3' },
          { id: 'analytics', label: 'Workforce Analytics', icon: 'BarChart3' },
        ]
      },
      {
        id: 'compliance',
        label: 'Compliance',
        icon: 'FileText',
        children: [
          { id: 'policies', label: 'Policy Management', icon: 'FileText' },
          { id: 'training', label: 'Compliance Training', icon: 'GraduationCap' },
          { id: 'audit', label: 'Audit Management', icon: 'Settings' },
        ]
      },
      {
        id: 'offboarding',
        label: 'Offboarding',
        icon: 'Users',
        children: [
          { id: 'resignation', label: 'Resignation Process', icon: 'FileText' },
          { id: 'interviews', label: 'Exit Interviews', icon: 'Users' },
          { id: 'checklist', label: 'Offboarding Checklist', icon: 'FileText' },
        ]
      },
      {
        id: 'security',
        label: 'Security',
        icon: 'Settings',
        children: [
          { id: 'roles', label: 'Role-Based Access', icon: 'Users' },
          { id: 'audit-logs', label: 'Audit Logs', icon: 'FileText' },
        ]
      },
      {
        id: 'development',
        label: 'Development',
        icon: 'ClipboardList',
        children: [
          { id: 'dev-checklist', label: 'Development Checklist', icon: 'CheckSquare' },
        ]
      },
    ]
  }
]

const getIcon = (iconName: string) => {
  const icons: { [key: string]: React.ElementType } = {
    Users,
    Building,
    Calendar,
    FileText,
    Settings,
    BarChart3,
    ChevronDown,
    ChevronRight,
    Award,
    Clock,
    DollarSign,
    GraduationCap,
    Cog,
    TrendingUp,
    Menu,
    X
  }
  return icons[iconName] || Users
}

export const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set(['hrm']))
  const location = useLocation()
  
  const isActive = (href: string) => {
    return location.pathname === href || location.pathname.startsWith(href + '/')
  }

  const toggleExpanded = (itemId: string) => {
    const newExpanded = new Set(expandedItems)
    if (newExpanded.has(itemId)) {
      newExpanded.delete(itemId)
    } else {
      newExpanded.add(itemId)
    }
    setExpandedItems(newExpanded)
  }

  const renderMenuItem = (item: NavItem, level: number = 0) => {
    const Icon = getIcon(item.icon)
    const hasChildren = item.children && item.children.length > 0
    const isExpanded = expandedItems.has(item.id)
    const active = isActive(`/${item.id}`)

    return (
      <div key={item.id}>
        <button
          onClick={() => hasChildren && toggleExpanded(item.id)}
          className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-none transition-colors duration-180 ${
            active 
              ? 'bg-nexus-primary-100 text-nexus-primary-700' 
              : 'text-gray-700 hover:bg-nexus-gray-100'
          }`}
        >
          <Icon className="h-4 w-4 flex-shrink-0" />
          {!isCollapsed && (
            <>
              <span className="flex-1 text-left">{item.label}</span>
              {hasChildren && (
                <ChevronRight 
                  className={`h-4 w-4 transition-transform duration-180 ${
                    isExpanded ? 'rotate-90' : ''
                  }`}
                />
              )}
            </>
          )}
        </button>
        
        {hasChildren && !isCollapsed && isExpanded && (
          <div className="ml-4">
            {item.children?.map(child => {
              // Special handling for development section
              if (item.id === 'development') {
                return renderSubMenuItem(child, `/${item.id}`)
              }
              // Special handling for employees section
              if (item.id === 'employees') {
                return renderSubMenuItem(child, `/${item.id}`)
              }
              return renderMenuItem(child, level + 1)
            })}
          </div>
        )}
      </div>
    )
  }

  const renderSubMenuItem = (item: NavItem, parentPath: string) => {
    const Icon = getIcon(item.icon)
    const active = isActive(`${parentPath}/${item.id}`)

    return (
      <div key={item.id}>
        <NavLink
          to={`${parentPath}/${item.id}`}
          className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-none transition-colors duration-180 ${
            active 
              ? 'bg-nexus-primary-100 text-nexus-primary-700' 
              : 'text-gray-700 hover:bg-nexus-gray-100'
          }`}
        >
          <Icon className="h-4 w-4 flex-shrink-0" />
          <span className="flex-1 text-left">{item.label}</span>
        </NavLink>
      </div>
    )
  }

  return (
    <div
      className="text-text-primary font-sans min-h-screen flex flex-col transition-all duration-180 shadow-lg border-r"
      style={{
        width: isCollapsed ? '64px' : '256px',
        marginTop: 'var(--header-height)',
        backgroundColor: '#FFFFFF',
        borderColor: '#e5e7eb'
      }}
    >
      {/* HEADER: NEXUS Brand */}
      <div className="flex items-center justify-between px-4 py-4 border-b border-[#edebe9]">
        {!isCollapsed && (
          <h1 className="text-xl font-extrabold tracking-[0.3em] uppercase text-[#201f1e]">NEXUS</h1>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1 rounded-none hover:bg-nexus-gray-100 transition-colors duration-180"
        >
          <Menu className="h-5 w-5 text-[#605e5c]" />
        </button>
      </div>

      {/* NAVIGATION ITEMS */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1 scrollbar-hairline">
        {menuConfig.map((item) => renderMenuItem(item))}
      </nav>
    </div>
  )
}

import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Header } from './components/Header'
import { Dashboard } from './pages/Dashboard'
import { EmployeeRecords } from './pages/EmployeeRecords'
import { EmployeeProfile } from './pages/EmployeeProfile'
import { DevChecklist } from './pages/DevChecklist'
import VirtualOrgChart from './components/orgchart/VirtualOrgChart'

function App() {
  return (
    <div className="h-screen bg-gray-50 overflow-hidden">
      <div className="flex h-full">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <Header />
          
          {/* Page Content */}
          <main className="flex-1 overflow-hidden">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboards" element={<Dashboard />} />
              <Route path="/dashboards/hr" element={<Dashboard />} />
              <Route path="/employees/records" element={<EmployeeRecords />} />
              <Route path="/employees/profile/:id" element={<EmployeeProfile />} />
              <Route path="/employees/org-chart" element={<VirtualOrgChart />} />
              <Route path="/development/dev-checklist" element={<DevChecklist />} />
              {/* Add more routes as we develop them */}
            </Routes>
          </main>
        </div>
      </div>
    </div>
  )
}

export default App

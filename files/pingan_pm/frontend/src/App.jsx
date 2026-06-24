import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import ProjectList from './pages/ProjectList'
import ProjectDetail from './pages/ProjectDetail'
import GanttView from './pages/GanttView'
import DependencyEditor from './pages/DependencyEditor'
import ResourceCalendar from './pages/ResourceCalendar'
import BaselineCompare from './pages/BaselineCompare'
import WarningDashboard from './pages/WarningDashboard'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/projects" replace />} />
          <Route path="/projects" element={<ProjectList />} />
          <Route path="/projects/:projectId" element={<ProjectDetail />} />
          <Route path="/projects/:projectId/gantt" element={<GanttView />} />
          <Route path="/projects/:projectId/dependencies" element={<DependencyEditor />} />
          <Route path="/projects/:projectId/resources" element={<ResourceCalendar />} />
          <Route path="/projects/:projectId/baseline" element={<BaselineCompare />} />
          <Route path="/warnings" element={<WarningDashboard />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App

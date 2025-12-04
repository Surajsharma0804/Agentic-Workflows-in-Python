import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { AlertProvider } from './contexts/AlertContext'
import ErrorBoundary from './components/ErrorBoundary'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import TermsOfService from './pages/TermsOfService'
import PrivacyPolicy from './pages/PrivacyPolicy'
import Dashboard from './pages/Dashboard'
import WorkflowRunner from './pages/WorkflowRunner'
import AIAssistant from './pages/AIAssistant'
import PluginExplorer from './pages/PluginExplorer'
import AuditViewer from './pages/AuditViewer'
import DAGVisualizer from './pages/DAGVisualizer'
import Settings from './pages/Settings'
import About from './pages/About'
import Contact from './pages/Contact'

function App() {
  return (
    <ErrorBoundary>
      <AlertProvider>
        <AuthProvider>
          <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/terms-of-service" element={<TermsOfService />} />
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />

          {/* Protected Routes */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/run" element={<WorkflowRunner />} />
                    <Route path="/ai" element={<AIAssistant />} />
                    <Route path="/plugins" element={<PluginExplorer />} />
                    <Route path="/audit" element={<AuditViewer />} />
                    <Route path="/dag" element={<DAGVisualizer />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
          </Routes>
        </AuthProvider>
      </AlertProvider>
    </ErrorBoundary>
  )
}

export default App

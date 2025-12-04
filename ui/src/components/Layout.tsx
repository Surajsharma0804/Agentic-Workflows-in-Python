import { ReactNode, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Home,
  Play,
  Bot,
  Puzzle,
  FileText,
  GitBranch,
  Settings,
  Info,
  Zap,
  Bell,
  User,
  LogOut,
  ChevronDown,
  Menu,
  X,
  Mail,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuth } from '@/contexts/AuthContext'
import toast from 'react-hot-toast'

interface LayoutProps {
  children: ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Run Workflow', href: '/run', icon: Play },
  { name: 'AI Assistant', href: '/ai', icon: Bot },
  { name: 'Plugins', href: '/plugins', icon: Puzzle },
  { name: 'Audit Log', href: '/audit', icon: FileText },
  { name: 'DAG Visualizer', href: '/dag', icon: GitBranch },
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Contact', href: '/contact', icon: Mail },
  { name: 'About', href: '/about', icon: Info },
]

function UserMenu() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [isOpen, setIsOpen] = useState(false)

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <div className="relative">
      <motion.button
        whileHover={{ scale: 1.02, y: -2 }}
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center space-x-3 p-3 rounded-xl glass border-2 border-border/50 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all group"
      >
        {user?.avatar ? (
          <img src={user.avatar} alt={user.name} className="w-10 h-10 rounded-full ring-2 ring-primary/50" />
        ) : (
          <div className="w-10 h-10 rounded-full gradient-primary flex items-center justify-center shadow-glow animate-glow">
            <User className="w-5 h-5 text-white" />
          </div>
        )}
        <div className="flex-1 text-left">
          <p className="text-sm font-semibold text-text-primary">{user?.name || 'User'}</p>
          <p className="text-xs text-text-muted">{user?.email || 'user@example.com'}</p>
        </div>
        <ChevronDown className={cn(
          'w-4 h-4 text-text-muted transition-transform group-hover:text-primary',
          isOpen && 'rotate-180'
        )} />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute bottom-full left-0 right-0 mb-2 glass-strong border border-border/50 rounded-xl shadow-2xl overflow-hidden"
          >
            <Link
              to="/settings"
              onClick={() => setIsOpen(false)}
              className="flex items-center space-x-3 px-4 py-3 hover:glass hover:bg-primary/10 transition-all hover-lift"
            >
              <Settings className="w-4 h-4 text-text-secondary" />
              <span className="text-sm text-text-primary">Settings</span>
            </Link>
            <button
              onClick={handleLogout}
              className="w-full flex items-center space-x-3 px-4 py-3 hover:glass hover:bg-danger-500/10 transition-all text-danger-400 hover-lift"
            >
              <LogOut className="w-4 h-4" />
              <span className="text-sm">Logout</span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen flex bg-bg">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsMobileMenuOpen(false)}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar - Desktop (always visible) & Mobile Drawer */}
      <aside className="hidden lg:flex lg:relative inset-y-0 left-0 w-72 glass-strong border-r-2 border-border/30 flex-col z-50 backdrop-blur-xl">
        {/* Desktop Sidebar Content */}
        {/* Logo */}
        <div className="p-6 border-b-2 border-border/30 flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 group">
            <motion.div
              whileHover={{ rotate: 360, scale: 1.1 }}
              transition={{ duration: 0.5 }}
              className="p-2 rounded-xl gradient-primary shadow-glow animate-glow"
            >
              <Zap className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h1 className="text-xl font-bold gradient-text">Agentic</h1>
              <p className="text-xs text-text-muted">Workflows Platform</p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon

            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 relative group',
                  isActive
                    ? 'gradient-primary text-text-inverse shadow-glow animate-glow'
                    : 'text-text-secondary hover:glass hover:text-text-primary hover-lift'
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute inset-0 gradient-primary rounded-xl shadow-xl"
                    transition={{ type: 'spring', duration: 0.6 }}
                  />
                )}
                <Icon className="w-5 h-5 relative z-10" />
                <span className="font-medium relative z-10">{item.name}</span>
                {isActive && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="ml-auto w-2 h-2 bg-white rounded-full relative z-10 shadow-lg"
                  />
                )}
              </Link>
            )
          })}
        </nav>

        {/* User Section */}
        <div className="p-4 border-t-2 border-border/30">
          <UserMenu />
        </div>

        {/* Footer */}
        <div className="p-4 border-t-2 border-border/30">
          <div className="text-xs text-text-muted text-center space-y-1">
            <p className="font-medium gradient-text">v2.0.0</p>
            <div className="flex items-center justify-center space-x-2 mt-2">
              <motion.div 
                animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-2 h-2 bg-success-500 rounded-full shadow-lg shadow-success-500/50"
              />
              <span className="text-success-500 font-semibold">Online</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar Drawer */}
      <motion.aside
        initial={false}
        animate={{
          x: isMobileMenuOpen ? 0 : '-100%',
        }}
        transition={{ duration: 0.3, type: 'spring', damping: 25 }}
        className="fixed lg:hidden inset-y-0 left-0 w-72 glass-strong border-r-2 border-border/30 flex flex-col z-50 backdrop-blur-xl"
      >
        {/* Mobile Logo & Close Button */}
        <div className="p-6 border-b-2 border-border flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 group" onClick={() => setIsMobileMenuOpen(false)}>
            <motion.div
              whileHover={{ rotate: 360, scale: 1.1 }}
              transition={{ duration: 0.5 }}
              className="p-2 rounded-xl bg-gradient-to-br from-primary to-accent shadow-glow"
            >
              <Zap className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h1 className="text-xl font-bold text-text-primary">Agentic</h1>
              <p className="text-xs text-text-muted">Workflows Platform</p>
            </div>
          </Link>
          
          {/* Close button for mobile */}
          <button
            onClick={() => setIsMobileMenuOpen(false)}
            className="lg:hidden p-2 rounded-lg hover:bg-bg-secondary transition-colors"
            aria-label="Close menu"
          >
            <X className="w-6 h-6 text-text-primary" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon

            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  'flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 relative group',
                  isActive
                    ? 'gradient-primary text-text-inverse shadow-glow animate-glow'
                    : 'text-text-secondary hover:glass hover:text-text-primary hover-lift'
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNavMobile"
                    className="absolute inset-0 gradient-primary rounded-xl shadow-xl"
                    transition={{ type: 'spring', duration: 0.6 }}
                  />
                )}
                <Icon className="w-5 h-5 relative z-10" />
                <span className="font-medium relative z-10">{item.name}</span>
                {isActive && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="ml-auto w-2 h-2 bg-white rounded-full relative z-10 shadow-lg"
                  />
                )}
              </Link>
            )
          })}
        </nav>

        {/* User Section */}
        <div className="p-4 border-t-2 border-border/30">
          <UserMenu />
        </div>

        {/* Footer */}
        <div className="p-4 border-t-2 border-border/30">
          <div className="text-xs text-text-muted text-center space-y-1">
            <p className="font-medium gradient-text">v2.0.0</p>
            <div className="flex items-center justify-center space-x-2 mt-2">
              <motion.div 
                animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-2 h-2 bg-success-500 rounded-full shadow-lg shadow-success-500/50"
              />
              <span className="text-success-500 font-semibold">Online</span>
            </div>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className="glass-strong border-b-2 border-border/30 px-4 sm:px-6 lg:px-8 py-4 sticky top-0 z-30 backdrop-blur-xl">
          <div className="flex items-center justify-between">
            {/* Hamburger Menu (Mobile) */}
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className="lg:hidden p-2 rounded-lg hover:bg-bg-secondary transition-colors"
              aria-label="Open menu"
            >
              <Menu className="w-6 h-6 text-text-primary" />
            </button>

            {/* Page Title */}
            <div className="flex-1 lg:flex-none">
              <h2 className="text-lg sm:text-xl font-semibold gradient-text">
                {navigation.find(n => n.href === location.pathname)?.name || 'Dashboard'}
              </h2>
              <p className="text-xs sm:text-sm text-text-muted hidden sm:block">
                {new Date().toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  month: 'short', 
                  day: 'numeric',
                  year: 'numeric'
                })}
              </p>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              <motion.button
                whileHover={{ scale: 1.1, y: -2 }}
                whileTap={{ scale: 0.9 }}
                className="relative p-2 rounded-lg glass hover:shadow-lg hover:shadow-primary/20 transition-all"
                aria-label="Notifications"
              >
                <Bell className="w-5 h-5 text-text-primary" />
                <motion.span 
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full shadow-lg shadow-danger-500/50"
                />
              </motion.button>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                {children}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  )
}

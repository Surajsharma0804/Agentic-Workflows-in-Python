import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  Activity,
  CheckCircle,
  XCircle,
  Clock,
  Zap,
  TrendingUp,
  Server,
  Database,
  Cpu,
  Play,
  Eye,
  FileText,
} from 'lucide-react'
import { healthAPI, workflowAPI } from '@/lib/api'
import { formatDuration } from '@/lib/utils'
import StatCard from '@/components/StatCard'
import ActivityChart from '@/components/ActivityChart'
import { CardSkeleton, TableSkeleton } from '@/components/LoadingSkeleton'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const navigate = useNavigate()
  const [selectedPeriod, setSelectedPeriod] = useState('7d')

  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => healthAPI.check(),
    refetchInterval: 5000,
  })

  const { data: workflows, isLoading: workflowsLoading } = useQuery({
    queryKey: ['workflows'],
    queryFn: () => workflowAPI.list(),
    refetchInterval: 10000,
  })

  // Generate mock activity data for chart
  const activityData = [
    { name: 'Mon', value: 12 },
    { name: 'Tue', value: 19 },
    { name: 'Wed', value: 15 },
    { name: 'Thu', value: 25 },
    { name: 'Fri', value: 22 },
    { name: 'Sat', value: 18 },
    { name: 'Sun', value: 20 },
  ]

  const stats = [
    {
      title: 'Total Workflows',
      value: workflows?.data?.length || 0,
      icon: Activity,
      color: 'blue' as const,
      trend: { value: 12, isPositive: true },
    },
    {
      title: 'Successful',
      value: workflows?.data?.filter((w: any) => w.status === 'success').length || 0,
      icon: CheckCircle,
      color: 'green' as const,
      trend: { value: 8, isPositive: true },
    },
    {
      title: 'Failed',
      value: workflows?.data?.filter((w: any) => w.status === 'failed').length || 0,
      icon: XCircle,
      color: 'red' as const,
      trend: { value: 3, isPositive: false },
    },
    {
      title: 'Running',
      value: workflows?.data?.filter((w: any) => w.status === 'running').length || 0,
      icon: Clock,
      color: 'yellow' as const,
    },
  ]

  return (
    <div className="space-y-8 relative">
      {/* Subtle Background Gradient */}
      <div className="fixed inset-0 z-0 opacity-30 pointer-events-none" style={{ background: 'var(--gradient-mesh)' }} />
      
      {/* Animated Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10"
      >
        <h1 className="text-5xl font-bold mb-3 animate-slide-down">
          Welcome to <span className="gradient-text animate-glow">Agentic Workflows</span>
        </h1>
        <p className="text-xl text-text-secondary animate-fade-in">
          Elite AI-powered workflow automation platform
        </p>
      </motion.div>

      {/* System Status Banner */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card-glass relative overflow-hidden hover-lift p-6 rounded-2xl"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600/10 to-accent-600/10 animate-shimmer" />
        <div className="relative flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center space-x-4">
            <motion.div
              animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              className="w-4 h-4 bg-success-500 rounded-full shadow-lg shadow-success-500/50 animate-pulse"
            />
            <div>
              <span className="text-xl font-semibold gradient-text">System Status</span>
              <p className="text-sm text-text-secondary mt-1">All systems operational</p>
            </div>
          </div>
          {health?.data && (
            <div className="flex items-center space-x-8">
              <motion.div 
                className="text-center"
                whileHover={{ scale: 1.1, y: -2 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Server className="w-6 h-6 text-primary-400 mx-auto mb-1 animate-pulse" />
                <p className="text-xs text-text-muted">API</p>
                <p className="text-sm font-semibold text-success-400">Online</p>
              </motion.div>
              <motion.div 
                className="text-center"
                whileHover={{ scale: 1.1, y: -2 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Database className="w-6 h-6 text-accent-400 mx-auto mb-1 animate-pulse" />
                <p className="text-xs text-text-muted">Database</p>
                <p className="text-sm font-semibold text-success-400">Connected</p>
              </motion.div>
              <motion.div 
                className="text-center"
                whileHover={{ scale: 1.1, y: -2 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Cpu className="w-6 h-6 text-info-400 mx-auto mb-1 animate-pulse" />
                <p className="text-xs text-text-muted">Workers</p>
                <p className="text-sm font-semibold text-success-400">Active</p>
              </motion.div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {workflowsLoading ? (
          <>
            <CardSkeleton />
            <CardSkeleton />
            <CardSkeleton />
            <CardSkeleton />
          </>
        ) : (
          stats.map((stat, index) => (
            <StatCard key={stat.title} {...stat} delay={index * 0.1} />
          ))
        )}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ActivityChart
          data={activityData}
          title="Workflow Activity (Last 7 Days)"
          color="#3b82f6"
        />
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card-glass hover-lift p-6 rounded-2xl"
        >
          <h3 className="text-lg font-semibold mb-4 gradient-text">Performance Metrics</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-text-secondary">Success Rate</span>
                <span className="font-semibold text-success-400">94%</span>
              </div>
              <div className="h-2 bg-surface rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '94%' }}
                  transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
                  className="h-full bg-gradient-to-r from-success-600 to-success-400 rounded-full shadow-lg shadow-success-500/30"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-text-secondary">Avg. Execution Time</span>
                <span className="font-semibold text-primary-400">2.3s</span>
              </div>
              <div className="h-2 bg-surface rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '65%' }}
                  transition={{ duration: 1, delay: 0.7, ease: "easeOut" }}
                  className="h-full bg-gradient-to-r from-primary-600 to-primary-400 rounded-full shadow-lg shadow-primary-500/30"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-text-secondary">Resource Usage</span>
                <span className="font-semibold text-warning-400">45%</span>
              </div>
              <div className="h-2 bg-surface rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '45%' }}
                  transition={{ duration: 1, delay: 0.9, ease: "easeOut" }}
                  className="h-full bg-gradient-to-r from-warning-600 to-warning-400 rounded-full shadow-lg shadow-warning-500/30"
                />
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card-glass hover-lift p-6 rounded-2xl"
      >
        <h2 className="text-2xl font-bold mb-6 gradient-text">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <motion.button
            whileHover={{ scale: 1.05, y: -4 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/run')}
            className="btn-gradient btn-glow flex items-center justify-center space-x-3 py-4 px-6 rounded-xl text-white font-semibold shadow-lg"
          >
            <Play className="w-5 h-5" />
            <span>Run New Workflow</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05, y: -4 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/dag')}
            className="glass hover-lift flex items-center justify-center space-x-3 py-4 px-6 rounded-xl font-semibold border-2 border-border/50 hover:border-primary transition-all"
          >
            <Eye className="w-5 h-5" />
            <span>View DAG</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05, y: -4 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/audit')}
            className="glass hover-lift flex items-center justify-center space-x-3 py-4 px-6 rounded-xl font-semibold border-2 border-border/50 hover:border-primary transition-all"
          >
            <FileText className="w-5 h-5" />
            <span>Check Audit Log</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Recent Workflows */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="card-glass hover-lift p-6 rounded-2xl"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold gradient-text">Recent Workflows</h2>
          <motion.button 
            whileHover={{ x: 5 }}
            className="text-sm text-primary-400 hover:text-primary-300 transition-colors font-semibold"
          >
            View All →
          </motion.button>
        </div>
        {workflowsLoading ? (
          <TableSkeleton rows={5} />
        ) : workflows?.data?.length > 0 ? (
          <div className="space-y-3">
            {workflows.data.slice(0, 5).map((workflow: any, index: number) => (
              <motion.div
                key={workflow.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                whileHover={{ scale: 1.02, x: 10 }}
                className="flex items-center justify-between p-4 glass rounded-xl border border-border/30 hover:border-primary/50 transition-all cursor-pointer hover-lift"
              >
                <div className="flex items-center space-x-4">
                  <motion.div 
                    className="w-10 h-10 rounded-full gradient-primary flex items-center justify-center shadow-lg"
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                  >
                    <Activity className="w-5 h-5 text-white" />
                  </motion.div>
                  <div>
                    <p className="font-medium text-text-primary">{workflow.name || workflow.id}</p>
                    <p className="text-sm text-text-secondary">{workflow.created_at || 'Just now'}</p>
                  </div>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    workflow.status === 'success'
                      ? 'bg-success-500/20 text-success-400 border border-success-500/30'
                      : workflow.status === 'failed'
                      ? 'bg-danger-500/20 text-danger-400 border border-danger-500/30'
                      : 'bg-warning-500/20 text-warning-400 border border-warning-500/30'
                  }`}
                >
                  {workflow.status || 'pending'}
                </span>
              </motion.div>
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="text-center py-12"
          >
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            >
              <Zap className="w-16 h-16 text-primary-400 mx-auto mb-4 animate-glow" />
            </motion.div>
            <p className="text-text-secondary text-lg mb-4">
              No workflows yet. Ready to get started?
            </p>
            <motion.button
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/run')}
              className="btn-gradient btn-glow px-8 py-3 rounded-xl text-white font-semibold shadow-lg"
            >
              Create Your First Workflow
            </motion.button>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}

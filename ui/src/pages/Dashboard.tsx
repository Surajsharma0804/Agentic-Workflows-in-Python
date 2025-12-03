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
    <div className="space-y-8">
      {/* Animated Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-5xl font-bold mb-3">
          Welcome to <span className="glow-text">Agentic Workflows</span>
        </h1>
        <p className="text-xl text-gray-400">
          Elite AI-powered workflow automation platform
        </p>
      </motion.div>

      {/* System Status Banner */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card-gradient relative overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10" />
        <div className="relative flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-4 h-4 bg-green-500 rounded-full shadow-lg shadow-green-500/50"
            />
            <div>
              <span className="text-xl font-semibold">System Status</span>
              <p className="text-sm text-gray-400 mt-1">All systems operational</p>
            </div>
          </div>
          {health?.data && (
            <div className="flex items-center space-x-8">
              <div className="text-center">
                <Server className="w-6 h-6 text-blue-400 mx-auto mb-1" />
                <p className="text-xs text-gray-400">API</p>
                <p className="text-sm font-semibold text-green-400">Online</p>
              </div>
              <div className="text-center">
                <Database className="w-6 h-6 text-purple-400 mx-auto mb-1" />
                <p className="text-xs text-gray-400">Database</p>
                <p className="text-sm font-semibold text-green-400">Connected</p>
              </div>
              <div className="text-center">
                <Cpu className="w-6 h-6 text-cyan-400 mx-auto mb-1" />
                <p className="text-xs text-gray-400">Workers</p>
                <p className="text-sm font-semibold text-green-400">Active</p>
              </div>
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
          className="card"
        >
          <h3 className="text-lg font-semibold mb-4">Performance Metrics</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Success Rate</span>
                <span className="font-semibold text-green-400">94%</span>
              </div>
              <div className="progress">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '94%' }}
                  transition={{ duration: 1, delay: 0.5 }}
                  className="progress-bar"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Avg. Execution Time</span>
                <span className="font-semibold text-blue-400">2.3s</span>
              </div>
              <div className="progress">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '65%' }}
                  transition={{ duration: 1, delay: 0.7 }}
                  className="progress-bar"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Resource Usage</span>
                <span className="font-semibold text-yellow-400">45%</span>
              </div>
              <div className="progress">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '45%' }}
                  transition={{ duration: 1, delay: 0.9 }}
                  className="progress-bar"
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
        className="card"
      >
        <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/run')}
            className="btn-neon flex items-center justify-center space-x-3 py-4"
          >
            <Play className="w-5 h-5" />
            <span>Run New Workflow</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/dag')}
            className="btn-secondary flex items-center justify-center space-x-3 py-4"
          >
            <Eye className="w-5 h-5" />
            <span>View DAG</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/audit')}
            className="btn-secondary flex items-center justify-center space-x-3 py-4"
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
        className="card"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">Recent Workflows</h2>
          <button className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
            View All →
          </button>
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
                className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg border border-gray-800 hover:border-gray-700 transition-all cursor-pointer"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <Activity className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="font-medium">{workflow.name || workflow.id}</p>
                    <p className="text-sm text-gray-400">{workflow.created_at || 'Just now'}</p>
                  </div>
                </div>
                <span
                  className={`badge ${
                    workflow.status === 'success'
                      ? 'badge-success'
                      : workflow.status === 'failed'
                      ? 'badge-error'
                      : 'badge-warning'
                  }`}
                >
                  {workflow.status || 'pending'}
                </span>
              </motion.div>
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <Zap className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 text-lg mb-4">
              No workflows yet. Ready to get started?
            </p>
            <button
              onClick={() => navigate('/run')}
              className="btn-primary"
            >
              Create Your First Workflow
            </button>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}

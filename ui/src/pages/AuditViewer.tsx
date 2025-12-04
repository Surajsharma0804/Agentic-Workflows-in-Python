import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  FileText,
  Search,
  Download,
  CheckCircle,
  XCircle,
  Clock,
  AlertTriangle,
} from 'lucide-react'
import { TableSkeleton } from '@/components/LoadingSkeleton'

export default function AuditViewer() {
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [dateRange, setDateRange] = useState('7d')

  const { data: auditLogs, isLoading } = useQuery({
    queryKey: ['audit', statusFilter, dateRange],
    queryFn: async () => {
      // Mock audit data
      return {
        data: Array.from({ length: 20 }, (_, i) => ({
          id: `audit_${i + 1}`,
          timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
          workflow_id: `wf_${Math.floor(Math.random() * 100)}`,
          workflow_name: ['File Organization', 'Data Pipeline', 'Email Processing', 'Web Scraping'][Math.floor(Math.random() * 4)],
          action: ['workflow_started', 'workflow_completed', 'workflow_failed', 'task_executed'][Math.floor(Math.random() * 4)],
          status: ['success', 'failed', 'warning'][Math.floor(Math.random() * 3)],
          user: 'admin@agentic.ai',
          duration: (Math.random() * 5 + 0.5).toFixed(2),
          details: 'Workflow executed successfully with all tasks completed',
        })),
      }
    },
  })

  const filteredLogs = auditLogs?.data?.filter((log: any) => {
    const matchesSearch = log.workflow_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         log.action.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === 'all' || log.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-400" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-400" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-400" />
      default:
        return <Clock className="w-5 h-5 text-blue-400" />
    }
  }

  const exportLogs = () => {
    const csv = [
      ['Timestamp', 'Workflow', 'Action', 'Status', 'Duration', 'User'].join(','),
      ...filteredLogs.map((log: any) => 
        [log.timestamp, log.workflow_name, log.action, log.status, log.duration, log.user].join(',')
      )
    ].join('\\n')
    
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `audit-logs-${Date.now()}.csv`
    a.click()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">Audit Log</span>
        </h1>
        <p className="text-xl text-gray-400">
          Track and monitor all workflow activities
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search logs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
          </div>
          
          <div className="flex gap-3">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            >
              <option value="all">All Status</option>
              <option value="success">Success</option>
              <option value="failed">Failed</option>
              <option value="warning">Warning</option>
            </select>
            
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            >
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="all">All Time</option>
            </select>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={exportLogs}
              className="btn-secondary flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Export</span>
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Events', value: auditLogs?.data?.length || 0, icon: FileText, color: 'blue' },
          { label: 'Successful', value: auditLogs?.data?.filter((l: any) => l.status === 'success').length || 0, icon: CheckCircle, color: 'green' },
          { label: 'Failed', value: auditLogs?.data?.filter((l: any) => l.status === 'failed').length || 0, icon: XCircle, color: 'red' },
          { label: 'Warnings', value: auditLogs?.data?.filter((l: any) => l.status === 'warning').length || 0, icon: AlertTriangle, color: 'yellow' },
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + index * 0.1 }}
            className="card"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">{stat.label}</p>
                <p className="text-2xl font-bold mt-1">{stat.value}</p>
              </div>
              <stat.icon className={`w-8 h-8 text-${stat.color}-400`} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Audit Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        
        {isLoading ? (
          <TableSkeleton rows={10} />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-gray-800">
                <tr>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Status</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Timestamp</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Workflow</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Action</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Duration</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">User</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs?.map((log: any, index: number) => (
                  <motion.tr
                    key={log.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.02 }}
                    className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-4">
                      {getStatusIcon(log.status)}
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-300">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="py-4 px-4 text-sm font-medium">
                      {log.workflow_name}
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-400">
                      {log.action.replace(/_/g, ' ')}
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-400">
                      {log.duration}s
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-400">
                      {log.user}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>
    </div>
  )
}

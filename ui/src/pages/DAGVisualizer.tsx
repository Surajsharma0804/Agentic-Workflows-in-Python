import { motion } from 'framer-motion'
import { GitBranch, Play, CheckCircle, XCircle, Clock } from 'lucide-react'

export default function DAGVisualizer() {
  const nodes = [
    { id: 'start', label: 'Start', status: 'completed', x: 50, y: 50 },
    { id: 'task1', label: 'File Organizer', status: 'completed', x: 200, y: 50 },
    { id: 'task2', label: 'HTTP Request', status: 'running', x: 350, y: 50 },
    { id: 'task3', label: 'Data Transform', status: 'pending', x: 500, y: 50 },
    { id: 'end', label: 'End', status: 'pending', x: 650, y: 50 },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500'
      case 'running': return 'bg-blue-500 animate-pulse'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-600'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5" />
      case 'running': return <Clock className="w-5 h-5 animate-spin" />
      case 'failed': return <XCircle className="w-5 h-5" />
      default: return <Play className="w-5 h-5" />
    }
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">DAG Visualizer</span>
        </h1>
        <p className="text-xl text-gray-400">
          Visualize workflow execution graphs
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Nodes', value: 5, icon: GitBranch, color: 'blue' },
          { label: 'Completed', value: 2, icon: CheckCircle, color: 'green' },
          { label: 'Running', value: 1, icon: Clock, color: 'yellow' },
          { label: 'Pending', value: 2, icon: Play, color: 'gray' },
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
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

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <h3 className="text-lg font-semibold mb-6">Workflow Execution Graph</h3>
        
        <div className="relative h-96 bg-gray-950 rounded-lg border border-gray-800 overflow-hidden">
          <svg className="w-full h-full">
            {/* Connections */}
            {nodes.slice(0, -1).map((node, i) => (
              <motion.line
                key={`line-${i}`}
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.5, delay: i * 0.2 }}
                x1={node.x + 60}
                y1={node.y + 100}
                x2={nodes[i + 1].x}
                y2={nodes[i + 1].y + 100}
                stroke="#3b82f6"
                strokeWidth="2"
                strokeDasharray="5,5"
              />
            ))}
          </svg>

          {/* Nodes */}
          {nodes.map((node, index) => (
            <motion.div
              key={node.id}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.2 }}
              className="absolute"
              style={{ left: node.x, top: node.y }}
            >
              <div className={`w-32 p-4 rounded-xl border-2 ${getStatusColor(node.status)} bg-gray-900 border-gray-700 hover:border-blue-500 transition-all cursor-pointer`}>
                <div className="flex items-center justify-between mb-2">
                  {getStatusIcon(node.status)}
                  <span className="text-xs text-gray-400">{node.status}</span>
                </div>
                <p className="text-sm font-medium">{node.label}</p>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-6 flex items-center justify-between">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full" />
              <span className="text-gray-400">Completed</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse" />
              <span className="text-gray-400">Running</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-gray-600 rounded-full" />
              <span className="text-gray-400">Pending</span>
            </div>
          </div>
          
          <button className="btn-primary">
            Refresh Graph
          </button>
        </div>
      </motion.div>
    </div>
  )
}

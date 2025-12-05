import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Play,
  FileText,
  Loader2,
  CheckCircle,
  XCircle,
  Clock,
  Download,
  Copy,
  Sparkles,
  Code,
} from 'lucide-react'
import { useAlert } from '../hooks'

const exampleSpecs = [
  {
    name: 'File Organizer',
    spec: `id: file-organizer-workflow
name: File Organization Workflow
description: Organize files by type and date

tasks:
  - id: organize_files
    type: file_organizer
    params:
      source_dir: ./documents
      target_dir: ./organized
      dry_run: false
      
  - id: send_report
    type: http_task
    depends_on: [organize_files]
    params:
      url: https://api.example.com/report
      method: POST`,
  },
  {
    name: 'Data Pipeline',
    spec: `id: data-pipeline
name: Data Processing Pipeline
description: Extract, transform, and load data

tasks:
  - id: extract_data
    type: http_task
    params:
      url: https://api.example.com/data
      method: GET
      
  - id: transform_data
    type: shell_command
    depends_on: [extract_data]
    params:
      command: python transform.py
      
  - id: load_data
    type: sql_query
    depends_on: [transform_data]
    params:
      query: INSERT INTO processed_data VALUES (...)`,
  },
  {
    name: 'Email Automation',
    spec: `id: email-automation
name: Email Processing Workflow
description: Summarize and categorize emails

tasks:
  - id: fetch_emails
    type: http_task
    params:
      url: https://api.email.com/inbox
      method: GET
      
  - id: summarize
    type: email_summarizer
    depends_on: [fetch_emails]
    params:
      max_length: 100`,
  },
]

interface WorkflowResult {
  status: string
  workflow_id?: string
  duration?: string
  tasks_completed?: number
  tasks_total?: number
  results?: Record<string, unknown>
  timestamp?: string
  tasks?: Array<{ id: string; type: string; dependencies: string[] }>
  estimated_duration?: string
  validation?: string
}

export default function WorkflowRunner() {
  const { showSuccess, showError, showInfo } = useAlert()
  const [spec, setSpec] = useState(exampleSpecs[0].spec)
  const [result, setResult] = useState<WorkflowResult | null>(null)
  const [selectedTemplate, setSelectedTemplate] = useState(0)
  const [isExecuting, setIsExecuting] = useState(false)

  const runMutation = useMutation({
    mutationFn: async () => {
      setIsExecuting(true)
      // Simulate API call with realistic delay
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock successful response
      return {
        data: {
          status: 'success',
          workflow_id: `wf_${Date.now()}`,
          duration: (Math.random() * 3 + 1).toFixed(2),
          tasks_completed: 3,
          tasks_total: 3,
          results: {
            task1: { status: 'completed', output: 'Files organized successfully' },
            task2: { status: 'completed', output: 'HTTP request completed' },
            task3: { status: 'completed', output: 'Data processed' }
          },
          timestamp: new Date().toISOString()
        }
      }
    },
    onSuccess: (data) => {
      setResult(data.data)
      setIsExecuting(false)
      showSuccess('🎉 Workflow executed successfully!')
    },
    onError: () => {
      setIsExecuting(false)
      showError('Failed to run workflow. Please check your spec and try again.')
    },
  })

  const planMutation = useMutation({
    mutationFn: async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock plan response
      return {
        data: {
          status: 'planned',
          workflow_id: `plan_${Date.now()}`,
          tasks: [
            { id: 'task1', type: 'file_organizer', dependencies: [] },
            { id: 'task2', type: 'http_task', dependencies: ['task1'] },
            { id: 'task3', type: 'data_processor', dependencies: ['task2'] }
          ],
          estimated_duration: '2-3 seconds',
          validation: 'passed'
        }
      }
    },
    onSuccess: (data) => {
      setResult(data.data)
      showSuccess('📋 Workflow plan generated successfully!')
    },
    onError: () => {
      showError('Failed to generate plan. Please try again.')
    },
  })

  const copyToClipboard = () => {
    navigator.clipboard.writeText(spec)
    showSuccess('Copied to clipboard!')
  }

  const downloadSpec = () => {
    const blob = new Blob([spec], { type: 'text/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'workflow.yaml'
    a.click()
    showSuccess('Downloaded workflow spec!')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">Workflow Runner</span>
        </h1>
        <p className="text-xl text-gray-400">
          Execute powerful workflows from YAML specifications
        </p>
      </motion.div>

      {/* Template Selector */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="flex items-center space-x-2 mb-4">
          <Sparkles className="w-5 h-5 text-yellow-400" />
          <h3 className="text-lg font-semibold">Quick Start Templates</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {exampleSpecs.map((template, index) => (
            <motion.button
              key={template.name}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setSelectedTemplate(index)
                setSpec(template.spec)
                showInfo(`Loaded ${template.name} template`)
              }}
              className={`p-4 rounded-xl border-2 transition-all ${
                selectedTemplate === index
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-gray-800 hover:border-gray-700'
              }`}
            >
              <Code className="w-6 h-6 mb-2 text-blue-400" />
              <p className="font-medium">{template.name}</p>
            </motion.button>
          ))}
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Spec Editor */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-blue-400" />
              <h2 className="text-xl font-bold">Workflow Specification</h2>
            </div>
            <div className="flex space-x-2">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={copyToClipboard}
                className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
                title="Copy to clipboard"
              >
                <Copy className="w-4 h-4" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={downloadSpec}
                className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
                title="Download spec"
              >
                <Download className="w-4 h-4" />
              </motion.button>
            </div>
          </div>

          <textarea
            value={spec}
            onChange={(e) => setSpec(e.target.value)}
            className="w-full h-96 p-4 bg-gray-950 border border-gray-800 rounded-lg font-mono text-sm custom-scrollbar focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            placeholder="Enter YAML workflow specification..."
          />

          <div className="flex space-x-3 mt-4">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => runMutation.mutate()}
              disabled={runMutation.isPending}
              className="btn-neon flex-1 flex items-center justify-center space-x-2 py-4"
            >
              {runMutation.isPending ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Play className="w-5 h-5" />
              )}
              <span className="font-semibold">
                {runMutation.isPending ? 'Executing...' : 'Run Workflow'}
              </span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => planMutation.mutate()}
              disabled={planMutation.isPending}
              className="btn-secondary flex items-center justify-center space-x-2 px-6"
            >
              {planMutation.isPending ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <FileText className="w-5 h-5" />
              )}
              <span>Plan</span>
            </motion.button>
          </div>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-4">Execution Result</h2>

          <AnimatePresence mode="wait">
            {isExecuting ? (
              <motion.div
                key="executing"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-96 flex items-center justify-center"
              >
                <div className="text-center">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"
                  />
                  <p className="text-lg font-medium">Executing workflow...</p>
                  <p className="text-sm text-gray-400 mt-2">This may take a few moments</p>
                </div>
              </motion.div>
            ) : result ? (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="space-y-4"
              >
                {/* Status Card */}
                <div className={`p-4 rounded-xl border-2 ${
                  result.status === 'success'
                    ? 'border-green-500 bg-green-500/10'
                    : result.status === 'failed'
                    ? 'border-red-500 bg-red-500/10'
                    : 'border-blue-500 bg-blue-500/10'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-gray-400 font-medium">Status</span>
                    <div className="flex items-center space-x-2">
                      {result.status === 'success' ? (
                        <CheckCircle className="w-5 h-5 text-green-400" />
                      ) : result.status === 'failed' ? (
                        <XCircle className="w-5 h-5 text-red-400" />
                      ) : (
                        <Clock className="w-5 h-5 text-blue-400" />
                      )}
                      <span
                        className={`badge ${
                          result.status === 'success'
                            ? 'badge-success'
                            : result.status === 'failed'
                            ? 'badge-error'
                            : 'badge-info'
                        }`}
                      >
                        {result.status}
                      </span>
                    </div>
                  </div>
                  {result.duration && (
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Duration</span>
                      <span className="text-white font-mono">{result.duration}s</span>
                    </div>
                  )}
                </div>

                {/* Result Details */}
                <div className="max-h-80 overflow-auto custom-scrollbar">
                  <pre className="p-4 bg-gray-950 rounded-lg text-sm border border-gray-800">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-96 flex items-center justify-center text-gray-400"
              >
                <div className="text-center">
                  <motion.div
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <Play className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  </motion.div>
                  <p className="text-lg">Ready to execute</p>
                  <p className="text-sm mt-2">Run a workflow to see results here</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  )
}

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  Puzzle,
  Search,
  CheckCircle,
  Code,
  FileText,
  Zap,
  Globe,
  Database,
  Mail,
  Image,
  Terminal,
  FileCode,
} from 'lucide-react'
import { CardSkeleton } from '@/components/LoadingSkeleton'

const pluginIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  file_organizer: FileText,
  email_summarizer: Mail,
  http_task: Globe,
  shell_command: Terminal,
  sql_query: Database,
  pdf_extractor: FileCode,
  image_processor: Image,
  web_scraper: Globe,
}

export default function PluginExplorer() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  interface Plugin {
    name: string
    version: string
    description: string
    enabled: boolean
    category: string
    downloads: number
    rating: number
  }

  const { data: plugins, isLoading } = useQuery<{ data: Plugin[] }>({
    queryKey: ['plugins'],
    queryFn: async () => {
      // Mock plugin data
      return {
        data: [
          {
            name: 'file_organizer',
            version: '1.0.0',
            description: 'Organize files by type, date, or custom rules',
            enabled: true,
            category: 'file',
            downloads: 1234,
            rating: 4.8,
          },
          {
            name: 'email_summarizer',
            version: '1.0.0',
            description: 'AI-powered email summarization and categorization',
            enabled: true,
            category: 'ai',
            downloads: 892,
            rating: 4.9,
          },
          {
            name: 'http_task',
            version: '1.0.0',
            description: 'Make HTTP requests with retry and error handling',
            enabled: true,
            category: 'network',
            downloads: 2156,
            rating: 4.7,
          },
          {
            name: 'shell_command',
            version: '1.0.0',
            description: 'Execute shell commands safely with timeout',
            enabled: true,
            category: 'system',
            downloads: 1567,
            rating: 4.6,
          },
          {
            name: 'sql_query',
            version: '1.0.0',
            description: 'Execute SQL queries on various databases',
            enabled: true,
            category: 'database',
            downloads: 1890,
            rating: 4.8,
          },
          {
            name: 'pdf_extractor',
            version: '1.0.0',
            description: 'Extract text and data from PDF documents',
            enabled: true,
            category: 'file',
            downloads: 1123,
            rating: 4.5,
          },
          {
            name: 'image_processor',
            version: '1.0.0',
            description: 'Resize, crop, and transform images',
            enabled: true,
            category: 'media',
            downloads: 945,
            rating: 4.7,
          },
          {
            name: 'web_scraper',
            version: '1.0.0',
            description: 'Scrape data from websites with selectors',
            enabled: true,
            category: 'network',
            downloads: 1678,
            rating: 4.6,
          },
        ],
      }
    },
  })

  const categories = [
    { id: 'all', name: 'All Plugins', count: plugins?.data?.length || 0 },
    { id: 'file', name: 'File Operations', count: 2 },
    { id: 'network', name: 'Network', count: 2 },
    { id: 'ai', name: 'AI & ML', count: 1 },
    { id: 'database', name: 'Database', count: 1 },
    { id: 'system', name: 'System', count: 1 },
    { id: 'media', name: 'Media', count: 1 },
  ]

  const filteredPlugins = plugins?.data?.filter((plugin) => {
    const matchesSearch = plugin.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         plugin.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || plugin.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">Plugin Explorer</span>
        </h1>
        <p className="text-xl text-gray-400">
          Discover and manage powerful workflow plugins
        </p>
      </motion.div>

      {/* Search and Filter */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search plugins..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
          >
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name} ({cat.count})
              </option>
            ))}
          </select>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Plugins', value: plugins?.data?.length || 0, icon: Puzzle, color: 'blue' },
          { label: 'Enabled', value: plugins?.data?.filter((p) => p.enabled).length || 0, icon: CheckCircle, color: 'green' },
          { label: 'Categories', value: 7, icon: Code, color: 'purple' },
          { label: 'Total Downloads', value: '11.5K', icon: Zap, color: 'yellow' },
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

      {/* Plugin Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          <>
            <CardSkeleton />
            <CardSkeleton />
            <CardSkeleton />
          </>
        ) : (
          filteredPlugins?.map((plugin, index: number) => {
            const Icon = pluginIcons[plugin.name] || Puzzle
            
            return (
              <motion.div
                key={plugin.name}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.02, y: -5 }}
                className="card cursor-pointer group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="p-3 rounded-xl bg-blue-500/20">
                    <Icon className="w-6 h-6 text-blue-400" />
                  </div>
                  <CheckCircle className="w-5 h-5 text-green-400" />
                </div>
                
                <h3 className="text-lg font-semibold mb-2 group-hover:text-blue-400 transition-colors">
                  {plugin.name.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                </h3>
                
                <p className="text-sm text-gray-400 mb-4">
                  {plugin.description}
                </p>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">v{plugin.version}</span>
                  <div className="flex items-center space-x-4">
                    <span className="text-gray-500">{plugin.downloads} downloads</span>
                    <span className="text-yellow-400">★ {plugin.rating}</span>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-gray-800">
                  <button className="w-full btn-primary py-2">
                    View Details
                  </button>
                </div>
              </motion.div>
            )
          })
        )}
      </div>
    </div>
  )
}

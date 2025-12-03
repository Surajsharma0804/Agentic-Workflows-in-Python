import { motion } from 'framer-motion'
import { Info, Zap, Github, Globe, Mail, Heart } from 'lucide-react'

export default function About() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">About</span>
        </h1>
        <p className="text-xl text-gray-400">
          Learn more about Agentic Workflows
        </p>
      </motion.div>

      {/* Hero Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="card-gradient text-center py-12"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="inline-block mb-6"
        >
          <Zap className="w-20 h-20 text-blue-400" />
        </motion.div>
        
        <h2 className="text-3xl font-bold mb-4">Agentic Workflows</h2>
        <p className="text-xl text-gray-400 mb-2">Version 1.0.0</p>
        <p className="text-gray-500">Elite AI-Powered Workflow Automation Platform</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Features */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h3 className="text-xl font-semibold mb-4">Key Features</h3>
          <ul className="space-y-3">
            {[
              'AI-powered workflow automation',
              'Visual DAG execution graphs',
              'Real-time monitoring & alerts',
              '9+ production-ready plugins',
              'Advanced retry & error handling',
              'Comprehensive audit logging',
              'RESTful API with OpenAPI docs',
              'Docker & Kubernetes ready',
            ].map((feature, index) => (
              <motion.li
                key={feature}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.05 }}
                className="flex items-center space-x-3"
              >
                <div className="w-2 h-2 bg-blue-400 rounded-full" />
                <span className="text-gray-300">{feature}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h3 className="text-xl font-semibold mb-4">Technology Stack</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-400 mb-2">Backend</p>
              <div className="flex flex-wrap gap-2">
                {['Python 3.10+', 'FastAPI', 'Celery', 'PostgreSQL', 'Redis'].map((tech) => (
                  <span key={tech} className="badge badge-primary">{tech}</span>
                ))}
              </div>
            </div>
            
            <div>
              <p className="text-sm text-gray-400 mb-2">Frontend</p>
              <div className="flex flex-wrap gap-2">
                {['React 18', 'TypeScript', 'Tailwind CSS', 'Framer Motion', 'Vite'].map((tech) => (
                  <span key={tech} className="badge badge-success">{tech}</span>
                ))}
              </div>
            </div>
            
            <div>
              <p className="text-sm text-gray-400 mb-2">DevOps</p>
              <div className="flex flex-wrap gap-2">
                {['Docker', 'Kubernetes', 'GitHub Actions', 'Prometheus'].map((tech) => (
                  <span key={tech} className="badge badge-info">{tech}</span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Python Files', value: '80+', icon: Info },
          { label: 'React Components', value: '15+', icon: Zap },
          { label: 'API Endpoints', value: '50+', icon: Globe },
          { label: 'Plugins', value: '9', icon: Heart },
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + index * 0.1 }}
            className="card text-center"
          >
            <stat.icon className="w-8 h-8 text-blue-400 mx-auto mb-2" />
            <p className="text-3xl font-bold mb-1">{stat.value}</p>
            <p className="text-sm text-gray-400">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Links */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4">Resources</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="flex items-center space-x-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors">
            <Github className="w-6 h-6 text-gray-400" />
            <div>
              <p className="font-medium">GitHub</p>
              <p className="text-sm text-gray-400">View source code</p>
            </div>
          </a>
          
          <a href="http://localhost:8000/api/docs" target="_blank" rel="noopener noreferrer" className="flex items-center space-x-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors">
            <Globe className="w-6 h-6 text-gray-400" />
            <div>
              <p className="font-medium">API Documentation</p>
              <p className="text-sm text-gray-400">Explore API endpoints</p>
            </div>
          </a>
          
          <a href="mailto:support@agentic.ai" className="flex items-center space-x-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors">
            <Mail className="w-6 h-6 text-gray-400" />
            <div>
              <p className="font-medium">Support</p>
              <p className="text-sm text-gray-400">Get help</p>
            </div>
          </a>
        </div>
      </motion.div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="text-center text-gray-500 text-sm"
      >
        <p>Built with ❤️ using modern web technologies</p>
        <p className="mt-2">© 2025 Agentic Workflows. All rights reserved.</p>
      </motion.div>
    </div>
  )
}

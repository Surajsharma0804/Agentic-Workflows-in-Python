import { useState } from 'react'
import { motion } from 'framer-motion'
import { Save, Key, Bell, Database } from 'lucide-react'
import { useAlert } from '../hooks'

export default function Settings() {
  const { showSuccess } = useAlert()
  const [settings, setSettings] = useState({
    apiKey: '••••••••••••••••',
    notifications: true,
    autoRetry: true,
    maxRetries: 3,
    timeout: 30,
    logLevel: 'info',
  })

  const handleSave = () => {
    showSuccess('Settings saved successfully!')
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">Settings</span>
        </h1>
        <p className="text-xl text-gray-400">
          Configure your workflow automation platform
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* API Configuration */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Key className="w-6 h-6 text-blue-400" />
            <h3 className="text-lg font-semibold">API Configuration</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">API Key</label>
              <input
                type="password"
                value={settings.apiKey}
                onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
                className="w-full px-4 py-2 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
            </div>
            
            <div>
              <label className="block text-sm text-gray-400 mb-2">Timeout (seconds)</label>
              <input
                type="number"
                value={settings.timeout}
                onChange={(e) => setSettings({ ...settings, timeout: parseInt(e.target.value) })}
                className="w-full px-4 py-2 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
            </div>
          </div>
        </motion.div>

        {/* Notifications */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Bell className="w-6 h-6 text-green-400" />
            <h3 className="text-lg font-semibold">Notifications</h3>
          </div>
          
          <div className="space-y-4">
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-sm text-gray-400">Enable Notifications</span>
              <input
                type="checkbox"
                checked={settings.notifications}
                onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
                className="w-5 h-5 rounded bg-gray-950 border-gray-800"
              />
            </label>
            
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-sm text-gray-400">Auto Retry Failed Tasks</span>
              <input
                type="checkbox"
                checked={settings.autoRetry}
                onChange={(e) => setSettings({ ...settings, autoRetry: e.target.checked })}
                className="w-5 h-5 rounded bg-gray-950 border-gray-800"
              />
            </label>
            
            <div>
              <label className="block text-sm text-gray-400 mb-2">Max Retries</label>
              <input
                type="number"
                value={settings.maxRetries}
                onChange={(e) => setSettings({ ...settings, maxRetries: parseInt(e.target.value) })}
                className="w-full px-4 py-2 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
            </div>
          </div>
        </motion.div>

        {/* System */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Database className="w-6 h-6 text-purple-400" />
            <h3 className="text-lg font-semibold">System</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Log Level</label>
              <select
                value={settings.logLevel}
                onChange={(e) => setSettings({ ...settings, logLevel: e.target.value })}
                className="w-full px-4 py-2 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
              >
                <option value="debug">Debug</option>
                <option value="info">Info</option>
                <option value="warning">Warning</option>
                <option value="error">Error</option>
              </select>
            </div>
            
            <button className="w-full btn-secondary">
              Clear Cache
            </button>
            
            <button className="w-full btn-secondary text-red-400 border-red-500/30 hover:bg-red-500/10">
              Reset to Defaults
            </button>
          </div>
        </motion.div>
      </div>

      {/* Save Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="flex justify-end"
      >
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSave}
          className="btn-neon flex items-center space-x-2 px-8"
        >
          <Save className="w-5 h-5" />
          <span>Save Settings</span>
        </motion.button>
      </motion.div>
    </div>
  )
}

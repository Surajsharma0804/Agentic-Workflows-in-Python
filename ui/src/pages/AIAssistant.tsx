import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, Send, Sparkles, Loader2, User } from 'lucide-react'
import { useAlert } from '../contexts/AlertContext'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function AIAssistant() {
  const { showError } = useAlert()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI workflow assistant. I can help you create workflows, debug issues, and optimize your automation. How can I assist you today?',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) {
      showError('Please enter a message')
      return
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      try {
        const responses = [
          'I can help you create a workflow for that! Here\'s a suggested YAML specification...',
          'That\'s a great question! Let me explain how that works in our system...',
          'I\'ve analyzed your workflow and found a few optimization opportunities...',
          'Here\'s a step-by-step guide to accomplish that task...',
        ]

        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: responses[Math.floor(Math.random() * responses.length)],
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, aiMessage])
        setIsLoading(false)
      } catch (error) {
        showError('Failed to get AI response. Please try again.')
        setIsLoading(false)
      }
    }, 1500)
  }

  const suggestions = [
    'Create a file organization workflow',
    'How do I handle errors in workflows?',
    'Optimize my data pipeline',
    'Explain workflow dependencies',
  ]

  return (
    <div className="space-y-6 h-[calc(100vh-12rem)]">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">
          <span className="glow-text">AI Assistant</span>
        </h1>
        <p className="text-xl text-gray-400">
          Get intelligent help with your workflows
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-full">
        {/* Chat Area */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-3 card flex flex-col h-full"
        >
          {/* Messages */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 custom-scrollbar">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex items-start space-x-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`p-2 rounded-full ${message.role === 'user' ? 'bg-blue-500/20' : 'bg-purple-500/20'}`}>
                      {message.role === 'user' ? (
                        <User className="w-5 h-5 text-blue-400" />
                      ) : (
                        <Bot className="w-5 h-5 text-purple-400" />
                      )}
                    </div>
                    
                    <div className={`p-4 rounded-xl ${message.role === 'user' ? 'bg-blue-500/10 border border-blue-500/30' : 'bg-gray-800/50 border border-gray-700'}`}>
                      <p className="text-sm text-gray-300">{message.content}</p>
                      <p className="text-xs text-gray-500 mt-2">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-start space-x-3"
              >
                <div className="p-2 rounded-full bg-purple-500/20">
                  <Bot className="w-5 h-5 text-purple-400" />
                </div>
                <div className="p-4 rounded-xl bg-gray-800/50 border border-gray-700">
                  <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
                </div>
              </motion.div>
            )}
          </div>

          {/* Input */}
          <div className="flex items-center space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask me anything about workflows..."
              className="flex-1 px-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="btn-neon px-6 py-3"
            >
              <Send className="w-5 h-5" />
            </motion.button>
          </div>
        </motion.div>

        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-6"
        >
          {/* Quick Actions */}
          <div className="card">
            <div className="flex items-center space-x-2 mb-4">
              <Sparkles className="w-5 h-5 text-yellow-400" />
              <h3 className="font-semibold">Suggestions</h3>
            </div>
            <div className="space-y-2">
              {suggestions.map((suggestion, index) => (
                <motion.button
                  key={suggestion}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setInput(suggestion)}
                  className="w-full text-left p-3 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors text-sm"
                >
                  {suggestion}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="card">
            <h3 className="font-semibold mb-4">Session Stats</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Messages</span>
                <span className="font-semibold">{messages.length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Workflows Created</span>
                <span className="font-semibold">0</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Issues Resolved</span>
                <span className="font-semibold">0</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Mail, ArrowLeft, Zap, Loader2, CheckCircle } from 'lucide-react'
import { useAlert } from '../contexts/AlertContext'

export default function ForgotPassword() {
  const { showSuccess, showError } = useAlert()
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [emailSent, setEmailSent] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })

      const data = await response.json()

      if (response.ok) {
        setEmailSent(true)
        showSuccess('Password reset email sent! Check your inbox.')
      } else {
        showError(data.detail || 'Failed to send reset email')
      }
    } catch (error) {
      showError('Network error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-4">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md relative z-10"
      >
        {/* Logo */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4 shadow-lg shadow-blue-500/50">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold glow-text mb-2">Reset Password</h1>
          <p className="text-gray-400">
            {emailSent ? 'Check your email' : 'Enter your email to reset your password'}
          </p>
        </motion.div>

        {/* Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="glass rounded-2xl p-8 shadow-2xl"
        >
          {!emailSent ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-gray-950 border border-gray-800 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={isLoading}
                className="w-full btn-neon py-3 flex items-center justify-center space-x-2"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <span>Send Reset Link</span>
                )}
              </motion.button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-8"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', duration: 0.5 }}
                className="inline-flex items-center justify-center w-16 h-16 bg-green-500/20 rounded-full mb-4"
              >
                <CheckCircle className="w-8 h-8 text-green-400" />
              </motion.div>
              
              <h3 className="text-xl font-semibold mb-2">Email Sent!</h3>
              <p className="text-gray-400 mb-6">
                We've sent a password reset link to <span className="text-white font-medium">{email}</span>
              </p>
              
              <div className="space-y-3 text-sm text-gray-400">
                <p>• Check your inbox and spam folder</p>
                <p>• The link will expire in 1 hour</p>
                <p>• Click the link to reset your password</p>
              </div>

              <button
                onClick={() => setEmailSent(false)}
                className="mt-6 text-blue-400 hover:text-blue-300 text-sm"
              >
                Didn't receive the email? Resend
              </button>
            </motion.div>
          )}

          {/* Back to Login */}
          <div className="mt-6">
            <Link
              to="/login"
              className="flex items-center justify-center space-x-2 text-sm text-gray-400 hover:text-gray-300 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to login</span>
            </Link>
          </div>
        </motion.div>

        {/* Help Text */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center text-sm text-gray-500 mt-8"
        >
          Need help?{' '}
          <a href="mailto:support@agentic.ai" className="text-gray-400 hover:text-gray-300">
            Contact support
          </a>
        </motion.p>
      </motion.div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Lock, ArrowLeft, Zap, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { useAlert } from '../contexts/AlertContext'
import AnimatedInput from '../components/ui/AnimatedInput'

export default function ResetPassword() {
  const { showSuccess, showError } = useAlert()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isVerifying, setIsVerifying] = useState(true)
  const [tokenValid, setTokenValid] = useState(false)
  const [tokenError, setTokenError] = useState('')
  const [resetSuccess, setResetSuccess] = useState(false)

  useEffect(() => {
    if (!token) {
      setTokenError('No reset token provided')
      setIsVerifying(false)
      return
    }

    // Verify token on mount
    fetch(`/api/auth/verify-reset-token/${token}`)
      .then(res => res.json())
      .then(data => {
        if (data.valid) {
          setTokenValid(true)
        } else {
          setTokenError(data.message || 'Invalid or expired token')
        }
      })
      .catch(() => {
        setTokenError('Failed to verify reset token')
      })
      .finally(() => {
        setIsVerifying(false)
      })
  }, [token])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      showError('Passwords do not match')
      return
    }

    if (password.length < 8) {
      showError('Password must be at least 8 characters long')
      return
    }

    setIsLoading(true)

    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          new_password: password
        })
      })

      const data = await response.json()

      if (response.ok) {
        setResetSuccess(true)
        showSuccess('Password reset successfully!')
        setTimeout(() => navigate('/login'), 3000)
      } else {
        showError(data.detail || 'Failed to reset password')
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
            {resetSuccess ? 'Password updated!' : 'Create a new password for your account'}
          </p>
        </motion.div>

        {/* Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="glass rounded-2xl p-8 shadow-2xl"
        >
          {isVerifying ? (
            <div className="text-center py-8">
              <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-400" />
              <p className="text-gray-400">Verifying reset token...</p>
            </div>
          ) : !tokenValid ? (
            <div className="text-center py-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', duration: 0.5 }}
                className="inline-flex items-center justify-center w-16 h-16 bg-red-500/20 rounded-full mb-4"
              >
                <AlertCircle className="w-8 h-8 text-red-400" />
              </motion.div>
              
              <h3 className="text-xl font-semibold mb-2">Invalid Token</h3>
              <p className="text-gray-400 mb-6">{tokenError}</p>
              
              <Link
                to="/forgot-password"
                className="text-blue-400 hover:text-blue-300 text-sm"
              >
                Request a new reset link
              </Link>
            </div>
          ) : resetSuccess ? (
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
              
              <h3 className="text-xl font-semibold mb-2">Password Reset!</h3>
              <p className="text-gray-400 mb-6">
                Your password has been successfully reset.
              </p>
              
              <p className="text-sm text-gray-500">
                Redirecting to login page...
              </p>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <AnimatedInput
                label="New Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter new password"
                icon={Lock}
                required
                minLength={8}
              />

              <AnimatedInput
                label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                icon={Lock}
                required
                minLength={8}
              />

              <div className="text-sm text-gray-400 space-y-1">
                <p>Password requirements:</p>
                <ul className="list-disc list-inside space-y-1 text-gray-500">
                  <li className={password.length >= 8 ? 'text-green-400' : ''}>
                    At least 8 characters
                  </li>
                  <li className={password === confirmPassword && password ? 'text-green-400' : ''}>
                    Passwords match
                  </li>
                </ul>
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
                  <span>Reset Password</span>
                )}
              </motion.button>
            </form>
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

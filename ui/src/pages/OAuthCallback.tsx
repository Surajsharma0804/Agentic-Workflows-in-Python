import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Loader2, AlertCircle } from 'lucide-react'
import { useAuth, useAlert } from '../hooks'

export default function OAuthCallback() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { setToken } = useAuth()
  const { showSuccess, showError } = useAlert()

  useEffect(() => {
    const token = searchParams.get('token')
    const provider = searchParams.get('provider')
    const error = searchParams.get('error')

    if (error) {
      showError(`Authentication failed: ${error}`)
      setTimeout(() => navigate('/login'), 2000)
      return
    }

    if (token) {
      // First store the token
      localStorage.setItem('auth_token', token)
      
      // Then fetch and set user data
      setToken(token)
        .then(() => {
          showSuccess(`Successfully logged in with ${provider}!`)
          // Navigate after a short delay to ensure state is updated
          setTimeout(() => navigate('/'), 500)
        })
        .catch((err) => {
          console.error('OAuth setToken error:', err)
          // Clear invalid token
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
          showError('Authentication failed. Please try again.')
          setTimeout(() => navigate('/login'), 2000)
        })
    } else {
      showError('No authentication token received')
      setTimeout(() => navigate('/login'), 2000)
    }
  }, [searchParams, navigate, setToken, showSuccess, showError])

  const error = searchParams.get('error')

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="relative z-10 text-center"
      >
        {error ? (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', duration: 0.5 }}
              className="inline-flex items-center justify-center w-20 h-20 bg-red-500/20 rounded-full mb-6"
            >
              <AlertCircle className="w-10 h-10 text-red-400" />
            </motion.div>
            <h2 className="text-2xl font-bold text-white mb-2">Authentication Failed</h2>
            <p className="text-gray-400">Redirecting to login...</p>
          </>
        ) : (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="inline-flex items-center justify-center w-20 h-20 bg-blue-500/20 rounded-full mb-6"
            >
              <Loader2 className="w-10 h-10 text-blue-400" />
            </motion.div>
            <h2 className="text-2xl font-bold text-white mb-2">Completing Sign In</h2>
            <p className="text-gray-400">Please wait...</p>
          </>
        )}
      </motion.div>
    </div>
  )
}

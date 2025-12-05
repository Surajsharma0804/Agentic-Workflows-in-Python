import { useState, useEffect } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, Zap, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useAlert } from '../contexts/AlertContext'
import AnimatedInput from '../components/ui/AnimatedInput'
import Button from '../components/ui/Button'
import AnimatedLoginHero from '../components/ui/AnimatedLoginHero'

export default function Login() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { login, loginWithGoogle, loginWithApple, loginWithGithub } = useAuth()
  const { showSuccess, showError } = useAlert()
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [loginSuccess, setLoginSuccess] = useState(false)
  const [loginError, setLoginError] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  })
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({})

  // Handle OAuth errors from URL
  useEffect(() => {
    const error = searchParams.get('error')
    const provider = searchParams.get('provider')
    
    if (error === 'oauth_not_configured' && provider) {
      showError(`${provider.charAt(0).toUpperCase() + provider.slice(1)} OAuth is not configured. Please use email/password login or contact the administrator to set up OAuth credentials.`)
      // Clear the error from URL
      searchParams.delete('error')
      searchParams.delete('provider')
      navigate({ search: searchParams.toString() }, { replace: true })
    }
  }, [searchParams, showError, navigate])

  const validateForm = () => {
    const newErrors: { email?: string; password?: string } = {}
    
    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      setLoginError(true)
      setTimeout(() => setLoginError(false), 500)
      return
    }
    
    setIsLoading(true)
    setLoginError(false)

    try {
      await login(formData.email, formData.password, formData.rememberMe)
      setLoginSuccess(true)
      showSuccess('Welcome back! Login successful.')
      
      // Delay navigation for success animation
      setTimeout(() => {
        navigate('/')
      }, 1000)
    } catch (error: any) {
      setLoginError(true)
      showError(error.message || 'Login failed. Please check your credentials.')
      setTimeout(() => setLoginError(false), 500)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSocialLogin = async (provider: 'google' | 'apple' | 'github') => {
    try {
      // Check if OAuth is configured by making a request
      const baseUrl = window.location.origin
      const response = await fetch(`${baseUrl}/api/auth/${provider}/login`, {
        method: 'GET',
        redirect: 'manual' // Don't follow redirects
      })
      
      // If we get a 501, OAuth is not configured
      if (response.status === 501) {
        showError(`${provider.charAt(0).toUpperCase() + provider.slice(1)} login is not configured yet. Please use email/password login or contact the administrator.`)
        return
      }
      
      // Otherwise, redirect to OAuth
      window.location.href = `${baseUrl}/api/auth/${provider}/login`
    } catch (error) {
      showError(`Failed to initiate ${provider} login. Please try again or use email/password login.`)
    }
  }

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-bg relative overflow-hidden">
      {/* Animated Gradient Mesh Background */}
      <div className="fixed inset-0 z-0" style={{ background: 'var(--gradient-mesh)' }} />
      
      {/* Skip to content link for accessibility */}
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>

      {/* Left Side - Hero (Hidden on mobile, visible on lg+) */}
      <div className="hidden lg:block lg:w-1/2 xl:w-3/5 relative z-10">
        <AnimatedLoginHero />
      </div>

      {/* Right Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8 relative z-10" id="main-content">
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Mobile Hero Banner */}
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="lg:hidden mb-8 text-center"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="inline-flex items-center justify-center w-16 h-16 gradient-primary rounded-2xl mb-4 shadow-glow"
            >
              <Zap className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-3xl font-bold mb-2 text-text-primary">Welcome Back</h1>
            <p className="text-text-secondary">Sign in to your account</p>
          </motion.div>

          {/* Logo for Desktop */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="hidden lg:block text-center mb-10"
          >
            <motion.div 
              className="inline-flex items-center justify-center w-20 h-20 gradient-primary rounded-3xl mb-6 shadow-glow"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <Zap className="w-10 h-10 text-white" />
            </motion.div>
            <h1 className="text-4xl font-bold text-text-primary mb-3">Welcome Back</h1>
            <p className="text-text-secondary text-lg">Sign in to your account</p>
          </motion.div>

          {/* Login Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ 
              opacity: 1, 
              scale: 1,
              x: loginError ? [-10, 10, -10, 10, 0] : 0
            }}
            transition={{ 
              opacity: { duration: 0.5, delay: 0.2 },
              scale: { duration: 0.5, delay: 0.2 },
              x: { duration: 0.4 }
            }}
            className="card-glass p-6 sm:p-8 hover-lift relative"
          >
            {/* Success Animation Overlay */}
            <AnimatePresence>
              {loginSuccess && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  className="absolute inset-0 flex items-center justify-center bg-surface/95 backdrop-blur-sm rounded-2xl z-50"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: [0, 1.2, 1] }}
                    transition={{ duration: 0.5 }}
                    className="text-center"
                  >
                    <CheckCircle className="w-20 h-20 text-success-500 mx-auto mb-4" />
                    <p className="text-xl font-semibold text-text-primary">Login Successful!</p>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>

            <form onSubmit={handleSubmit} className="space-y-5"
              role="form"
              aria-label="Login form"
            >
              {/* Email */}
              <AnimatedInput
                type="email"
                label="Email Address"
                value={formData.email}
                onChange={(e) => {
                  setFormData({ ...formData, email: e.target.value })
                  if (errors.email) setErrors({ ...errors, email: undefined })
                }}
                error={errors.email}
                leftIcon={<Mail className="w-5 h-5" />}
                autoComplete="email"
                aria-label="Email address"
                aria-required="true"
                aria-invalid={!!errors.email}
              />

              {/* Password */}
              <AnimatedInput
                type={showPassword ? 'text' : 'password'}
                label="Password"
                value={formData.password}
                onChange={(e) => {
                  setFormData({ ...formData, password: e.target.value })
                  if (errors.password) setErrors({ ...errors, password: undefined })
                }}
                error={errors.password}
                leftIcon={<Lock className="w-5 h-5" />}
                rightIcon={
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-text-muted hover:text-text-primary transition-colors"
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                }
                autoComplete="current-password"
                aria-label="Password"
                aria-required="true"
                aria-invalid={!!errors.password}
              />

              {/* Remember Me & Forgot Password */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <label className="flex items-center cursor-pointer group">
                  <div className="relative">
                    <input
                      type="checkbox"
                      checked={formData.rememberMe}
                      onChange={(e) => setFormData({ ...formData, rememberMe: e.target.checked })}
                      className="w-5 h-5 rounded-md glass border-2 border-primary/50 text-primary focus:ring-2 focus:ring-primary/30 transition-all cursor-pointer checked:bg-gradient-to-br checked:from-primary checked:to-accent checked:border-primary"
                      aria-label="Remember me"
                    />
                    {formData.rememberMe && (
                      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <span className="ml-3 text-sm font-medium text-text-secondary group-hover:text-text-primary transition-colors">
                    Remember me
                  </span>
                </label>
                <Link
                  to="/forgot-password"
                  className="text-sm text-primary-400 hover:text-primary-300 transition-colors font-semibold"
                >
                  Forgot password?
                </Link>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                variant="neon"
                size="lg"
                isLoading={isLoading}
                className="w-full btn-gradient btn-glow"
                aria-label="Sign in to your account"
              >
                {!isLoading && 'Sign In'}
              </Button>
          </form>

            {/* Divider with Gradient */}
            <div className="relative my-8">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />
              </div>
              <div className="relative flex justify-center">
                <span className="px-6 py-2 bg-surface/90 backdrop-blur-sm text-text-secondary text-sm font-medium border border-border/30 rounded-full">
                  Or continue with
                </span>
              </div>
            </div>

            {/* Social Login Buttons with Premium Effects */}
            <div className="grid grid-cols-3 gap-3"
              role="group"
              aria-label="Social login options"
            >
              <motion.button
                whileHover={{ scale: 1.03, y: -2 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => handleSocialLogin('google')}
                disabled={isLoading}
                className="group relative flex items-center justify-center p-4 glass border border-border/50 rounded-xl hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all min-h-[60px]"
                aria-label="Sign in with Google"
                title="Sign in with Google"
              >
                <svg 
                  className="w-6 h-6" 
                  viewBox="0 0 24 24"
                >
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.03, y: -2 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => handleSocialLogin('apple')}
                disabled={isLoading}
                className="group relative flex items-center justify-center p-4 glass border border-border/50 rounded-xl hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all min-h-[60px]"
                aria-label="Sign in with Apple"
                title="Sign in with Apple"
              >
                <svg 
                  className="w-6 h-6 text-text-primary" 
                  viewBox="0 0 24 24" 
                  fill="currentColor"
                >
                  <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/>
                </svg>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.03, y: -2 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => handleSocialLogin('github')}
                disabled={isLoading}
                className="group relative flex items-center justify-center p-4 glass border border-border/50 rounded-xl hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all min-h-[60px]"
                aria-label="Sign in with GitHub"
                title="Sign in with GitHub"
              >
                <svg 
                  className="w-6 h-6 text-text-primary" 
                  viewBox="0 0 24 24" 
                  fill="currentColor"
                >
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </motion.button>
            </div>

            {/* Sign Up Link */}
            <div className="mt-6 text-center">
              <p className="text-sm text-text-secondary">
                Don't have an account?{' '}
                <Link
                  to="/register"
                  className="text-primary-400 hover:text-primary-300 font-bold transition-colors"
                >
                  Sign up
                </Link>
              </p>
            </div>
          </motion.div>

          {/* Footer */}
          <p className="text-center text-xs sm:text-sm text-text-muted mt-6 sm:mt-8 px-4">
            By signing in, you agree to our{' '}
            <Link 
              to="/terms-of-service" 
              className="text-accent-400 hover:text-accent-300 transition-colors font-semibold underline decoration-accent-400/30 hover:decoration-accent-300"
            >
              Terms of Service
            </Link>
            {' '}and{' '}
            <Link 
              to="/privacy-policy" 
              className="text-accent-400 hover:text-accent-300 transition-colors font-semibold underline decoration-accent-400/30 hover:decoration-accent-300"
            >
              Privacy Policy
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  )
}

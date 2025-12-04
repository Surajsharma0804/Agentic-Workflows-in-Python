import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, Zap, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useAlert } from '../contexts/AlertContext'
import AnimatedInput from '../components/ui/AnimatedInput'
import Button from '../components/ui/Button'
import AnimatedLoginHero from '../components/ui/AnimatedLoginHero'

export default function Login() {
  const navigate = useNavigate()
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
    setIsLoading(true)
    try {
      if (provider === 'google') await loginWithGoogle()
      else if (provider === 'apple') await loginWithApple()
      else await loginWithGithub()
      
      showSuccess(`Successfully logged in with ${provider}!`)
      navigate('/')
    } catch (error: any) {
      showError(error.message || `${provider} login failed. Please try again.`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-bg">
      {/* Skip to content link for accessibility */}
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>

      {/* Left Side - Hero (Hidden on mobile, visible on lg+) */}
      <div className="hidden lg:block lg:w-1/2 xl:w-3/5">
        <AnimatedLoginHero />
      </div>

      {/* Right Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8" id="main-content">
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Mobile Hero Banner */}
          <div className="lg:hidden mb-8 p-6 bg-gradient-to-br from-primary-600 to-accent-600 rounded-2xl text-white text-center">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl mb-4"
            >
              <Zap className="w-8 h-8" />
            </motion.div>
            <h1 className="text-2xl font-bold mb-2">Agentic Workflows</h1>
            <p className="text-white/80 text-sm">AI-Powered Automation Platform</p>
          </div>

          {/* Logo for Desktop */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="hidden lg:block text-center mb-8"
          >
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-2xl mb-4 shadow-glow">
              <Zap className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-text-primary mb-2">Welcome Back</h1>
            <p className="text-text-secondary">Sign in to continue to your account</p>
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
            className="card p-6 sm:p-8"
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
                placeholder="you@example.com"
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
                placeholder="••••••••"
                autoComplete="current-password"
                aria-label="Password"
                aria-required="true"
                aria-invalid={!!errors.password}
              />

              {/* Remember Me & Forgot Password */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <label className="flex items-center cursor-pointer group">
                  <input
                    type="checkbox"
                    checked={formData.rememberMe}
                    onChange={(e) => setFormData({ ...formData, rememberMe: e.target.checked })}
                    className="w-4 h-4 rounded bg-surface border-2 border-border text-primary focus:ring-2 focus:ring-primary/20 transition-colors"
                    aria-label="Remember me"
                  />
                  <span className="ml-2 text-sm text-text-secondary group-hover:text-text-primary transition-colors">
                    Remember me
                  </span>
                </label>
                <Link
                  to="/forgot-password"
                  className="text-sm text-primary hover:text-primary-hover transition-colors font-medium"
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
                className="w-full"
                aria-label="Sign in to your account"
              >
                {!isLoading && 'Sign In'}
              </Button>
          </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t-2 border-border" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-surface text-text-muted font-medium">Or continue with</span>
              </div>
            </div>

            {/* Social Login Buttons */}
            <div className="grid grid-cols-3 gap-2 sm:gap-3"
              role="group"
              aria-label="Social login options"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleSocialLogin('google')}
                disabled={isLoading}
                className="flex items-center justify-center p-3 sm:p-4 bg-surface border-2 border-border rounded-xl hover:border-primary hover:bg-bg-secondary transition-all min-h-[44px]"
                aria-label="Sign in with Google"
              >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleSocialLogin('apple')}
                disabled={isLoading}
                className="flex items-center justify-center p-3 sm:p-4 bg-surface border-2 border-border rounded-xl hover:border-primary hover:bg-bg-secondary transition-all min-h-[44px]"
                aria-label="Sign in with Apple"
              >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/>
              </svg>
            </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleSocialLogin('github')}
                disabled={isLoading}
                className="flex items-center justify-center p-3 sm:p-4 bg-surface border-2 border-border rounded-xl hover:border-primary hover:bg-bg-secondary transition-all min-h-[44px]"
                aria-label="Sign in with GitHub"
              >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
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
                  className="text-primary hover:text-primary-hover font-semibold transition-colors"
                >
                  Sign up
                </Link>
              </p>
            </div>
          </motion.div>

          {/* Footer */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-center text-xs sm:text-sm text-text-muted mt-6 sm:mt-8 px-4"
          >
            By signing in, you agree to our{' '}
            <a href="#" className="text-text-secondary hover:text-primary transition-colors">
              Terms of Service
            </a>
            {' '}and{' '}
            <a href="#" className="text-text-secondary hover:text-primary transition-colors">
              Privacy Policy
            </a>
          </motion.p>
        </motion.div>
      </div>
    </div>
  )
}

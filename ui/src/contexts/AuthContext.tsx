import { createContext, useState, useEffect, ReactNode } from 'react'

export interface User {
  id: string
  name: string
  email: string
  company?: string
  avatar?: string
  role: string
}

export interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>
  register: (name: string, email: string, password: string, company?: string) => Promise<void>
  logout: () => void
  setToken: (token: string) => Promise<void>
  loginWithGoogle: () => Promise<void>
  loginWithApple: () => Promise<void>
  loginWithGithub: () => Promise<void>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      // Check for stored auth token
      const token = localStorage.getItem('auth_token')
      const storedUser = localStorage.getItem('user')
      
      if (token && storedUser) {
        try {
          // Validate token is still valid by fetching current user
          const response = await fetch('/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          })
          
          if (response.ok) {
            const userData = await response.json()
            localStorage.setItem('user', JSON.stringify(userData))
            setUser(userData)
          } else {
            // Token is invalid, clear storage
            localStorage.removeItem('auth_token')
            localStorage.removeItem('user')
            setUser(null)
          }
        } catch (error) {
          // Network error or invalid token
          console.error('Auth validation error:', error)
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
          setUser(null)
        }
      }
      
      setIsLoading(false)
    }
    
    initAuth()
  }, [])

  const login = async (email: string, password: string, rememberMe = false) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          remember_me: rememberMe,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data = await response.json()
      const { access_token, user } = data

      const storage = rememberMe ? localStorage : sessionStorage
      storage.setItem('auth_token', access_token)
      storage.setItem('user', JSON.stringify(user))

      setUser(user)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed. Please check your credentials.'
      throw new Error(errorMessage)
    }
  }

  const register = async (name: string, email: string, password: string, company?: string) => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
          company,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Registration failed')
      }

      const data = await response.json()
      const { access_token, user } = data

      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('user', JSON.stringify(user))

      setUser(user)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Registration failed. Please try again.'
      throw new Error(errorMessage)
    }
  }

  const setToken = async (token: string) => {
    try {
      // Fetch user info with token
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Failed to fetch user info:', response.status, errorText)
        throw new Error('Failed to fetch user info')
      }

      const userData = await response.json()
      
      // Store both token and user data
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      // Update state
      setUser(userData)
      
      return userData
    } catch (error) {
      console.error('setToken error:', error)
      // Clean up on error
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      setUser(null)
      throw error
    }
  }

  const loginWithGoogle = async () => {
    // OAuth handled by backend redirect
    throw new Error('Use handleSocialLogin instead')
  }

  const loginWithApple = async () => {
    // OAuth handled by backend redirect
    throw new Error('Use handleSocialLogin instead')
  }

  const loginWithGithub = async () => {
    // OAuth handled by backend redirect
    throw new Error('Use handleSocialLogin instead')
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    sessionStorage.removeItem('auth_token')
    sessionStorage.removeItem('user')
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        setToken,
        loginWithGoogle,
        loginWithApple,
        loginWithGithub,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

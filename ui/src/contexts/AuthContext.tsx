import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'

interface User {
  id: string
  name: string
  email: string
  company?: string
  avatar?: string
  role: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>
  register: (name: string, email: string, password: string, company?: string) => Promise<void>
  logout: () => void
  loginWithGoogle: () => Promise<void>
  loginWithApple: () => Promise<void>
  loginWithGithub: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for stored auth token
    const token = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user')
    
    if (token && storedUser) {
      setUser(JSON.parse(storedUser))
    }
    
    setIsLoading(false)
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
    } catch (error: any) {
      throw new Error(error.message || 'Login failed. Please check your credentials.')
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
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed. Please try again.')
    }
  }

  const loginWithGoogle = async () => {
    // Simulate OAuth flow
    await new Promise(resolve => setTimeout(resolve, 1500))

    const mockUser: User = {
      id: 'google_' + Date.now(),
      name: 'Google User',
      email: 'user@gmail.com',
      avatar: `https://ui-avatars.com/api/?name=Google+User&background=ea4335&color=fff`,
      role: 'user',
    }

    const token = 'mock_google_token_' + Date.now()
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user', JSON.stringify(mockUser))

    setUser(mockUser)
  }

  const loginWithApple = async () => {
    // Simulate OAuth flow
    await new Promise(resolve => setTimeout(resolve, 1500))

    const mockUser: User = {
      id: 'apple_' + Date.now(),
      name: 'Apple User',
      email: 'user@icloud.com',
      avatar: `https://ui-avatars.com/api/?name=Apple+User&background=000000&color=fff`,
      role: 'user',
    }

    const token = 'mock_apple_token_' + Date.now()
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user', JSON.stringify(mockUser))

    setUser(mockUser)
  }

  const loginWithGithub = async () => {
    // Simulate OAuth flow
    await new Promise(resolve => setTimeout(resolve, 1500))

    const mockUser: User = {
      id: 'github_' + Date.now(),
      name: 'GitHub User',
      email: 'user@github.com',
      avatar: `https://ui-avatars.com/api/?name=GitHub+User&background=24292e&color=fff`,
      role: 'user',
    }

    const token = 'mock_github_token_' + Date.now()
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user', JSON.stringify(mockUser))

    setUser(mockUser)
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
        loginWithGoogle,
        loginWithApple,
        loginWithGithub,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

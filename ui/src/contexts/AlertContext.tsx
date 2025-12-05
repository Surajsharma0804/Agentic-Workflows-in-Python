import { createContext, useState, ReactNode, useCallback } from 'react'
import { AlertContainer, AlertType } from '../components/Alert'

interface Alert {
  id: string
  type: AlertType
  message: string
}

export interface AlertContextType {
  showAlert: (type: AlertType, message: string) => void
  showSuccess: (message: string) => void
  showError: (message: string) => void
  showWarning: (message: string) => void
  showInfo: (message: string) => void
}

export const AlertContext = createContext<AlertContextType | undefined>(undefined)

export function AlertProvider({ children }: { children: ReactNode }) {
  const [alerts, setAlerts] = useState<Alert[]>([])

  const showAlert = useCallback((type: AlertType, message: string) => {
    const id = Math.random().toString(36).substring(7)
    setAlerts((prev) => [...prev, { id, type, message }])
  }, [])

  const showSuccess = useCallback((message: string) => {
    showAlert('success', message)
  }, [showAlert])

  const showError = useCallback((message: string) => {
    showAlert('error', message)
  }, [showAlert])

  const showWarning = useCallback((message: string) => {
    showAlert('warning', message)
  }, [showAlert])

  const showInfo = useCallback((message: string) => {
    showAlert('info', message)
  }, [showAlert])

  const closeAlert = useCallback((id: string) => {
    setAlerts((prev) => prev.filter((alert) => alert.id !== id))
  }, [])

  return (
    <AlertContext.Provider value={{ showAlert, showSuccess, showError, showWarning, showInfo }}>
      {children}
      <AlertContainer alerts={alerts} onClose={closeAlert} />
    </AlertContext.Provider>
  )
}

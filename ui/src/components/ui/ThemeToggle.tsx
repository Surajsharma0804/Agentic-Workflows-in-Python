import { motion } from 'framer-motion'
import { Sun, Moon, Monitor } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

export default function ThemeToggle() {
  const { theme, resolvedTheme, setThemeMode } = useTheme()

  const themes = [
    { value: 'light' as const, icon: Sun, label: 'Light' },
    { value: 'dark' as const, icon: Moon, label: 'Dark' },
    { value: 'system' as const, icon: Monitor, label: 'System' },
  ]

  return (
    <div className="flex items-center gap-1 p-1 bg-surface rounded-xl border-2 border-border">
      {themes.map(({ value, icon: Icon, label }) => (
        <motion.button
          key={value}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setThemeMode(value)}
          className={`
            relative px-3 py-2 rounded-lg transition-all duration-200
            ${theme === value 
              ? 'text-text-inverse' 
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
            }
          `}
          aria-label={`Switch to ${label} theme`}
          aria-pressed={theme === value}
        >
          {theme === value && (
            <motion.div
              layoutId="theme-indicator"
              className="absolute inset-0 bg-primary rounded-lg"
              transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
            />
          )}
          <Icon className="w-4 h-4 relative z-10" />
        </motion.button>
      ))}
    </div>
  )
}

import { motion } from 'framer-motion'
import { useState, forwardRef, InputHTMLAttributes } from 'react'

interface AnimatedInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  helperText?: string
}

const AnimatedInput = forwardRef<HTMLInputElement, AnimatedInputProps>(
  (
    {
      label,
      error,
      leftIcon,
      rightIcon,
      helperText,
      className = '',
      id,
      ...props
    },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false)
    const [hasValue, setHasValue] = useState(false)
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(e.target.value.length > 0)
      props.onChange?.(e)
    }

    return (
      <div className="w-full">
        <div className="relative">
          {/* Floating Label */}
          {label && (
            <motion.label
              htmlFor={inputId}
              animate={{
                top: isFocused || hasValue ? '-0.75rem' : '50%',
                fontSize: isFocused || hasValue ? '0.75rem' : '1rem',
                translateY: isFocused || hasValue ? '0' : '-50%',
              }}
              transition={{ duration: 0.2 }}
              className={`
                absolute left-3 px-2 bg-surface pointer-events-none z-10
                transition-colors duration-200
                ${isFocused ? 'text-primary' : 'text-text-secondary'}
                ${error ? 'text-danger-500' : ''}
              `}
            >
              {label}
            </motion.label>
          )}

          {/* Left Icon */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted z-10">
              {leftIcon}
            </div>
          )}

          {/* Input */}
          <motion.input
            ref={ref}
            id={inputId}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            onChange={handleChange}
            animate={{
              borderColor: error
                ? 'var(--color-danger-500)'
                : isFocused
                ? 'var(--primary)'
                : 'var(--border)',
            }}
            transition={{ duration: 0.2 }}
            className={`
              w-full px-4 py-3 bg-surface border-2 rounded-xl
              text-text-primary placeholder-text-muted
              focus:outline-none focus:ring-2 focus:ring-primary/20
              transition-all duration-200
              ${leftIcon ? 'pl-10' : ''}
              ${rightIcon ? 'pr-10' : ''}
              ${error ? 'border-danger-500 focus:ring-danger-500/20' : ''}
              ${className}
            `}
            {...props}
          />

          {/* Right Icon */}
          {rightIcon && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-muted">
              {rightIcon}
            </div>
          )}

          {/* Focus Ring Animation */}
          {isFocused && !error && (
            <motion.div
              layoutId="input-focus-ring"
              className="absolute inset-0 rounded-xl pointer-events-none"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              style={{
                boxShadow: '0 0 0 3px rgba(99, 102, 241, 0.1)',
              }}
            />
          )}
        </div>

        {/* Helper Text or Error */}
        {(helperText || error) && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mt-1.5 text-sm ${
              error ? 'text-danger-500' : 'text-text-muted'
            }`}
          >
            {error || helperText}
          </motion.p>
        )}
      </div>
    )
  }
)

AnimatedInput.displayName = 'AnimatedInput'

export default AnimatedInput

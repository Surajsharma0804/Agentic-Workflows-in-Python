import { motion } from 'framer-motion'
import { useState, useEffect, forwardRef, InputHTMLAttributes } from 'react'

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
      value,
      ...props
    },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false)
    const [hasValue, setHasValue] = useState(!!value)
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`

    // Update hasValue when value prop changes
    useEffect(() => {
      setHasValue(!!value && String(value).length > 0)
    }, [value])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(e.target.value.length > 0)
      props.onChange?.(e)
    }

    // Don't show placeholder when label is present and not focused/filled
    const showPlaceholder = !label || isFocused || hasValue

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
                absolute ${leftIcon ? 'left-10' : 'left-3'} px-2 pointer-events-none z-10
                transition-all duration-200 font-medium
                ${isFocused || hasValue ? 'bg-gradient-to-r from-surface via-surface to-surface' : 'bg-surface'}
                ${isFocused ? 'text-primary-500' : hasValue ? 'text-primary-400' : 'text-text-muted'}
                ${error ? 'text-danger-500' : ''}
              `}
            >
              {label}
            </motion.label>
          )}

          {/* Left Icon */}
          {leftIcon && (
            <div className={`
              absolute left-3 top-1/2 transform -translate-y-1/2 z-10
              transition-colors duration-200
              ${isFocused ? 'text-primary-500' : hasValue ? 'text-primary-400' : 'text-text-muted'}
              ${error ? 'text-danger-500' : ''}
            `}>
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
                : hasValue
                ? 'var(--color-primary-400)'
                : 'var(--border)',
            }}
            transition={{ duration: 0.2 }}
            className={`
              w-full px-4 py-3 rounded-xl border-2
              text-text-primary placeholder-text-muted/60
              focus:outline-none transition-all duration-200
              ${isFocused ? 'bg-surface/80 shadow-lg shadow-primary/10' : 'bg-surface'}
              ${leftIcon ? 'pl-10' : ''}
              ${rightIcon ? 'pr-10' : ''}
              ${error ? 'border-danger-500 bg-danger-500/5' : ''}
              ${isFocused && !error ? 'ring-4 ring-primary/10' : ''}
              ${className}
            `}
            placeholder={showPlaceholder ? props.placeholder : ''}
            value={value}
            {...(props as any)}
          />

          {/* Right Icon */}
          {rightIcon && (
            <div className={`
              absolute right-3 top-1/2 transform -translate-y-1/2
              transition-colors duration-200
              ${isFocused ? 'text-primary-500' : 'text-text-muted'}
            `}>
              {rightIcon}
            </div>
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

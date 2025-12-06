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
    const inputId = id || `input-${Math.random().toString(36).substring(2, 11)}`

    // Update hasValue when value prop changes or on autofill
    useEffect(() => {
      setHasValue(!!value && String(value).length > 0)
    }, [value])

    // Detect autofill by checking if input has value after mount
    useEffect(() => {
      const checkAutofill = () => {
        const input = document.getElementById(inputId) as HTMLInputElement
        if (input && input.value) {
          setHasValue(true)
        }
      }
      
      // Check immediately and after a short delay for autofill
      checkAutofill()
      const timer = setTimeout(checkAutofill, 100)
      
      return () => clearTimeout(timer)
    }, [inputId])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(e.target.value.length > 0)
      props.onChange?.(e)
    }

    return (
      <div className="w-full">
        <div className="relative">
          {/* Floating Label with Gradient */}
          {label && (
            <motion.label
              htmlFor={inputId}
              animate={{
                top: isFocused || hasValue ? '-0.625rem' : '50%',
                fontSize: isFocused || hasValue ? '0.75rem' : '0.95rem',
                translateY: isFocused || hasValue ? '0' : '-50%',
                scale: isFocused ? 1.02 : 1,
              }}
              transition={{ duration: 0.2, type: 'spring', stiffness: 400, damping: 25 }}
              className={`
                absolute ${leftIcon ? 'left-10' : 'left-4'} px-2 pointer-events-none z-20
                transition-all duration-200 font-semibold
                ${isFocused || hasValue ? 'glass-strong rounded-md shadow-sm' : 'bg-transparent'}
                ${isFocused && !error ? 'gradient-text' : hasValue && !error ? 'text-primary-400' : 'text-text-muted'}
                ${error ? 'text-danger-500' : ''}
              `}
            >
              {label}
            </motion.label>
          )}

          {/* Left Icon with Animation */}
          {leftIcon && (
            <motion.div 
              animate={{
                scale: isFocused ? 1.1 : 1,
                rotate: isFocused ? [0, -5, 5, 0] : 0,
              }}
              transition={{ duration: 0.3 }}
              className={`
                absolute left-3 top-1/2 transform -translate-y-1/2 z-20
                transition-all duration-300
                ${isFocused && !error ? 'text-primary-500 drop-shadow-lg' : hasValue && !error ? 'text-primary-400' : 'text-text-muted'}
                ${error ? 'text-danger-500' : ''}
              `}
            >
              {leftIcon}
            </motion.div>
          )}

          {/* Input Container with Glow Effect */}
          <div className="relative">
            {/* Animated Border Glow */}
            {isFocused && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute -inset-0.5 bg-gradient-to-r from-primary via-accent to-primary rounded-xl blur-sm opacity-30 animate-pulse"
              />
            )}
            
            {/* Input */}
            <input
              ref={ref}
              id={inputId}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onChange={handleChange}
              className={`
                relative w-full px-4 py-4 rounded-xl border-2
                text-text-primary placeholder-transparent
                focus:outline-none transition-all duration-200
                font-medium text-base
                ${isFocused 
                  ? 'glass-strong border-primary shadow-xl shadow-primary/20 bg-surface/90 pt-5 pb-3' 
                  : hasValue 
                  ? 'glass border-primary/50 bg-surface/80 pt-5 pb-3' 
                  : 'glass border-border/50 bg-surface/70'
                }
                ${leftIcon ? 'pl-11' : ''}
                ${rightIcon ? 'pr-11' : ''}
                ${error ? 'border-danger-500 bg-danger-500/10 shadow-lg shadow-danger-500/20' : ''}
                ${isFocused && !error ? 'ring-4 ring-primary/20' : ''}
                hover:border-primary/70 hover:shadow-lg hover:shadow-primary/10
                ${className}
              `}
              style={{
                backdropFilter: 'blur(12px)',
                WebkitBackdropFilter: 'blur(12px)',
              }}
              placeholder={label || props.placeholder || ''}
              value={value}
              {...props}
            />
          </div>

          {/* Right Icon with Hover Effect */}
          {rightIcon && (
            <motion.div 
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className={`
                absolute right-3 top-1/2 transform -translate-y-1/2 z-20
                transition-all duration-300 cursor-pointer
                ${isFocused && !error ? 'text-primary-500' : 'text-text-muted'}
                ${error ? 'text-danger-500' : ''}
                hover:text-primary-400
              `}
            >
              {rightIcon}
            </motion.div>
          )}
        </div>

        {/* Helper Text or Error with Animation */}
        {(helperText || error) && (
          <motion.p
            initial={{ opacity: 0, y: -5, x: -5 }}
            animate={{ opacity: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, y: -5 }}
            transition={{ duration: 0.3 }}
            className={`mt-2 text-sm font-medium flex items-center gap-1 ${
              error ? 'text-danger-500' : 'text-text-muted'
            }`}
          >
            {error && (
              <motion.span
                animate={{ rotate: [0, -10, 10, -10, 0] }}
                transition={{ duration: 0.5 }}
              >
                ⚠️
              </motion.span>
            )}
            {error || helperText}
          </motion.p>
        )}
      </div>
    )
  }
)

AnimatedInput.displayName = 'AnimatedInput'

export default AnimatedInput

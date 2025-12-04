import { motion, HTMLMotionProps } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import { forwardRef } from 'react'

interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'ref'> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'ghost' | 'neon'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles = `
      inline-flex items-center justify-center gap-2 font-semibold
      transition-all duration-200 focus:outline-none focus-visible:ring-2
      focus-visible:ring-offset-2 focus-visible:ring-primary
      disabled:opacity-50 disabled:cursor-not-allowed
      transform active:scale-95
    `

    const variants = {
      primary: `
        bg-gradient-to-r from-primary to-primary-hover text-text-inverse
        hover:shadow-glow hover:-translate-y-1 hover:shadow-xl
        border-2 border-transparent relative overflow-hidden
        before:absolute before:inset-0 before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent
        before:translate-x-[-200%] hover:before:translate-x-[200%] before:transition-transform before:duration-700
      `,
      secondary: `
        glass text-text-primary border-2 border-border/50
        hover:border-primary hover:shadow-lg hover:shadow-primary/20 hover:-translate-y-1
      `,
      success: `
        bg-gradient-to-r from-success-600 to-success-500 text-white
        hover:shadow-xl hover:shadow-success-500/40 hover:-translate-y-1
        border-2 border-transparent relative overflow-hidden
        before:absolute before:inset-0 before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent
        before:translate-x-[-200%] hover:before:translate-x-[200%] before:transition-transform before:duration-700
      `,
      danger: `
        bg-gradient-to-r from-danger-600 to-danger-500 text-white
        hover:shadow-xl hover:shadow-danger-500/40 hover:-translate-y-1
        border-2 border-transparent relative overflow-hidden
        before:absolute before:inset-0 before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent
        before:translate-x-[-200%] hover:before:translate-x-[200%] before:transition-transform before:duration-700
      `,
      ghost: `
        bg-transparent text-text-primary border-2 border-border/50
        hover:glass hover:border-primary hover:shadow-lg hover:shadow-primary/20
      `,
      neon: `
        bg-gradient-to-r from-primary via-accent to-primary text-white
        bg-[length:200%_auto] hover:bg-right-bottom
        shadow-xl shadow-primary/50 hover:shadow-2xl hover:shadow-accent/60
        hover:-translate-y-1 border-2 border-transparent
        animate-glow relative overflow-hidden
        before:absolute before:inset-0 before:bg-gradient-to-r before:from-transparent before:via-white/30 before:to-transparent
        before:translate-x-[-200%] hover:before:translate-x-[200%] before:transition-transform before:duration-500
      `,
    }

    const sizes = {
      sm: 'px-3 py-1.5 text-sm rounded-lg',
      md: 'px-6 py-3 text-base rounded-xl',
      lg: 'px-8 py-4 text-lg rounded-xl',
    }

    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: disabled || isLoading ? 1 : 1.02 }}
        whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <>
            {leftIcon && <span className="flex-shrink-0">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="flex-shrink-0">{rightIcon}</span>}
          </>
        )}
      </motion.button>
    )
  }
)

Button.displayName = 'Button'

export default Button

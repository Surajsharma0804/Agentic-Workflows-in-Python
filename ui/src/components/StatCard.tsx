import { motion } from 'framer-motion'
import { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatCardProps {
  title: string
  value: number | string
  icon: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple'
  delay?: number
}

const colorClasses = {
  blue: {
    icon: 'text-blue-400',
    bg: 'bg-blue-500/20',
    glow: 'shadow-blue-500/30',
  },
  green: {
    icon: 'text-green-400',
    bg: 'bg-green-500/20',
    glow: 'shadow-green-500/30',
  },
  red: {
    icon: 'text-red-400',
    bg: 'bg-red-500/20',
    glow: 'shadow-red-500/30',
  },
  yellow: {
    icon: 'text-yellow-400',
    bg: 'bg-yellow-500/20',
    glow: 'shadow-yellow-500/30',
  },
  purple: {
    icon: 'text-purple-400',
    bg: 'bg-purple-500/20',
    glow: 'shadow-purple-500/30',
  },
}

export default function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  color = 'blue',
  delay = 0,
}: StatCardProps) {
  const colors = colorClasses[color]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.02, y: -5 }}
      className={cn('card group cursor-pointer', colors.glow)}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-400 mb-1">{title}</p>
          <motion.p
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: delay + 0.2 }}
            className="text-3xl font-bold"
          >
            {value}
          </motion.p>
          {trend && (
            <div className="flex items-center mt-2 text-sm">
              <span
                className={cn(
                  'font-medium',
                  trend.isPositive ? 'text-green-400' : 'text-red-400'
                )}
              >
                {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
              </span>
              <span className="text-gray-500 ml-2">vs last week</span>
            </div>
          )}
        </div>
        <motion.div
          whileHover={{ rotate: 360 }}
          transition={{ duration: 0.5 }}
          className={cn('p-4 rounded-xl', colors.bg)}
        >
          <Icon className={cn('w-8 h-8', colors.icon)} />
        </motion.div>
      </div>
    </motion.div>
  )
}

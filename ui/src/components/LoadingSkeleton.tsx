import { motion } from 'framer-motion'

interface LoadingSkeletonProps {
  className?: string
  count?: number
  height?: string
}

export function LoadingSkeleton({ className = '', count = 1, height = 'h-4' }: LoadingSkeletonProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className={`skeleton ${height} ${className}`}
        />
      ))}
    </>
  )
}

export function CardSkeleton() {
  return (
    <div className="card space-y-4">
      <LoadingSkeleton height="h-6" className="w-1/3" />
      <LoadingSkeleton height="h-4" count={3} />
      <LoadingSkeleton height="h-10" className="w-1/4" />
    </div>
  )
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center space-x-4">
          <LoadingSkeleton height="h-12" className="w-12 rounded-full" />
          <div className="flex-1 space-y-2">
            <LoadingSkeleton height="h-4" className="w-3/4" />
            <LoadingSkeleton height="h-3" className="w-1/2" />
          </div>
        </div>
      ))}
    </div>
  )
}

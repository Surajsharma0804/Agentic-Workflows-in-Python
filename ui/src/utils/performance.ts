/**
 * Performance utilities for optimizing React applications
 */

/**
 * Debounce function to limit how often a function can fire
 * @param fn Function to debounce
 * @param wait Wait time in milliseconds (default: 200ms)
 * @returns Debounced function
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  wait = 200
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      fn(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function to ensure a function is called at most once in a specified time period
 * @param fn Function to throttle
 * @param limit Time limit in milliseconds (default: 200ms)
 * @returns Throttled function
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit = 200
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Lazy load images with Intersection Observer
 * @param imageElement Image element to lazy load
 */
export function lazyLoadImage(imageElement: HTMLImageElement): void {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target as HTMLImageElement;
        const src = img.dataset.src;
        if (src) {
          img.src = src;
          img.classList.remove('lazy');
          observer.unobserve(img);
        }
      }
    });
  });

  imageObserver.observe(imageElement);
}

/**
 * Preload critical resources
 * @param urls Array of URLs to preload
 * @param type Resource type ('image', 'script', 'style', 'font')
 */
export function preloadResources(
  urls: string[],
  type: 'image' | 'script' | 'style' | 'font' = 'image'
): void {
  urls.forEach((url) => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = url;
    link.as = type;
    if (type === 'font') {
      link.crossOrigin = 'anonymous';
    }
    document.head.appendChild(link);
  });
}

/**
 * Measure performance of a function
 * @param fn Function to measure
 * @param label Label for the measurement
 * @returns Result of the function
 */
export async function measurePerformance<T>(
  fn: () => T | Promise<T>,
  label: string
): Promise<T> {
  const start = performance.now();
  const result = await fn();
  const end = performance.now();
  console.log(`[Performance] ${label}: ${(end - start).toFixed(2)}ms`);
  return result;
}

/**
 * Request idle callback with fallback for unsupported browsers
 * @param callback Function to call when idle
 * @param options Options for requestIdleCallback
 */
export function requestIdleCallbackPolyfill(
  callback: IdleRequestCallback,
  options?: IdleRequestOptions
): number {
  if ('requestIdleCallback' in window) {
    return window.requestIdleCallback(callback, options);
  }
  // Fallback for browsers that don't support requestIdleCallback
  return setTimeout(() => {
    const start = Date.now();
    callback({
      didTimeout: false,
      timeRemaining: () => Math.max(0, 50 - (Date.now() - start)),
    });
  }, 1) as unknown as number;
}

/**
 * Cancel idle callback with fallback
 * @param id ID returned from requestIdleCallbackPolyfill
 */
export function cancelIdleCallbackPolyfill(id: number): void {
  if ('cancelIdleCallback' in window) {
    window.cancelIdleCallback(id);
  } else {
    clearTimeout(id);
  }
}

/**
 * Check if user prefers reduced motion
 * @returns True if user prefers reduced motion
 */
export function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Get connection speed
 * @returns Connection effective type or 'unknown'
 */
export function getConnectionSpeed(): string {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const nav = navigator as any;
  const connection = nav.connection || nav.mozConnection || nav.webkitConnection;

  return connection?.effectiveType || 'unknown';
}

/**
 * Check if device is low-end
 * @returns True if device is considered low-end
 */
export function isLowEndDevice(): boolean {
  const connection = getConnectionSpeed();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const memory = (navigator as any).deviceMemory;

  // Consider device low-end if:
  // - Connection is slow-2g or 2g
  // - Device memory is less than 4GB
  return (
    connection === 'slow-2g' ||
    connection === '2g' ||
    (memory && memory < 4)
  );
}

/**
 * Optimize animations based on device capabilities
 * @returns Animation configuration
 */
export function getAnimationConfig(): {
  duration: number;
  enabled: boolean;
} {
  if (prefersReducedMotion()) {
    return { duration: 0, enabled: false };
  }

  if (isLowEndDevice()) {
    return { duration: 150, enabled: true };
  }

  return { duration: 300, enabled: true };
}

/**
 * Report Web Vitals to analytics
 * @param metric Web Vital metric
 */
export function reportWebVitals(metric: {
  name: string;
  value: number;
  id: string;
}): void {
  // Send to analytics service (e.g., Google Analytics, Sentry)
  console.log('[Web Vitals]', metric);

  // Example: Send to Google Analytics
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const win = window as any;
  if (typeof window !== 'undefined' && win.gtag) {
    win.gtag('event', metric.name, {
      value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
      event_category: 'Web Vitals',
      event_label: metric.id,
      non_interaction: true,
    });
  }
}

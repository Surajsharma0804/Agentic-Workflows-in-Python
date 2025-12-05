// Test setup file - only loaded during testing
// This file is excluded from production builds

// Mock window.matchMedia for tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }),
})

// Mock IntersectionObserver for tests
if (typeof window !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).IntersectionObserver = class IntersectionObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    takeRecords() {
      return []
    }
    unobserve() {}
  };

  // Mock ResizeObserver for tests
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).ResizeObserver = class ResizeObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    unobserve() {}
  }
}

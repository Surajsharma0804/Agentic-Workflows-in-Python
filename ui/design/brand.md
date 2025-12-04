# 🎨 Agentic Workflows - Brand Design System

## Brand Identity

**Mission**: Empower developers with AI-powered workflow automation that's intuitive, powerful, and beautiful.

**Visual Language**: Futuristic, professional, trustworthy, innovative

---

## Color Palette

### Primary Colors
```css
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-200: #bfdbfe;
--primary-300: #93c5fd;
--primary-400: #60a5fa;
--primary-500: #3b82f6;  /* Main brand color */
--primary-600: #2563eb;
--primary-700: #1d4ed8;
--primary-800: #1e40af;
--primary-900: #1e3a8a;
```

### Secondary Colors
```css
--secondary-50: #faf5ff;
--secondary-100: #f3e8ff;
--secondary-200: #e9d5ff;
--secondary-300: #d8b4fe;
--secondary-400: #c084fc;
--secondary-500: #a855f7;  /* Accent color */
--secondary-600: #9333ea;
--secondary-700: #7e22ce;
--secondary-800: #6b21a8;
--secondary-900: #581c87;
```

### Neon Accents (for highlights)
```css
--neon-blue: #00f0ff;
--neon-purple: #b000ff;
--neon-pink: #ff00ff;
--neon-green: #00ff88;
```

### Semantic Colors
```css
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

### Dark Theme (Primary)
```css
--dark-bg: #0a0a0f;
--dark-surface: #13131a;
--dark-surface-elevated: #1a1a24;
--dark-border: #1f1f2e;
--dark-hover: #252533;
--dark-text: #ffffff;
--dark-text-secondary: #a1a1aa;
--dark-text-tertiary: #71717a;
```

### Light Theme (Optional)
```css
--light-bg: #ffffff;
--light-surface: #f9fafb;
--light-border: #e5e7eb;
--light-hover: #f3f4f6;
--light-text: #111827;
--light-text-secondary: #6b7280;
```

---

## Typography

### Font Families
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Type Scale
```css
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
--text-5xl: 3rem;        /* 48px */
--text-6xl: 3.75rem;     /* 60px */
```

### Font Weights
```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

### Line Heights
```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

---

## Spacing System

Based on 4px base unit:

```css
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

---

## Border Radius

```css
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-base: 0.25rem;  /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-3xl: 1.5rem;    /* 24px */
--radius-full: 9999px;
```

---

## Shadows

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
--shadow-glow-blue: 0 0 20px rgba(59, 130, 246, 0.5);
--shadow-glow-purple: 0 0 20px rgba(168, 85, 247, 0.5);
```

---

## Iconography

### Icon Set: Lucide React
- Consistent 24px base size
- 2px stroke width
- Rounded line caps
- Semantic naming

### Icon Usage Guidelines
- **Navigation**: Use outline style
- **Actions**: Use filled style for primary actions
- **Status**: Use colored icons with semantic meaning
- **Decorative**: Use subtle, low-contrast icons

---

## Animation Principles

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Duration
```css
--duration-fast: 150ms;
--duration-base: 200ms;
--duration-slow: 300ms;
--duration-slower: 500ms;
```

### Animation Guidelines
- **Micro-interactions**: 150-200ms
- **Page transitions**: 300-500ms
- **Loading states**: Continuous, smooth
- **Respect prefers-reduced-motion**

---

## Component Patterns

### Cards
- Background: `--dark-surface`
- Border: `--dark-border`
- Padding: `--space-6`
- Radius: `--radius-xl`
- Hover: Lift with shadow + border color change

### Buttons
- **Primary**: Gradient blue-purple, white text, shadow
- **Secondary**: Dark surface, border, hover lift
- **Ghost**: Transparent, border on hover
- **Danger**: Red gradient, white text
- Height: 40px (base), 48px (large), 32px (small)
- Padding: 16px horizontal

### Inputs
- Background: `--dark-bg`
- Border: `--dark-border`
- Focus: Blue ring, 2px
- Height: 40px
- Padding: 12px horizontal

### Badges
- Small, rounded-full
- Semantic colors with 20% opacity background
- Border with 30% opacity
- 8px horizontal padding

---

## Accessibility Standards

### Color Contrast
- Text on background: Minimum 4.5:1 (WCAG AA)
- Large text: Minimum 3:1
- UI components: Minimum 3:1

### Focus Indicators
- Visible 2px outline
- Blue color (#3b82f6)
- 2px offset from element

### Touch Targets
- Minimum 44x44px for interactive elements
- 8px spacing between targets

---

## Responsive Breakpoints

```css
--screen-sm: 640px;
--screen-md: 768px;
--screen-lg: 1024px;
--screen-xl: 1280px;
--screen-2xl: 1536px;
```

### Mobile-First Approach
- Design for 375px width first
- Progressive enhancement for larger screens
- Touch-friendly interactions on mobile

---

## Logo Usage

### Primary Logo
- SVG format for scalability
- Minimum size: 120px width
- Clear space: 16px on all sides
- Dark background version (white/blue)
- Light background version (blue/purple)

### Favicon
- 32x32px, 16x16px sizes
- SVG for modern browsers
- ICO fallback for legacy

---

## Brand Voice

### Tone
- **Professional** but approachable
- **Technical** but not intimidating
- **Innovative** but reliable
- **Confident** but humble

### Writing Style
- Active voice
- Short sentences
- Clear, concise language
- Technical accuracy
- Helpful, not condescending

---

## Usage Examples

### Hero Section
```tsx
<div className="bg-gradient-to-br from-primary-600 to-secondary-600">
  <h1 className="text-6xl font-bold text-white">
    AI-Powered Workflow Automation
  </h1>
</div>
```

### Card Component
```tsx
<div className="card hover:border-primary-500/50 transition-all">
  <h3 className="text-xl font-semibold mb-2">Workflow Name</h3>
  <p className="text-gray-400">Description</p>
</div>
```

### Button Component
```tsx
<button className="btn-primary">
  <Play className="w-5 h-5 mr-2" />
  Run Workflow
</button>
```

---

## Design Tokens Export

All design tokens are available in:
- `tailwind.config.js` - For Tailwind CSS
- `src/styles/tokens.css` - For CSS variables
- `src/lib/design-tokens.ts` - For TypeScript

---

**Last Updated**: December 2025
**Version**: 1.0.0
**Maintained By**: Agentic Workflows Team

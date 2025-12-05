# Agentic Workflows - Frontend

Modern React + TypeScript frontend for the Agentic Workflows platform.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **TanStack Query** - Data fetching
- **Playwright** - E2E testing

## Quick Start

```bash
# Install dependencies
npm ci

# Start development server
npm run dev

# Access at http://localhost:3000
```

## Available Scripts

### Development

```bash
npm run dev          # Start development server with hot reload
npm run preview      # Preview production build locally
```

### Building

```bash
npm run build        # Build for production (includes sitemap generation)
npm run build:check  # Type check + build
```

### Code Quality

```bash
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues automatically
npm run type-check   # Run TypeScript type checking
```

### Testing

```bash
npm run test:e2e         # Run E2E tests (headless)
npm run test:e2e:ui      # Run E2E tests with UI
npm run test:e2e:headed  # Run E2E tests in headed mode
```

## Project Structure

```
ui/
├── public/              # Static assets
│   ├── robots.txt      # SEO robots file
│   └── manifest.json   # PWA manifest
├── src/
│   ├── components/     # Reusable components
│   ├── contexts/       # React contexts
│   ├── hooks/          # Custom hooks
│   ├── lib/            # Utilities and API client
│   ├── pages/          # Page components
│   ├── App.tsx         # Main app component
│   └── main.tsx        # Entry point
├── e2e/                # Playwright E2E tests
├── scripts/            # Build scripts
│   └── generate-sitemap.js
└── dist/               # Build output (generated)
```

## Environment Variables

Create a `.env` file in the `ui/` directory:

```env
# API URL (optional, defaults to relative path)
VITE_API_URL=

# Feature flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_TRACKING=true
```

## Development Guidelines

### Component Structure

```typescript
// Use functional components with TypeScript
import { FC } from 'react';

interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export const MyComponent: FC<MyComponentProps> = ({ title, onAction }) => {
  return (
    <div>
      <h1>{title}</h1>
      <button onClick={onAction}>Action</button>
    </div>
  );
};
```

### API Calls

```typescript
// Use the API client from lib/api.ts
import { workflowAPI } from '@/lib/api';

const fetchWorkflows = async () => {
  const response = await workflowAPI.list();
  return response.data;
};
```

### Styling

```typescript
// Use Tailwind CSS classes
<div className="flex items-center justify-between p-4 bg-surface rounded-lg">
  <h2 className="text-xl font-bold text-text-primary">Title</h2>
</div>
```

## Performance Optimization

### Code Splitting

Routes are automatically code-split by Vite. For manual code splitting:

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>
```

### Image Optimization

Images are automatically optimized during build. Use responsive images:

```typescript
<img
  src="/images/hero.jpg"
  srcSet="/images/hero-320w.jpg 320w, /images/hero-640w.jpg 640w"
  sizes="(max-width: 640px) 320px, 640px"
  alt="Hero image"
  loading="lazy"
/>
```

## Testing

### Writing E2E Tests

```typescript
// e2e/my-feature.spec.ts
import { test, expect } from '@playwright/test';

test('feature works correctly', async ({ page }) => {
  await page.goto('/my-feature');
  await expect(page.locator('h1')).toContainText('My Feature');
});
```

### Running Tests

```bash
# Run all tests
npm run test:e2e

# Run specific test file
npx playwright test e2e/my-feature.spec.ts

# Debug tests
npm run test:e2e:ui
```

## Build Output

The build process generates:

- Optimized JavaScript bundles (code-split)
- Minified CSS
- Optimized images (WebP/AVIF)
- Source maps (development only)
- sitemap.xml
- robots.txt

## Deployment

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Deploy to Static Hosting

```bash
# The dist/ folder can be deployed to:
# - Netlify
# - Vercel
# - Cloudflare Pages
# - AWS S3 + CloudFront
# - Any static hosting service
```

### Deploy with Backend

The backend serves the built frontend from `ui/dist/`. Just build and the backend will serve it.

## Troubleshooting

### Build Fails

```bash
# Clear cache and rebuild
rm -rf node_modules/.vite
npm run build
```

### Type Errors

```bash
# Check types
npm run type-check

# Common fix: restart TypeScript server in VS Code
# Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"
```

### E2E Tests Fail

```bash
# Install/update browsers
npx playwright install

# Run with UI to debug
npm run test:e2e:ui
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests: `npm run lint && npm run type-check && npm run test:e2e`
4. Submit PR

## Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Playwright Documentation](https://playwright.dev/)

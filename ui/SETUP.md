# UI Setup Guide

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running on http://localhost:8000

## Installation

### Step 1: Install Dependencies

```bash
cd ui
npm install
```

This will install all required packages:
- react & react-dom
- react-router-dom
- @tanstack/react-query
- axios
- lucide-react
- react-hot-toast
- tailwindcss
- And more...

### Step 2: Start Development Server

```bash
npm run dev
```

The UI will be available at http://localhost:5173

### Step 3: Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Troubleshooting

### TypeScript Errors

If you see TypeScript errors about missing modules, it means dependencies aren't installed yet.

**Solution**: Run `npm install` in the `ui/` directory.

### Port Already in Use

If port 5173 is already in use, you can change it in `vite.config.ts`:

```typescript
export default defineConfig({
  server: {
    port: 3000  // Change to your preferred port
  }
})
```

### API Connection Issues

1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check CORS settings in backend
3. Update API_BASE_URL in `src/lib/api.ts` if needed

## Development Workflow

1. **Install dependencies** (first time only):
   ```bash
   npm install
   ```

2. **Start dev server**:
   ```bash
   npm run dev
   ```

3. **Make changes** - Hot reload is enabled

4. **Type check**:
   ```bash
   npm run type-check
   ```

5. **Lint code**:
   ```bash
   npm run lint
   ```

6. **Build for production**:
   ```bash
   npm run build
   ```

## Note About TypeScript Errors

If you see TypeScript errors in your IDE before running `npm install`, this is normal. The errors will disappear once you:

1. Navigate to the `ui/` directory
2. Run `npm install`
3. Restart your IDE/editor

The TypeScript configuration is set to be lenient until dependencies are installed.

## Quick Start

```bash
# One-command setup and start
cd ui && npm install && npm run dev
```

Then visit http://localhost:5173

## Environment Variables

Create a `.env.local` file in the `ui/` directory:

```env
VITE_API_URL=http://localhost:8000/api
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Check TypeScript types |

## Dependencies

### Core
- React 18.2
- React Router 6.21
- TypeScript 5.3

### UI & Styling
- Tailwind CSS 3.4
- Lucide React (icons)
- Framer Motion (animations)

### Data & State
- TanStack Query (data fetching)
- Zustand (state management)
- Axios (HTTP client)

### Utilities
- date-fns (date formatting)
- react-hot-toast (notifications)
- recharts (charts)
- react-markdown (markdown rendering)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Next Steps

After installation:
1. Explore the pages in `src/pages/`
2. Check the API client in `src/lib/api.ts`
3. Customize the theme in `tailwind.config.js`
4. Add your own components in `src/components/`

---

**Status**: Ready for development  
**Last Updated**: December 2025

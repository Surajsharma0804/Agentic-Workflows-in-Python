# Agentic Workflows - Web Dashboard

Modern, responsive web dashboard for managing and monitoring agentic workflows.

## Features

- **Dashboard**: Overview of workflows, executions, and system health
- **Workflow Runner**: Execute workflows with real-time progress tracking
- **DAG Visualizer**: Visual workflow builder with drag-and-drop interface
- **Plugin Explorer**: Browse and manage available plugins
- **Audit Viewer**: View comprehensive audit logs
- **AI Assistant**: Natural language workflow creation
- **Settings**: Configure system preferences

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Routing**: React Router v6
- **Icons**: Lucide React
- **State Management**: React Hooks
- **API Client**: Axios

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running on http://localhost:8000

### Installation

```bash
# Navigate to UI directory
cd ui

# Install dependencies (REQUIRED - fixes TypeScript errors)
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### ⚠️ Important: TypeScript Errors

If you see TypeScript errors about missing modules (react, lucide-react, etc.), you need to install dependencies first:

```bash
cd ui
npm install
```

After installation, restart your IDE/editor and the errors will disappear.

See [SETUP.md](./SETUP.md) for detailed installation instructions.

### Development

```bash
# Run with hot reload
npm run dev

# Access at http://localhost:5173
```

## Project Structure

```
ui/
├── src/
│   ├── components/          # Reusable UI components
│   │   └── Layout.tsx       # Main layout with navigation
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── WorkflowRunner.tsx
│   │   ├── DAGVisualizer.tsx
│   │   ├── PluginExplorer.tsx
│   │   ├── AuditViewer.tsx
│   │   ├── AIAssistant.tsx
│   │   ├── Settings.tsx
│   │   └── About.tsx
│   ├── lib/                 # Utilities and API client
│   │   ├── api.ts           # API client
│   │   └── utils.ts         # Helper functions
│   ├── App.tsx              # Main app component with routing
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── vite.config.ts           # Vite config
└── tailwind.config.js       # Tailwind config
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint |

## Pages Overview

### Dashboard
- Workflow statistics and metrics
- Recent executions
- System health indicators
- Quick actions

### Workflow Runner
- Select and execute workflows
- Real-time progress tracking
- View execution logs
- Download results

### DAG Visualizer
- Visual workflow builder
- Drag-and-drop interface
- Node configuration
- Connection management

### Plugin Explorer
- Browse available plugins
- View plugin documentation
- Install/uninstall plugins
- Plugin configuration

### Audit Viewer
- Comprehensive audit logs
- Filter and search
- Export logs
- Timeline view

### AI Assistant
- Natural language workflow creation
- Workflow optimization suggestions
- Interactive chat interface
- Code generation

### Settings
- API configuration
- Theme preferences
- Notification settings
- User preferences

## API Integration

The dashboard connects to the backend API at `http://localhost:8000/api`.

### API Endpoints Used

- `GET /api/health` - Health check
- `GET /api/workflows` - List workflows
- `POST /api/workflows/execute` - Execute workflow
- `GET /api/plugins` - List plugins
- `GET /api/audit` - Get audit logs
- `POST /api/llm/generate` - AI workflow generation

### Configuration

Update API base URL in `src/lib/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

Or set environment variable:

```bash
# .env.local
VITE_API_URL=http://your-api-url/api
```

## Styling

### Tailwind CSS

The project uses Tailwind CSS for styling. Configuration in `tailwind.config.js`.

### Theme

Dark mode support with system preference detection.

### Custom Colors

```javascript
colors: {
  primary: '#3b82f6',
  secondary: '#8b5cf6',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
}
```

## Development Tips

### Hot Reload

Vite provides instant hot module replacement (HMR) for fast development.

### TypeScript

Full TypeScript support with strict mode enabled.

### Code Organization

- Keep components small and focused
- Use custom hooks for reusable logic
- Separate API calls in `lib/api.ts`
- Use TypeScript interfaces for type safety

### Performance

- Lazy load pages with React.lazy()
- Optimize images and assets
- Use React.memo() for expensive components
- Implement virtual scrolling for large lists

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Output in dist/ directory
# Serve with any static file server
```

### Deployment Options

#### Static Hosting
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

#### Docker
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Port Already in Use

```bash
# Change port in vite.config.ts
server: {
  port: 3000
}
```

### API Connection Issues

1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check CORS settings in backend
3. Update API_BASE_URL in `src/lib/api.ts`

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Write meaningful component names
4. Add comments for complex logic
5. Test on multiple browsers

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: See main README.md
- API Docs: http://localhost:8000/api/docs

---

**Status**: Production Ready
**Version**: 1.0.0
**Last Updated**: December 2025

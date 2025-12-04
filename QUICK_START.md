# 🚀 Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (for production) or SQLite (for development)

## 🏃 Development Setup

### 1. Backend Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements-full.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn agentic_workflows.api.server:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd ui

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173
```

## 🎨 New UI Features

### Responsive Design
- ✅ Mobile-first (375px → 1536px)
- ✅ Tablet & desktop optimized
- ✅ Touch-friendly (44px tap targets)

### Theme System
- ✅ Light/Dark modes
- ✅ System preference detection
- ✅ Persistent across sessions

### Animations
- ✅ Smooth page transitions
- ✅ Button micro-interactions
- ✅ Form validation feedback
- ✅ Reduced-motion support

### Accessibility
- ✅ WCAG AA compliant
- ✅ Keyboard navigation
- ✅ Screen reader friendly
- ✅ Focus indicators

## 🧪 Testing

### Frontend Tests
```bash
cd ui
npm run test        # Unit tests
npm run test:e2e    # Playwright E2E tests
```

### Backend Tests
```bash
pytest tests/
```

## 📦 Production Build

### Frontend
```bash
cd ui
npm run build
# Output in ui/dist/
```

### Docker
```bash
docker build -t agentic-workflows .
docker run -p 8000:8000 agentic-workflows
```

## 🎯 Key Pages

- **Login**: `/login` - Redesigned with animations
- **Dashboard**: `/` - Overview and stats
- **Workflow Runner**: `/run` - Execute workflows
- **AI Assistant**: `/ai` - Chat interface
- **Plugins**: `/plugins` - Browse plugins
- **Audit Log**: `/audit` - View execution history
- **DAG Visualizer**: `/dag` - Visual workflow editor
- **Settings**: `/settings` - User preferences

## 🎨 Using the Design System

### Theme Hook
```typescript
import { useTheme } from '@/hooks/useTheme'

function MyComponent() {
  const { theme, toggleTheme } = useTheme()
  return <button onClick={toggleTheme}>Toggle Theme</button>
}
```

### Button Component
```typescript
import Button from '@/components/ui/Button'

<Button variant="primary" size="lg">
  Click Me
</Button>
```

### Animated Input
```typescript
import AnimatedInput from '@/components/ui/AnimatedInput'

<AnimatedInput
  label="Email"
  type="email"
  leftIcon={<Mail />}
/>
```

## 🐛 Troubleshooting

### CSS Warnings in VS Code
These are normal for Tailwind CSS. The `.vscode/settings.json` file suppresses them.

### Build Errors
```bash
# Clear cache and rebuild
rm -rf node_modules ui/dist
npm install
npm run build
```

### Database Issues
```bash
# Reset database
alembic downgrade base
alembic upgrade head
```

## 📚 Documentation

- **Design System**: `/design/colors.md`
- **Responsive Testing**: `/demo/responsive-checklist.md`
- **Technical Decisions**: `/fixes/DECISIONS.md`
- **Architecture**: `/ARCHITECTURE.md`

## 🚢 Deployment

See `/docs/deployment/` for platform-specific guides:
- Render.com (current)
- Docker
- AWS
- Vercel (frontend only)

## 💡 Tips

1. **Use the theme toggle** in the top right to switch between light/dark modes
2. **Test responsive design** using browser DevTools (F12 → Toggle Device Toolbar)
3. **Check accessibility** with keyboard navigation (Tab through elements)
4. **Monitor performance** with Lighthouse audits

## 🆘 Need Help?

- Check `/demo/responsive-checklist.md` for validation steps
- Review `/fixes/DECISIONS.md` for technical details
- Run tests to verify functionality
- Check browser console for errors

---

**Version**: 2.0.0  
**Last Updated**: December 4, 2025  
**Status**: ✅ Production Ready

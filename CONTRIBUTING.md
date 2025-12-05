# Contributing to Agentic Workflows

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check existing [Issues](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues) and [Discussions](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/discussions)
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Why this would be useful
   - Possible implementation approach

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit** with clear messages:
   ```bash
   git commit -m "feat: add new plugin for X"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots/videos if UI changes
   - Test results

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)

### Backend Setup
```bash
# Clone repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-full.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn agentic_workflows.api.server:app --reload
```

### Frontend Setup
```bash
cd ui
npm install
npm run dev
```

## Coding Standards

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Use async/await for I/O operations
- Keep functions small and focused
- Add tests for new features

Example:
```python
async def create_workflow(
    name: str,
    description: str,
    spec: dict
) -> Workflow:
    """
    Create a new workflow.
    
    Args:
        name: Workflow name
        description: Workflow description
        spec: Workflow specification
        
    Returns:
        Created workflow instance
        
    Raises:
        ValidationError: If spec is invalid
    """
    # Implementation
```

### TypeScript (Frontend)
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable
- Add proper error handling

Example:
```typescript
interface WorkflowProps {
  id: string
  name: string
  onExecute: (id: string) => Promise<void>
}

export function WorkflowCard({ id, name, onExecute }: WorkflowProps) {
  // Implementation
}
```

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add Slack notification plugin
fix: resolve OAuth callback error
docs: update API documentation
refactor: simplify workflow execution logic
```

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_workflows.py

# Run with coverage
pytest --cov=agentic_workflows
```

### Frontend Tests
```bash
cd ui
npm test
npm run test:coverage
```

## Adding New Plugins

1. Create plugin file in `agentic_workflows/plugins/`
2. Inherit from `PluginBase`
3. Implement `plan()` and `execute()` methods
4. Add to plugin registry in `plugins.py`
5. Write tests
6. Update documentation

Example:
```python
from .base import PluginBase

class MyPlugin(PluginBase):
    name = "my_plugin"
    
    def plan(self) -> list:
        return [{"action": "do_something"}]
    
    def execute(self) -> dict:
        # Implementation
        return {"status": "success"}
```

## Documentation

- Update README.md if adding major features
- Add docstrings to all functions/classes
- Update API documentation if changing endpoints
- Add examples for new features

## Review Process

1. Automated checks must pass (tests, linting)
2. Code review by maintainer
3. Address feedback
4. Approval and merge

## Questions?

- Open a [Discussion](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/discussions)
- Email: surajkumarind08@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

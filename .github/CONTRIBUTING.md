# Contributing to Agentic Workflows

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include detailed steps to reproduce
4. Include system information and logs

### Suggesting Features

1. Check if the feature has been suggested
2. Use the feature request template
3. Explain the use case and benefits
4. Provide examples if possible

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `pytest -v` and `npm test --prefix ui`
5. **Run linters**: `npm run lint --prefix ui`
6. **Commit with clear messages**: `git commit -m 'feat: add amazing feature'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd agentic-workflows

# Backend setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-full.txt
pip install -e .

# Frontend setup
cd ui
npm install

# Run tests
pytest -v
npm test --prefix ui
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Maximum line length: 100 characters

### TypeScript/React
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Write meaningful component names

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add workflow execution endpoint
fix(ui): resolve login form validation issue
docs(readme): update installation instructions
```

## Testing Requirements

- All new features must include tests
- Maintain 100% test pass rate
- Add integration tests for API endpoints
- Add unit tests for utility functions

## Review Process

1. Automated checks must pass (CI/CD)
2. Code review by maintainer
3. Address review comments
4. Approval and merge

## Questions?

Feel free to open an issue for any questions or clarifications.

Thank you for contributing! 🎉

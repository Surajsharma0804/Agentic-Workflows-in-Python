# Setup Guide

## Prerequisites

- Python 3.10 or higher (tested with Python 3.14)
- pip package manager

## Installation

### 1. Clone or Download the Repository

```bash
cd agentic-workflows
```

### 2. Create a Virtual Environment

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the Package in Editable Mode

```bash
pip install -e .
```

This makes the `agentic-workflows` command available globally in your virtual environment.

### 5. Install Development Dependencies (Optional)

```bash
pip install pytest
```

## Verify Installation

### Check CLI is Available

```bash
agentic-workflows --help
```

You should see:
```
Usage: agentic-workflows [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run
```

### Run Tests

```bash
pytest -v
```

All tests should pass.

### Run Example Workflows

**File Organizer (Dry Run):**
```bash
agentic-workflows run --spec .kiro/specs/lazy_file_butler.yaml
```

**Email Summarizer (Dry Run):**
```bash
agentic-workflows run --spec .kiro/specs/email_summarizer.yaml
```

**Actual Execution (No Dry Run):**
```bash
agentic-workflows run --spec .kiro/specs/lazy_file_butler.yaml --no-dry-run
```

## Project Structure

```
agentic-workflows/
├── agentic_workflows/          # Main package
│   ├── core/                   # Core orchestration
│   │   ├── agents.py          # Planner & Executor agents
│   │   ├── audit.py           # Audit logging
│   │   ├── orchestrator.py    # Main orchestrator
│   │   └── spec.py            # Workflow spec models
│   ├── plugins/               # Task plugins
│   │   ├── base.py           # Plugin base class
│   │   ├── file_organizer.py # File organization plugin
│   │   ├── email_summarizer.py
│   │   └── http_task.py
│   ├── utils/                # Utilities
│   └── runner.py             # CLI entry point
├── .kiro/                    # Kiro IDE configuration
│   ├── specs/               # Workflow specifications
│   └── steering/            # Agent steering rules
├── examples/                # Example data
├── tests/                   # Test suite
├── pyproject.toml          # Package configuration
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Creating Custom Workflows

1. Create a new YAML file in `.kiro/specs/`
2. Define your workflow structure:

```yaml
id: my-workflow
name: My Custom Workflow
description: What this workflow does

tasks:
  - id: task1
    type: file_organizer  # or email_summarizer, http_task
    params:
      target: ./path/to/files
      dry_run: true
```

3. Run it:
```bash
agentic-workflows run --spec .kiro/specs/my-workflow.yaml
```

## Troubleshooting

### Import Errors

If you see import errors, try:
```bash
pip install -e . --force-reinstall --no-deps
```

### Module Not Found

Make sure your virtual environment is activated:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Tests Failing

Clear Python cache and reinstall:
```bash
# Windows
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force

# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} +

pip install -e .
pytest -v
```

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [examples/README.md](examples/README.md) for sample workflows
- Explore `.kiro/specs/` for workflow templates
- Create custom plugins by extending `PluginBase`

## Support

For issues or questions, check the project documentation or create an issue in the repository.

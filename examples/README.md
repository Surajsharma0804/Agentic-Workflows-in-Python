# Examples

This directory contains example workflows and sample data for testing the agentic workflows framework.

## Available Examples

### 1. Lazy File Butler
Organizes files in the `demo_downloads` directory by category, normalizes filenames, and detects duplicates.

**Run:**
```bash
python -m agentic_workflows.runner run --spec .kiro/specs/lazy_file_butler.yaml --dry-run
```

### 2. Email Summarizer
Summarizes emails from a text file into concise summaries.

**Run:**
```bash
python -m agentic_workflows.runner run --spec .kiro/specs/email_summarizer.yaml --dry-run
```

## Demo Downloads Directory

The `demo_downloads` folder is used for testing the file organizer plugin. Add test files here to see the organization in action.

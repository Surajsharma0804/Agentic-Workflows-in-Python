# Kiro Agent Steering - Lazy Agentic Workflows Project

- Project tone: clear, production-ready Python 3.10+ code.
- Testing: every new function must include unit tests (pytest).
- Non-destructive default: never delete files automatically. Put duplicates into a "duplicates/" folder unless user explicitly requests deletion with `allow_destructive=true`.
- Naming & style: snake_case for functions and files; PEP8 for code.
- Logging: use audit.log for all plugin actions with structured JSON lines.
- Spec mapping: workflow spec fields should map directly to plugin params.
- Acceptance criteria: each task must expose `plan()` and `execute()` then pass unit tests.

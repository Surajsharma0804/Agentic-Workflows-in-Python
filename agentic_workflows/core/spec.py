"""Workflow specification data models and loading."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import yaml
from pathlib import Path


@dataclass
class TaskSpec:
    """Specification for a single task in a workflow."""
    id: str
    type: str
    params: Dict[str, Any] = field(default_factory=dict)
    run_if: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowSpec:
    """Specification for a complete workflow."""
    id: str
    name: str
    description: str
    tasks: List[TaskSpec] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


def load_spec(path: str) -> WorkflowSpec:
    """Load a workflow specification from a YAML file."""
    p = Path(path)
    data = yaml.safe_load(p.read_text())
    tasks = [
        TaskSpec(
            id=t.get('id'),
            type=t.get('type'),
            params=t.get('params', {}),
            run_if=t.get('run_if')
        )
        for t in data.get('tasks', [])
    ]
    return WorkflowSpec(
        id=data.get('id'),
        name=data.get('name'),
        description=data.get('description', ''),
        tasks=tasks,
        metadata=data.get('metadata', {})
    )

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
    """Load a workflow specification from a YAML file with validation."""
    p = Path(path)
    
    # Validate file exists
    if not p.exists():
        raise FileNotFoundError(f"Spec file not found: {path}")
    
    # Load and validate YAML
    try:
        data = yaml.safe_load(p.read_text())
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}")
    
    # Validate structure
    if not isinstance(data, dict):
        raise ValueError(f"Spec must be a YAML object, got {type(data)}")
    
    # Validate required fields
    if 'id' not in data:
        raise ValueError("Spec missing required field: id")
    if 'name' not in data:
        raise ValueError("Spec missing required field: name")
    
    # Validate and load tasks
    tasks = []
    for i, t in enumerate(data.get('tasks', [])):
        if not isinstance(t, dict):
            raise ValueError(f"Task {i} must be an object, got {type(t)}")
        
        task_id = t.get('id')
        task_type = t.get('type')
        
        if not task_id:
            raise ValueError(f"Task {i} missing required field: id")
        if not task_type:
            raise ValueError(f"Task {i} missing required field: type")
        
        tasks.append(TaskSpec(
            id=task_id,
            type=task_type,
            params=t.get('params', {}),
            run_if=t.get('run_if')
        ))
    
    return WorkflowSpec(
        id=data['id'],
        name=data['name'],
        description=data.get('description', ''),
        tasks=tasks,
        metadata=data.get('metadata', {})
    )

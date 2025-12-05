from agentic_workflows.core.orchestrator import Orchestrator
from agentic_workflows.core.spec import WorkflowSpec, TaskSpec
import tempfile
from pathlib import Path

def test_orchestrator_dry_run(tmp_path):
    # Create test directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Create a simple spec file
    spec_path = tmp_path / "test_spec.yaml"
    spec_path.write_text(f"""
id: test-workflow
name: Test Workflow
description: A test workflow
tasks:
  - id: task1
    type: file_organizer
    params:
      target: {str(test_dir)}
      dry_run: true
""")
    
    audit_path = tmp_path / "audit.log"
    orch = Orchestrator(audit_path=str(audit_path))
    result = orch.run_spec(str(spec_path), dry_run=True)
    
    assert result["spec"] == "Test Workflow"
    assert len(result["plan"]) == 1
    assert result["plan"][0]["type"] == "file_organizer"
    assert audit_path.exists()

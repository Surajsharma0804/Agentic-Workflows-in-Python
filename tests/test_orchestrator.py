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
    
    # Verify new response structure
    assert result["workflow_name"] == "Test Workflow"
    assert result["status"] in ("success", "partial_failure")
    assert result["dry_run"] is True
    assert "workflow_id" in result
    assert "duration_seconds" in result
    assert "start_timestamp" in result
    assert "end_timestamp" in result
    assert result["tasks_total"] == 1
    assert "results" in result
    assert "metadata" in result
    assert audit_path.exists()

"""Test that workflow runs produce unique, dynamic outputs."""
from agentic_workflows.core.orchestrator import Orchestrator
from pathlib import Path
import time


def test_runs_produce_unique_outputs(tmp_path):
    """Verify that each workflow run produces unique identifiers and timestamps."""
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
    
    # Run workflow twice
    result1 = orch.run_spec(str(spec_path), dry_run=True)
    time.sleep(0.1)  # Small delay to ensure different timestamps
    result2 = orch.run_spec(str(spec_path), dry_run=True)
    
    # Verify workflow_id is unique
    assert result1["workflow_id"] != result2["workflow_id"], \
        "Each run should have a unique workflow_id"
    
    # Verify timestamps are different
    assert result1["start_timestamp"] != result2["start_timestamp"], \
        "Each run should have different start timestamps"
    assert result1["end_timestamp"] != result2["end_timestamp"], \
        "Each run should have different end timestamps"
    
    # Verify both have required fields
    for result in [result1, result2]:
        assert "workflow_id" in result
        assert "duration_seconds" in result
        assert isinstance(result["duration_seconds"], (int, float))
        assert "start_timestamp" in result
        assert "end_timestamp" in result
        assert "metadata" in result
        assert "results" in result
        assert result["status"] in ("success", "partial_failure")
    
    print(f"\n✅ Run 1 ID: {result1['workflow_id']}")
    print(f"✅ Run 2 ID: {result2['workflow_id']}")
    print(f"✅ Run 1 Duration: {result1['duration_seconds']}s")
    print(f"✅ Run 2 Duration: {result2['duration_seconds']}s")
    print(f"✅ Runs are unique and distinguishable!")


def test_task_timing_details(tmp_path):
    """Verify that tasks have detailed timing information."""
    # Create test directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Create spec with multiple tasks
    spec_path = tmp_path / "test_spec.yaml"
    spec_path.write_text(f"""
id: multi-task-workflow
name: Multi Task Workflow
description: Workflow with multiple tasks
tasks:
  - id: task1
    type: file_organizer
    params:
      target: {str(test_dir)}
      dry_run: true
  - id: task2
    type: http_task
    params:
      url: https://httpbin.org/get
      method: GET
      dry_run: true
""")
    
    audit_path = tmp_path / "audit.log"
    orch = Orchestrator(audit_path=str(audit_path))
    result = orch.run_spec(str(spec_path), dry_run=True)
    
    # Verify task-level timing
    assert "results" in result
    results = result["results"]
    
    for task_id, task_result in results.items():
        assert "start_ts" in task_result, f"Task {task_id} missing start_ts"
        assert "end_ts" in task_result, f"Task {task_id} missing end_ts"
        assert "duration_seconds" in task_result, f"Task {task_id} missing duration_seconds"
        assert isinstance(task_result["duration_seconds"], (int, float))
        assert task_result["duration_seconds"] >= 0
        assert "status" in task_result
        assert "type" in task_result
        
        print(f"\n✅ Task {task_id}:")
        print(f"   Type: {task_result['type']}")
        print(f"   Status: {task_result['status']}")
        print(f"   Duration: {task_result['duration_seconds']}s")
        print(f"   Start: {task_result['start_ts']}")
        print(f"   End: {task_result['end_ts']}")
    
    # Verify overall timing
    assert result["tasks_total"] == 2
    assert "executor_duration_seconds" in result["metadata"]
    assert "duration_seconds" in result
    print(f"\n✅ Overall Duration: {result['duration_seconds']}s")
    print(f"✅ Executor Duration: {result['metadata']['executor_duration_seconds']}s")
    print(f"✅ All tasks have detailed timing information!")

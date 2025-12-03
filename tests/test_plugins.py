"""Plugin tests."""
import pytest
from agentic_workflows.plugins.file_organizer import FileOrganizer, normalize_filename
from agentic_workflows.plugins.email_summarizer import EmailSummarizer
from agentic_workflows.plugins.http_task import HTTPTask

def test_normalize_filename():
    assert normalize_filename("My File.TXT") == "my_file.txt"
    assert normalize_filename("Test@#$%.pdf") == "test.pdf"

def test_file_organizer_plan(tmp_path):
    organizer = FileOrganizer({"target": str(tmp_path), "dry_run": True})
    plan = organizer.plan()
    assert isinstance(plan, list)

def test_email_summarizer_plan():
    summarizer = EmailSummarizer({"source_path": "nonexistent.txt", "dry_run": True})
    plan = summarizer.plan()
    assert isinstance(plan, list)

def test_http_task_plan():
    task = HTTPTask({"url": "https://api.example.com", "dry_run": True})
    plan = task.plan()
    assert isinstance(plan, list)
    assert plan[0]["action"] == "http_call"

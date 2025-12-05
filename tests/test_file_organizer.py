from agentic_workflows.plugins.file_organizer import normalize_filename, FileOrganizer
from pathlib import Path
import tempfile
import shutil

def test_normalize():
    assert normalize_filename("My File NAME.TXT") == "my_file_name.txt"
    assert normalize_filename("a@b#c!!.pdf") == "abc.pdf"

def test_plan_and_execute(tmp_path):
    # create sample files
    d = tmp_path / "downloads"
    d.mkdir()
    f1 = d / "Hello World.txt"
    f2 = d / "image.PNG"
    f1.write_text("content")
    f2.write_text("imagebytes")
    org = FileOrganizer({"target": str(d), "dry_run": True})
    plan = org.plan()
    assert any(p["action"].startswith("move") for p in plan)

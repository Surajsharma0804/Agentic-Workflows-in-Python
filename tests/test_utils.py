from agentic_workflows.utils.helpers import ensure_dir
import tempfile
from pathlib import Path

def test_ensure_dir(tmp_path):
    p = tmp_path / "x" / "y"
    r = ensure_dir(str(p))
    assert isinstance(r, Path)
    assert r.exists()

from pathlib import Path
from .base import PluginBase
import hashlib
import re

DEFAULT_CATEGORIES = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'},
    'documents': {'.pdf', '.docx', '.doc', '.txt', '.md', '.pptx', '.xlsx'},
    'archives': {'.zip', '.tar', '.gz', '.rar'},
    'media': {'.mp3', '.mp4', '.mkv', '.mov'},
}

def normalize_filename(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9._-]', '', name)
    return name

def file_hash(path: Path, chunk_size: int = 8192) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

class FileOrganizer(PluginBase):
    name = "file_organizer"

    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        
        # Validate and secure target path
        target_str = params.get("target", ".")
        self.target = Path(target_str).expanduser().resolve()
        
        # Security: Ensure target is within allowed directories
        # For FREE tier, restrict to current working directory and subdirectories
        allowed_base = Path.cwd().resolve()
        try:
            self.target.relative_to(allowed_base)
        except ValueError:
            raise ValueError(
                f"Security: Target path must be within {allowed_base}, got {self.target}"
            )
        
        # Validate target exists and is a directory
        if not self.target.exists():
            raise FileNotFoundError(f"Target directory does not exist: {self.target}")
        if not self.target.is_dir():
            raise ValueError(f"Target must be a directory, not a file: {self.target}")
        
        self.categories = params.get("categories", DEFAULT_CATEGORIES)
        self.dry_run = params.get("dry_run", True)
        self.allow_destructive = params.get("allow_destructive", False)

    def _categorize(self, p: Path):
        ext = p.suffix.lower()
        for cat, exts in self.categories.items():
            if ext in exts:
                return cat
        return "others"

    def plan(self):
        actions = []
        if not self.target.exists():
            actions.append({"action": "error", "reason": "target_missing", "target": str(self.target)})
            return actions
        seen = {}
        for p in self.target.iterdir():
            if p.is_file():
                cat = self._categorize(p)
                dest_dir = self.target / cat
                normalized = normalize_filename(p.name)
                dest = dest_dir / normalized
                h = file_hash(p)
                if h in seen:
                    actions.append({"action": "move_to_duplicates", "src": str(p), "dest": str(self.target / "duplicates" / normalized)})
                else:
                    seen[h] = p
                    actions.append({"action": "move", "src": str(p), "dest": str(dest)})
        return actions

    def execute(self):
        import shutil
        plan = self.plan()
        results = []
        for a in plan:
            if a["action"] == "error":
                results.append({"action": a, "status": "failed"})
                continue
            if self.dry_run:
                results.append({"action": a, "status": "planned"})
                continue
            # actual move
            src = Path(a["src"])
            dst = Path(a["dest"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            final = dst
            i = 1
            while final.exists():
                stem = final.stem
                suffix = final.suffix
                final = dst.parent / f"{stem}_{i}{suffix}"
                i += 1
            shutil.move(str(src), str(final))
            results.append({"action": a, "status": "moved", "final": str(final)})
            if self.audit:
                self.audit.record({"plugin": self.name, "action": "moved", "src": str(src), "dst": str(final)})
        return {"status": "ok", "results": results}

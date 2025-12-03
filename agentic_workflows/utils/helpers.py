import logging
from pathlib import Path

def setup_logging(level="INFO"):
    logging.basicConfig(level=getattr(logging, level), format="%(asctime)s [%(levelname)s] %(message)s")

def ensure_dir(path: str):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

import json
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def read_json(path: str, default=None):
    """Read a JSON file. Return default if missing or corrupted."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("File not found: %s — using default", path)
        return default if default is not None else {}
    except json.JSONDecodeError:
        logger.warning("Corrupted JSON: %s — using default", path)
        return default if default is not None else {}


def write_json(path: str, data):
    """Write JSON atomically: write to temp file then rename."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    dir_name = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise

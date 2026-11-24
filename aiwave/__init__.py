"""AIWave client for supported chat requests and AI video routes."""
from .client import AIWave

# Read the installed distribution metadata instead of repeating the number here.
# A literal in this file drifted two releases behind pyproject.toml and shipped
# 0.2.0 inside the 0.2.1 wheel; deriving it makes that impossible.
from pathlib import Path as _Path

def _read_version():
    """Version from pyproject.toml when present, else from installed metadata.

    The source file wins on purpose. A hosted notebook or a developer checkout
    next to an older pip-installed copy would otherwise report the stale
    installed number instead of the code actually being imported.
    """
    pyproject = _Path(__file__).resolve().parent.parent / "pyproject.toml"
    try:
        import re as _re
        match = _re.search(
            r'^version\s*=\s*"([^"]+)"',
            pyproject.read_text(encoding="utf-8"),
            _re.MULTILINE,
        )
        if match:
            return match.group(1)
    except OSError:                     # wheel install: no pyproject alongside
        pass
    try:
        from importlib.metadata import version as _v
        return _v("aiwave")
    except Exception:                   # pragma: no cover - last resort
        return "0.2.2"

__version__ = _read_version()

__all__ = ["AIWave"]

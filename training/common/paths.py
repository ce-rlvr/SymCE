from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_path(*parts: str) -> Path:
    """Return an absolute path anchored at the repository root."""
    return REPO_ROOT.joinpath(*parts)

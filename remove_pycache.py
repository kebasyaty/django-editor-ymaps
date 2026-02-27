"""Remove __pycache__ directories."""

from __future__ import annotations

import os
from pathlib import Path
from shutil import rmtree


def remove_pycache(path: str) -> None:
    """Call the function from your project's root directory."""
    print("Start removing __pycache__")  # noqa: T201
    for root, dirs, _ in os.walk(path):
        if "__pycache__" in dirs:
            pycache_path = Path(*(root, "__pycache__"))
            rmtree(pycache_path)
    print("Done")  # noqa: T201


if __name__ == "__main__":
    remove_pycache(".")

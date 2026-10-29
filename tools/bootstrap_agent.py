#!/usr/bin/env python3
"""Idempotent, shell-independent bootstrap of local coding-agent tooling.

Only creates/uses .venv-agent and installs tools/requirements-agent.txt.
No source code, npm packages, Lerd services, or databases are changed.
"""
from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv-agent"
PYTHON = VENV / "bin" / "python"
REQUIREMENTS = ROOT / "tools" / "requirements-agent.txt"


def execute(arguments: list[str]) -> None:
    print("+ " + " ".join(arguments), flush=True)
    completed = subprocess.run(arguments, cwd=ROOT, check=False)
    if completed.returncode:
        raise RuntimeError(
            f"Command exited with code {completed.returncode}. "
            "Do not modify system Python, disable security, or falsely mark a task complete."
        )


def dependencies_ready() -> bool:
    if not PYTHON.is_file():
        return False
    check = (
        "import importlib.metadata, yaml; "
        "version=importlib.metadata.version('PyYAML'); "
        "major,minor=map(int,version.split('.')[:2]); "
        "assert (major, minor) >= (6, 0) and major < 7, version"
    )
    return subprocess.run(
        [str(PYTHON), "-c", check], cwd=ROOT, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=False
    ).returncode == 0


def main() -> int:
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ is required for agent tooling.", file=sys.stderr)
        return 1
    if not REQUIREMENTS.is_file():
        print("ERROR: Missing tools/requirements-agent.txt.", file=sys.stderr)
        return 1
    if VENV.is_symlink():
        print("ERROR: Refusing symlinked .venv-agent directory.", file=sys.stderr)
        return 1

    try:
        if not PYTHON.is_file():
            if VENV.exists() and any(VENV.iterdir()):
                raise RuntimeError(
                    ".venv-agent exists but has no usable Python interpreter. "
                    "Inspect it; do not delete or overwrite an unknown directory automatically."
                )
            execute([sys.executable, "-m", "venv", str(VENV)])
        if not dependencies_ready():
            # Install into the local venv only, never via the system Python pip.
            execute([str(PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS)])
        if not dependencies_ready():
            raise RuntimeError("PyYAML requirements are not importable from .venv-agent.")
        print("Agent Python environment ready:", PYTHON.relative_to(ROOT), flush=True)
        # All are read-only checks; leave TASKS.yaml and checkpoint unchanged.
        for tool, args in (
            ("validate_plan.py", []),
            ("check_repo_contracts.py", []),
            ("agent_tasks.py", ["doctor"]),
            ("agent_tasks.py", ["next"]),
            ("agent_tasks.py", ["summary"]),
        ):
            execute([str(PYTHON), str(ROOT / "tools" / tool), *args])
    except (OSError, RuntimeError) as error:
        print("AGENT BOOTSTRAP BLOCKED:", error, file=sys.stderr)
        print(
            "Record the failure for the user. Do not claim P00 started or completed; "
            "do not use --break-system-packages or modify Lerd globally.",
            file=sys.stderr,
        )
        return 1
    print("Bootstrap checks passed. Continue from the next/resume task shown above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

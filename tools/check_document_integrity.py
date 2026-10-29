#!/usr/bin/env python3
"""Reject missing-file tool messages, placeholder bodies and truncated project Markdown.

Read-only: scans root Markdown and docs/**/*.md, ignoring virtual environments/build output.
This is a structural document check, not a review of requirement correctness.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    "docs/PRD.md": (2500, ("PRD-01", "PRD-03", "PRD-05", "PRD-07", "PRD-09", "AUTH-REQ-01", "RBAC-REQ-02", "CMS-REQ-01")),
    "docs/TRD.md": (2500, ("TRD-01",)),
    "docs/AFD.md": (2000, ("AFD-01",)),
    "docs/DBD.md": (2000, ("DBD-01",)),
    "docs/BSD.md": (4000, ("BSD-01",)),
    "docs/IPD.md": (2000, ("IPD-01",)),
}
# These are common AI/connector failure responses that must never replace an artifact.
BAD_TEXT = (
    re.compile(r"the requested file reference is not currently visible", re.I),
    re.compile(r"use files[.]search or files[.]list to rediscover", re.I),
    re.compile(r"retry with a returned ref_id or file_id", re.I),
    re.compile(r"file(?: reference)? (?:is )?not currently visible", re.I),
    re.compile(r"unable to (?:retrieve|access|load) (?:the )?(?:file|document) reference", re.I),
    re.compile(r"no (?:such )?file(?: or directory)?[.]?\s*$", re.I),
)


def invalid_reasons(path: str, body: str) -> list[str]:
    issues = []
    if not body.strip():
        issues.append("empty Markdown")
        return issues
    if not re.search(r"(?m)^#\s+\S", body):
        issues.append("missing primary H1 Markdown heading")
    for rule in BAD_TEXT:
        if rule.search(body):
            issues.append("contains a file-access failure message")
            break
    if path in CORE:
        min_chars, required = CORE[path]
        if len(body) < min_chars:
            issues.append(f"critical specification too short: {len(body)} < {min_chars} characters")
        missing = [item for item in required if item not in body]
        if missing:
            issues.append("missing critical requirement sections/IDs: " + ", ".join(missing))
    elif path.startswith("docs/agent/tasks/") and len(body.strip()) < 400:
        issues.append("task card unexpectedly short")
    return issues


def scan_documentation(root: Path = ROOT) -> tuple[int, list[str]]:
    paths = list(root.glob("*.md")) + list((root / "docs").rglob("*.md"))
    errors = []
    for file in sorted(set(paths)):
        relative = file.relative_to(root).as_posix()
        if any(part in (".venv-agent", "node_modules", ".git", ".next", "dist", "build") for part in file.parts):
            continue
        try:
            body = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative}: unreadable file ({type(error).__name__})")
            continue
        for issue in invalid_reasons(relative, body):
            errors.append(f"{relative}: {issue}")
    for name in CORE:
        if not (root / name).is_file():
            errors.append(f"{name}: missing critical document")
    return len(paths), errors


def main() -> int:
    checked, issues = scan_documentation()
    for issue in issues:
        print("ERROR:", issue)
    if issues:
        print(f"FAILED: {len(issues)} integrity issues across {checked} Markdown files.")
        return 1
    print(f"OK: {checked} Markdown documents checked; no file-reference errors or truncated core specs.")
    print("This does not replace product/technical review or application testing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Small non-destructive checks of task tooling against repository registry."""
import pathlib, subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
for command in ([sys.executable,"tools/validate_plan.py"],[sys.executable,"tools/agent_tasks.py","doctor"],[sys.executable,"tools/agent_tasks.py","next"]):
 r=subprocess.run(command,cwd=ROOT)
 if r.returncode:sys.exit(r.returncode)
print("Agent tooling smoke checks passed (no implementation features tested).")

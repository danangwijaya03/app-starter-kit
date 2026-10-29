#!/usr/bin/env python3
"""Small non-destructive checks of task tooling against repository registry."""
import pathlib, subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
for command in ([sys.executable,"tools/validate_plan.py"],[sys.executable,"tools/agent_tasks.py","doctor"],[sys.executable,"tools/agent_tasks.py","next"]):
 r=subprocess.run(command,cwd=ROOT)
 if r.returncode:sys.exit(r.returncode)
print("Agent tooling smoke checks passed (no implementation features tested).")

# Evidence invalidation sanity check: an untracked source edit must change the fingerprint.
import importlib.util
spec=importlib.util.spec_from_file_location('agent_tasks', ROOT/'tools/agent_tasks.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
baseline=module.source_fingerprint()
probe=ROOT/'tools/.agent-fingerprint-probe.tmp'
if probe.exists():sys.exit('Refusing to overwrite existing fingerprint probe')
try:
 probe.write_text('temporary code change for fingerprint test',encoding='utf-8')
 if module.source_fingerprint()==baseline:sys.exit('Source fingerprint failed to detect new file')
finally:
 probe.unlink(missing_ok=True)
if module.source_fingerprint()!=baseline:sys.exit('Source fingerprint did not recover after cleanup')
print('Source fingerprint invalidation check passed')

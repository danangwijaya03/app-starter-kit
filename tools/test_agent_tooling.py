#!/usr/bin/env python3
"""Isolated non-destructive smoke tests for task CLI, risk gates, splitting and reporting."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
def call(*args,cwd=ROOT,ok=True):
 p=subprocess.run(list(args),cwd=cwd,text=True,capture_output=True)
 if ok and p.returncode!=0:raise AssertionError(str(args)+" failed: "+p.stdout+"\n"+p.stderr)
 if not ok and p.returncode==0:raise AssertionError(str(args)+" unexpectedly succeeded")
 return p

for cmd in ([sys.executable,"tools/validate_plan.py"],
            [sys.executable,"tools/check_repo_contracts.py"],
            [sys.executable,"tools/agent_tasks.py","doctor"],
            [sys.executable,"tools/agent_tasks.py","next"]):
 call(*cmd)
summary=json.loads(call(sys.executable,"tools/agent_tasks.py","summary","--json").stdout)
assert summary["total"]==sum(p["total"] for p in summary["phases"])
assert len(summary["phases"])==17

# Build a completely separate git repo; never touch actual TASKS.yaml or Lerd data.
with tempfile.TemporaryDirectory(prefix="agent-tooling-") as tmp:
 temp=Path(tmp)
 (temp/"tools").mkdir()
 (temp/"docs/agent/tasks").mkdir(parents=True)
 (temp/"docs/agent/phases").mkdir(parents=True)
 shutil.copy2(ROOT/"tools/agent_tasks.py",temp/"tools/agent_tasks.py")
 shutil.copy2(ROOT/"tools/split_agent_task.py",temp/"tools/split_agent_task.py")
 (temp/"tools/check_scenario.py").write_text(
  "import sys\nassert '--case' in sys.argv\nassert sys.argv[-1] in ('good','denied')\n",encoding="utf-8")
 call("git","init","-q",cwd=temp)
 data={"metadata":{"task_count":2},"tasks":[
  {"id":"P00-01","phase":"P00","title":"Document baseline","status":"pending",
   "depends_on":[],"card":"docs/agent/tasks/P00-01.md","scope":["docs"],
   "steps":["Record baseline"],"acceptance_criteria":["Document exists"],"validation":["Check docs"],
   "risk":"low","output_artifact":"docs/baseline.md","tests_evidence":[]},
  {"id":"P04-01","phase":"P04","title":"Authentication security check","status":"pending",
   "depends_on":[],"card":"docs/agent/tasks/P04-01.md","scope":["tests"],
   "steps":["Test auth"],"acceptance_criteria":["Auth secure"],"validation":["Check tests"],
   "risk":"low","output_artifact":"tests/auth.test.ts","tests_evidence":[]}]}
 (temp/"docs/agent/TASKS.yaml").write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")
 (temp/"docs/agent/tasks/P00-01.md").write_text("# P00-01\n",encoding="utf-8")
 (temp/"docs/agent/tasks/P04-01.md").write_text("# P04-01\n",encoding="utf-8")
 (temp/"docs/agent/PHASES.md").write_text("| [P00](phases/P00-test.md) | 1 |\n**Total predefined atomic tasks:** 2\n",encoding="utf-8")
 (temp/"docs/agent/phases/P00-test.md").write_text("# P00\n",encoding="utf-8")
 cli=[sys.executable,"tools/agent_tasks.py"]
 assert json.loads(call(*cli,"summary","--json",cwd=temp).stdout)["total"]==2
 call(*cli,"start","P04-01",cwd=temp)
 call(*cli,"run","P04-01","--kind","integration","--","python3","tools/check_scenario.py","--case","good",cwd=temp)
 call(*cli,"complete","P04-01",cwd=temp,ok=False) # Negative evidence + independent review missing
 call(*cli,"run","P04-01","--kind","negative","--","python3","tools/check_scenario.py","--case","denied",cwd=temp)
 call(*cli,"complete","P04-01",cwd=temp,ok=False) # Review still missing
 review=temp/"docs/agent/reviews/P04-01.md"
 review.parent.mkdir(parents=True)
 review.write_text("TASK: P04-01\nDECISION: APPROVED\nReviewer: independent tester\n"
  "Reviewed actual positive and negative assertions, state change, and authentication failure handling. "
  "No credentials or user data were used in these disposable tests.\n",encoding="utf-8")
 call(*cli,"review","P04-01","--reviewer","independent tester","--evidence","docs/agent/reviews/P04-01.md",cwd=temp)
 # A new source edit invalidates test AND review.
 (temp/"tools/check_scenario.py").write_text("import sys\nassert '--case' in sys.argv\nassert sys.argv[-1] in ('good','denied')\n# new edit\n",encoding="utf-8")
 call(*cli,"complete","P04-01",cwd=temp,ok=False)
 for kind,case in (("integration","good"),("negative","denied")):
  call(*cli,"run","P04-01","--kind",kind,"--","python3","tools/check_scenario.py","--case",case,cwd=temp)
 call(*cli,"review","P04-01","--reviewer","independent tester","--evidence","docs/agent/reviews/P04-01.md",cwd=temp)
 call(*cli,"complete","P04-01",cwd=temp)
 plan={"children":[
  {"title":"Create baseline","scope":["docs/base.md"],"steps":["Write doc"],
   "output_artifact":"docs/base.md","acceptance_criteria":["Doc present"],
   "test_cases":{"positive":["Doc exists"],"negative":["Missing doc fails"]}},
  {"title":"Link baseline","scope":["docs/index.md"],"steps":["Link doc"],
   "output_artifact":"docs/index.md","acceptance_criteria":["Link valid"],
   "test_cases":{"positive":["Valid reference"],"negative":["Broken reference rejected"]}}
 ]}
 (temp/"plan.json").write_text(json.dumps(plan),encoding="utf-8")
 call(*cli,"split","P00-01","--plan","plan.json",cwd=temp)
 new=yaml.safe_load((temp/"docs/agent/TASKS.yaml").read_text())
 assert new["metadata"]["task_count"]==4
 parent=next(t for t in new["tasks"] if t["id"]=="P00-01")
 assert parent["depends_on"]==["P00-01-S02"]
 assert (temp/"docs/agent/tasks/P00-01-S01.md").exists()
 call(*cli,"start","P00-01",cwd=temp,ok=False) # Parent remains blocked by children.
 call(*cli,"split","P00-01","--plan","plan.json",cwd=temp,ok=False) # No double split.
print("OK: task summary, high-risk evidence+review gate, stale proof, and safe task splitting.")

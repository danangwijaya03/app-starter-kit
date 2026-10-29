#!/usr/bin/env python3
"""Documentation DAG and path verifier. NOT a test of application code."""
from pathlib import Path
import re,sys
try:import yaml
except ImportError:sys.exit("Missing PyYAML: python3 -m pip install -r tools/requirements-agent.txt")
R=Path(__file__).resolve().parents[1]
D=yaml.safe_load((R/"docs/agent/TASKS.yaml").read_text(encoding="utf-8"))
T=D["tasks"];errors=[];ids=[x.get("id") for x in T];m={x["id"]:x for x in T}
if len(T)!=157 or len(ids)!=len(set(ids)):errors.append("Expected 157 unique task IDs")
if D["metadata"].get("task_count")!=157:errors.append("task_count mismatch")
if {x["phase"] for x in T}!={"P"+str(i).zfill(2) for i in range(17)}:errors.append("Missing phase")
for t in T:
 i=t["id"]
 if not re.fullmatch(r"P(?:0[0-9]|1[0-6])-\d{2}[A-Z]?",i):errors.append("Bad ID "+i)
 if not (R/t["card"]).is_file():errors.append("Missing card "+i)
 for dep in t.get("depends_on",[]):
  if dep not in m:errors.append("Missing dependency "+i+" -> "+dep)
  if dep==i:errors.append("Self-dependency "+i)
 for ref in t.get("spec_refs",[]):
  if not (R/ref).is_file():errors.append("Missing spec ref "+i+" -> "+ref)
 if not t.get("output_artifact"):errors.append("Missing output artifact "+i)
 if t["status"] not in ("pending","in_progress","blocked","completed","verified"):errors.append("Bad status "+i)
 if t["status"] in ("completed","verified") and not t.get("tests_evidence"):errors.append("Completed without test evidence "+i)
visited=set();visiting=set()
def scan(i):
 if i in visiting:errors.append("Dependency cycle at "+i);return
 if i in visited:return
 visiting.add(i)
 for dep in m[i].get("depends_on",[]):
  if dep in m:scan(dep)
 visiting.remove(i);visited.add(i)
for i in ids:scan(i)
if len(list((R/"docs/agent/phases").glob("P*.md")))!=17:errors.append("Expected 17 phase files")
for n in ("AGENTS.md","README.md","README-SERVER.md","docs/PRD.md","docs/TRD.md","docs/AFD.md","docs/DBD.md","docs/BSD.md","docs/IPD.md"):
 if not (R/n).is_file():errors.append("Missing "+n)
for path in R.rglob("*.md"):
 s=re.sub(r"```.*?```","",path.read_text(encoding="utf-8"),flags=re.S)
 for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)",s):
  target=target.split("#",1)[0].split(" ",1)[0]
  if not target or target.startswith(("http:","https:","mailto:","/","sandbox:")):continue
  if not (path.parent/target).exists():errors.append("Broken local link "+str(path.relative_to(R))+" -> "+target)
if errors:
 for e in errors[:50]:print("ERROR",e)
 print("Total errors:",len(errors));sys.exit(1)
print("OK: 157 unique tasks, 17 phases, no missing dependencies/cycles, cards and local links valid.")
print("This checks documentation only, not the Next.js app build or integration behavior.")

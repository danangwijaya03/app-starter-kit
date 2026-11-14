#!/usr/bin/env python3
"""Documentation DAG and path verifier. NOT a test of application code."""
from pathlib import Path
from check_document_integrity import scan_documentation
import re,sys
try:import yaml
except ImportError:sys.exit("Missing PyYAML: python3 -m pip install -r tools/requirements-agent.txt")
R=Path(__file__).resolve().parents[1]
D=yaml.safe_load((R/"docs/agent/TASKS.yaml").read_text(encoding="utf-8"))
T=D["tasks"];errors=[];ids=[x.get("id") for x in T];m={x["id"]:x for x in T}
if not T or len(ids)!=len(set(ids)):errors.append("Missing or duplicate task IDs")
if D["metadata"].get("task_count")!=len(T):errors.append("task_count mismatch; update metadata after splitting tasks")
if D["metadata"].get("canonical_branch")!="main":errors.append("canonical_branch must be main for this approved workflow")
if D["metadata"].get("coding_agent_policy")!="provider_agnostic_one_agent_per_task":errors.append("coding agent policy must remain provider-agnostic")
for key in ("preview_policy","agent_workflow","reference_catalog","manual_setup","review_queue"):
 p=D["metadata"].get(key)
 if not p or not (R/p).is_file():errors.append("Missing delivery policy document "+key)
if {x["phase"] for x in T}!={"P"+str(i).zfill(2) for i in range(17)}:errors.append("Missing phase")
for t in T:
 if t.get("task_complexity") not in ("low","medium","high"):errors.append("Missing/invalid task complexity "+str(t.get("id")))
 if t.get("preview_expectation") not in ("when_reviewable","fixture","diagnostic","integrated"):errors.append("Missing/invalid preview expectation "+str(t.get("id")))
 i=t["id"]
 if not re.fullmatch(r"P(?:0[0-9]|1[0-6])-\d{2}[A-Z]?(?:-S\d{2})?",i):errors.append("Bad ID "+i)
 if not (R/t["card"]).is_file():errors.append("Missing card "+i)
 else:
  card=(R/t["card"]).read_text(encoding="utf-8")
  if "CODING AGENT" not in card:errors.append("Missing agent audience in "+i)
  if t.get("split_from"):
   if "## Positive tests" not in card or "## Negative tests" not in card:errors.append("Missing split child tests "+i)
  elif "## Specific positive/negative test design" not in card or "## Acceptance checklist" not in card:errors.append("Missing acceptance/test design "+i)
 if not t.get("scope") or not t.get("steps") or not t.get("acceptance_criteria"):errors.append("Incomplete task definition "+i)
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
phases=(R/"docs/agent/PHASES.md").read_text(encoding="utf-8")
for n in range(17):
 p="P%02d"%n
 match=re.search(r"\]\(phases/"+p+r"-[^)]+\.md\) \| (\d+) \|",phases)
 expected=sum(t["phase"]==p for t in T)
 if match is None or int(match.group(1))!=expected:errors.append("Phase counter mismatch "+p+" expected "+str(expected))
for path in ("tools/split_agent_task.py","tools/check_repo_contracts.py","docs/agent/TEST-AND-REVIEW-POLICY.md","docs/agent/TASK-SPLITTING.md"):
 if not (R/path).is_file():errors.append("Missing agent optimization "+path)
for n in ("PANDUAN-MULAI-LOW-AGENT.md","docs/DOCUMENTATION-MAP.md","AGENTS.md","README.md","README-SERVER.md","docs/PRD.md","docs/TRD.md","docs/AFD.md","docs/DBD.md","docs/BSD.md","docs/IPD.md","docs/DEVELOPMENT-ROADMAP.md","docs/agent/AGENT-ROUTING.md","docs/agent/PREVIEW-AND-FEEDBACK.md","docs/agent/REVIEW-QUEUE.md","docs/agent/SINGLE-MODEL-WORKFLOW.md","docs/references/REFERENCE-MAP.md","docs/references/ADOPTION-PROTOCOL.md","docs/MANUAL-CLONE-SETUP.md"):
 if not (R/n).is_file():errors.append("Missing "+n)
for path in R.rglob("*.md"):
 if any(part in (".venv-agent", "node_modules", ".git", ".next", "dist", "build") for part in path.relative_to(R).parts):continue
 s=re.sub(r"```.*?```","",path.read_text(encoding="utf-8"),flags=re.S)
 for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)",s):
  target=target.split("#",1)[0].split(" ",1)[0]
  if not target or target.startswith(("http:","https:","mailto:","/","sandbox:")):continue
  if not (path.parent/target).exists():errors.append("Broken local link "+str(path.relative_to(R))+" -> "+target)
# Audience guard: keep operator guide and coding-agent instructions distinct.
for p, audience in (
 ("PANDUAN-MULAI-LOW-AGENT.md","USER"),
 ("AGENTS.md","CODING AGENT"),
 ("docs/agent/LOW-REASONING-RUNBOOK.md","CODING AGENT"),
 ("README-SERVER.md","USER")
):
 path=R/p
 if not path.is_file():continue
 content=path.read_text(encoding="utf-8")
 if "**Ditujukan untuk:" not in content or audience not in content.split("**Ditujukan untuk:",1)[1][:90]:
  errors.append("Missing correct document audience: "+p)
checked_docs,content_errors=scan_documentation()
errors.extend(content_errors)
if errors:
 for e in errors[:50]:print("ERROR",e)
 print("Total errors:",len(errors));sys.exit(1)
print(f"OK: {len(T)} unique tasks, 17 phases, no missing dependencies/cycles, cards and local links valid.")
print("This checks documentation only, not the Next.js app build or integration behavior.")

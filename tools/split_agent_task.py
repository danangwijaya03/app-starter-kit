#!/usr/bin/env python3
"""Split a PENDING task into bounded children and retain its ID as integration checkpoint.

Run only with a reviewed JSON plan. No code or database changes are performed here.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"docs/agent/TASKS.yaml"
CARD=ROOT/"docs/agent/tasks"
ID_RE=re.compile(r"^P(?:0[0-9]|1[0-6])-\d{2}[A-Z]?$")
def fail(message):sys.exit(message)
def atomic(path,body):
 temp=path.with_suffix(path.suffix+".tmp")
 temp.write_text(body,encoding="utf-8")
 os.replace(temp,path)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("parent")
 p.add_argument("--plan",required=True,help="JSON file describing 2-9 child tasks; see TASK-SPLITTING.md")
 x=p.parse_args()
 if not ID_RE.fullmatch(x.parent):fail("Use a valid original task ID; children cannot be split again automatically.")
 data=yaml.safe_load(REG.read_text(encoding="utf-8"))
 tasks=data["tasks"]
 lookup={t["id"]:t for t in tasks}
 parent=lookup.get(x.parent)
 if not parent or parent["status"]!="pending":fail("Parent must exist and be PENDING (split before starting implementation).")
 if parent.get("split_children"):fail("Parent has already been split.")
 try:plan=json.loads(Path(x.plan).read_text(encoding="utf-8"))
 except (OSError,ValueError):fail("Cannot read valid JSON plan.")
 children=plan.get("children",[])
 if not isinstance(children,list) or not 2<=len(children)<=9:fail("Use 2-9 child definitions.")
 new=[];created=[]
 for index,c in enumerate(children,1):
  if not isinstance(c,dict) or any(not c.get(k) for k in ("title","scope","steps","output_artifact","acceptance_criteria","test_cases")):
   fail("Missing child: title/scope/steps/output_artifact/acceptance_criteria/test_cases")
  if any(not isinstance(c[k],list) or not all(isinstance(v,str) and v.strip() for v in c[k]) for k in ("scope","steps","acceptance_criteria")):
   fail("scope/steps/acceptance_criteria must contain nonempty strings.")
  cases=c["test_cases"]
  if not isinstance(cases,dict) or any(not isinstance(cases.get(k),list) or not cases[k] for k in ("positive","negative")):
   fail("Each child must have positive and negative test scenarios.")
  tid=x.parent+"-S%02d"%index
  if tid in lookup or (CARD/(tid+".md")).exists():fail("Child ID/card collision: "+tid)
  t={k:v for k,v in parent.items() if k not in ("status","tests_evidence","completed_commit","blocked_reason","review_record","started_at_utc","depends_on")}
  t.update({"id":tid,"title":c["title"],"scope":c["scope"],"steps":c["steps"],"acceptance_criteria":c["acceptance_criteria"],
     "validation":["Run real positive and negative focused tests"],"output_artifact":c["output_artifact"],"test_cases":cases,
     "depends_on":list(parent["depends_on"]) if not new else [new[-1]["id"]],"status":"pending",
     "tests_evidence":[],"completed_commit":None,"blocked_reason":None,"split_from":x.parent,"card":"docs/agent/tasks/"+tid+".md"})
  new.append(t)
  lines=["# "+tid+" — "+c["title"],"","**Ditujukan untuk: CODING AGENT.** Split child of "+x.parent+".",
      "","## Exact scope",*[("- "+v) for v in c["scope"]],"","## Steps",*[(str(i)+". "+v) for i,v in enumerate(c["steps"],1)],
      "","## Output","- "+c["output_artifact"],"","## Acceptance",*[("- "+v) for v in c["acceptance_criteria"]],
      "","## Positive tests",*[("- "+v) for v in cases["positive"]],"","## Negative tests",*[("- "+v) for v in cases["negative"]],
      "","Run the available relevant tests after final changes; record evidence using agent_tasks.py run --kind. Review risk before complete."]
  created.append((CARD/(tid+".md"),"\n".join(lines)+"\n"))
 parent["depends_on"]=[new[-1]["id"]]
 parent["split_children"]=[t["id"] for t in new]
 # Parent retains original acceptance criteria; it is the final integration checkpoint.
 idx=tasks.index(parent);tasks[idx:idx]=new
 data["metadata"]["task_count"]=len(tasks)
 doc=ROOT/parent["card"]
 if not doc.exists():fail("Original parent card missing.")
 old=doc.read_text(encoding="utf-8")
 note=("\n> **SPLIT:** This parent is now the integration checkpoint. Finish "+
  ", ".join(t["id"] for t in new)+" first; validate aggregate acceptance. Old steps below are historical.\n")
 changed_card=old.replace("\n",note+"\n",1)
 # Prepare documentation counters (do not mutate any state until all inputs validate).
 phase=parent["phase"]
 phases=ROOT/"docs/agent/PHASES.md"
 phase_body=phases.read_text(encoding="utf-8")
 regex=re.compile(r"(\]\(phases/"+re.escape(phase)+r"-[^)]+\.md\) \| )\d+( \|)")
 if not regex.search(phase_body):fail("Cannot find phase counter.")
 count=sum(t["phase"]==phase for t in tasks)
 phase_body=regex.sub(lambda m:m.group(1)+str(count)+m.group(2),phase_body,count=1)
 phase_body=re.sub(r"(\*\*Total predefined atomic tasks:\*\* )\d+",lambda m:m.group(1)+str(len(tasks)),phase_body)
 guide_dir=ROOT/"docs/agent/phases"
 found=list(guide_dir.glob(phase+"-*.md"))
 if len(found)!=1:fail("Expected exactly one phase guide.")
 guide=found[0];guide_body=guide.read_text(encoding="utf-8")
 guide_body+="\n## Additional split for "+x.parent+"\n\n"+"\n".join("- ["+t["id"]+"](../tasks/"+t["id"]+".md)" for t in new)+"\n"
 # Persist the reviewed child plan first, then parent + registry. On interruption, inspect Git.
 for path,body in created:atomic(path,body)
 atomic(doc,changed_card)
 atomic(phases,phase_body)
 atomic(guide,guide_body)
 atomic(REG,yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=110))
 print("SPLIT",x.parent,"->",", ".join(t["id"] for t in new),"| tasks:",len(tasks))
 print("Run python3 tools/validate_plan.py and inspect git diff before continuing.")
if __name__=="__main__":main()

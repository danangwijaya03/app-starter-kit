#!/usr/bin/env python3
"""Agent task selector and checkpoint runner. Does not replace real software tests."""
import argparse, datetime as dt, hashlib, json, os, pathlib, re, subprocess, sys
try:
 import yaml
except ImportError: sys.exit("Install PyYAML: python3 -m pip install -r tools/requirements-agent.txt")
ROOT=pathlib.Path(__file__).resolve().parents[1]
REG=ROOT/"docs/agent/TASKS.yaml"; CHECK=ROOT/"docs/agent/CHECKPOINT.md"; EVID=ROOT/"docs/agent/evidence"
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
def read():
 d=yaml.safe_load(REG.read_text(encoding="utf-8"))
 return d, {x["id"]:x for x in d["tasks"]}
def write(data):
 tmp=REG.with_suffix(".yaml.tmp")
 tmp.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=105),encoding="utf-8")
 os.replace(tmp,REG)
def git(*args):
 p=subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True)
 return p.stdout.strip() if p.returncode==0 else "unavailable"
def source_fingerprint():
 """Hash tracked and untracked project files, excluding task state/evidence and generated outputs.
 The fingerprint makes a successful test invalid after any source/document edits.
 """
 p=subprocess.run(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT,capture_output=True)
 if p.returncode!=0:sys.exit("Cannot fingerprint repository: git ls-files failed")
 excluded={"docs/agent/TASKS.yaml","docs/agent/CHECKPOINT.md"}
 h=hashlib.sha256()
 for raw in sorted(set(p.stdout.split(b"\0"))):
  if not raw:continue
  rel=os.fsdecode(raw)
  if rel in excluded or (rel.startswith("docs/agent/evidence/") or rel.startswith("docs/agent/reviews/")):continue
  file=ROOT/rel
  if not file.is_file() or file.is_symlink():continue
  h.update(raw+b"\0")
  with file.open("rb") as stream:
   while True:
    chunk=stream.read(1024*1024)
    if not chunk:break
    h.update(chunk)
 return h.hexdigest()

RISK_HIGH_PHASES={"P04","P05","P14","P15","P16"}
RISK_WORDS=re.compile(r"auth|session|password|credential|rbac|role|permission|super.?admin|privilege|migrat|backup|restore|recover|release|deploy|rollback|bootstrap|publish",re.I)
KINDS={"docs","unit","integration","negative","build"}
def effective_risk(t):
 levels={"low":0,"medium":1,"high":2,"critical":2}
 level=levels.get(t.get("risk","low"),0)
 if t["phase"] in RISK_HIGH_PHASES or RISK_WORDS.search(t.get("title","")):level=max(level,2)
 elif t["phase"] in ("P03","P07","P09","P10","P11","P12","P13"):level=max(level,1)
 return ("low","medium","high")[level]
def summary(d,m,as_json=False):
 phases=[]
 for n in range(17):
  p="P%02d"%n;ts=[t for t in d["tasks"] if t["phase"]==p]
  obj={"phase":p,"total":len(ts),"high_risk":sum(effective_risk(t)=="high" for t in ts)}
  obj.update({st:sum(t["status"]==st for t in ts) for st in ("pending","in_progress","blocked","completed","verified")})
  phases.append(obj)
 completed=sum(t["status"] in ("completed","verified") for t in d["tasks"])
 result={"total":len(m),"completed":completed,"percent":round(100*completed/max(len(m),1),1),
  "active":[t["id"] for t in d["tasks"] if t["status"]=="in_progress"],
  "blocked":[t["id"] for t in d["tasks"] if t["status"]=="blocked"],
  "ready":[t["id"] for t in d["tasks"] if ready(t,m)],"phases":phases}
 if as_json:print(json.dumps(result,indent=2))
 else:
  print("Tasks %s/%s (%s%%) | active=%s | next=%s | blocked=%s"%(completed,len(m),result["percent"],result["active"],result["ready"][0] if result["ready"] else "-",len(result["blocked"])))
  print("PHASE TOTAL PENDING ACTIVE BLOCKED DONE VERIFIED HIGH")
  for p in phases:print("%s %s %s %s %s %s %s %s"%(p["phase"],p["total"],p["pending"],p["in_progress"],p["blocked"],p["completed"],p["verified"],p["high_risk"]))
 return result
def current_proofs(t):
 current=source_fingerprint();out=[]
 for file in t.get("tests_evidence",[]):
  try:v=json.loads((ROOT/file).read_text(encoding="utf-8"))
  except (OSError,ValueError):continue
  if v.get("task_id")==t["id"] and v.get("exit_code")==0 and v.get("source_fingerprint")==current:out.append(v)
 return out
def required_kinds(t):
 if t["phase"]=="P00":return [{"docs"}]
 if effective_risk(t)=="high":return [{"integration"},{"negative"}]
 if t["phase"] in ("P01","P06","P08"):return [{"unit","integration","build"}]
 return [{"unit","integration"}]
def check_proofs(t):
 kinds={v.get("kind") for v in current_proofs(t)}
 missing=["/".join(sorted(opts)) for opts in required_kinds(t) if not kinds.intersection(opts)]
 if missing:sys.exit("Missing current passing test evidence types: "+", ".join(missing))
def check_review(t):
 if effective_risk(t)!="high":return
 path=t.get("review_record")
 if not path:sys.exit("Independent review required for high-risk task; see TEST-AND-REVIEW-POLICY.md")
 try:v=json.loads((ROOT/path).read_text(encoding="utf-8"))
 except (OSError,ValueError):sys.exit("Missing or malformed review record")
 if v.get("task_id")!=t["id"] or v.get("decision")!="APPROVED" or v.get("fingerprint")!=source_fingerprint():
  sys.exit("High-risk review is stale or invalid; get independent review on current source.")

def ready(t,m): return t["status"]=="pending" and all(m[x]["status"] in ("completed","verified") for x in t.get("depends_on",[]))
def checkpoint(t,note,action):
 text="# Agent checkpoint (tool-managed)\n\n- Updated UTC: "+utc()+"\n- Last action: "+action+"\n- Current task: "+t["id"]+"\n- Status: "+t["status"]+"\n- Git: "+git("rev-parse","--short","HEAD")+"\n- Notes: "+note.replace("\n"," ")[:500]+"\n\n## Working tree\n\n```text\n"+git("status","--short")[:1500]+"\n```\n\n## Resume\nRead AGENTS.md; inspect current Git changes, task card and previous real test evidence. Do not rerun destructive operations blindly.\n"
 CHECK.write_text(text,encoding="utf-8")
def show(t,m):
 print(t["id"],"|",t["title"],"|",t["status"],"| effective-risk:",effective_risk(t))
 print("Depends:",", ".join(x+"="+m[x]["status"] for x in t.get("depends_on",[])) or "(none)")
 print("Card:",t.get("card"))
 print("Scope:",t.get("scope"));print("Output:",t.get("output_artifact"))
 print("Evidence:",t.get("tests_evidence",[]))
 for s in t.get("steps",[]):print(" STEP:",s)
 if t.get("blocked_reason"):print("BLOCKED:",t["blocked_reason"])
def is_safe_command(cmd):
 if not cmd or cmd[0] not in ("npm","npx","node","python3","python","pytest"):return False
 if any(arg in cmd for arg in ("--pass-with-no-tests","--passWithNoTests")):return False
 # A validation wrapper is NOT a sandbox; reject obvious arbitrary-eval and misleading no-test modes.
 if any(flag in cmd for flag in ("-e","--eval","-c","--require","--import","--passWithNoTests","--pass-with-no-tests")):return False
 if cmd[0]=="npx" and "--no-install" not in cmd:return False
 s=" ".join(cmd).lower()
 if re.search(r"password|secret|token|database_url|://[^\\s]+:[^\\s]+@",s):return False
 if any(re.search(r"\\b"+w+r"\\b",s) for w in ("restore","migrate","deploy","bootstrap-admin","drop","delete","reset","rm","clean","install","publish")):return False
 return any(x in s for x in ("test","lint","typecheck","build","check","verify","validate_plan.py"))
def run_check(cmd,filename,task=None,phase=None,kind="general"):
 if cmd and cmd[0]=="--":cmd=cmd[1:]
 if kind not in KINDS:sys.exit("Invalid evidence kind")
 if not is_safe_command(cmd):sys.exit("Unsafe or non-validation command: refused. Use only focused test/lint/typecheck/build/verify.")
 before=source_fingerprint()
 try:status=subprocess.run(cmd,cwd=ROOT,timeout=900).returncode
 except (FileNotFoundError,subprocess.TimeoutExpired):status=124
 after=source_fingerprint()
 if before!=after:
  print("Validation modified source; refusing passing evidence.");status=status or 125
 EVID.mkdir(parents=True,exist_ok=True)
 ev={"task_id":task,"phase":phase,"kind":kind,"command":cmd,"exit_code":status,"timestamp_utc":utc(),"git_commit":git("rev-parse","HEAD"),"source_fingerprint":source_fingerprint()}
 target=EVID/filename;target.write_text(json.dumps(ev,indent=2)+"\n",encoding="utf-8")
 print("Evidence:",target.relative_to(ROOT),"exit:",status)
 return status,str(target.relative_to(ROOT))
def main():
 p=argparse.ArgumentParser();a=p.add_subparsers(dest="action",required=True)
 for key in ("doctor","next","ready","validate"):a.add_parser(key)
 z=a.add_parser("split");z.add_argument("id");z.add_argument("--plan",required=True)
 z=a.add_parser("summary");z.add_argument("--json",action="store_true")
 for key in ("show","start","complete","progress","block","unblock","run","review"):
  q=a.add_parser(key);q.add_argument("id")
  if key in ("complete","progress","block","unblock"):q.add_argument("--note",default="")
  if key=="block":q.add_argument("--reason",required=True)
  if key=="run":
   q.add_argument("--kind",choices=sorted(KINDS),required=True)
  if key=="review":
   q.add_argument("--reviewer",required=True);q.add_argument("--evidence",required=True)
 for key in ("gate","gate-run"):
  q=a.add_parser(key);q.add_argument("phase")
  if key=="gate":q.add_argument("--note",default="")
  if key=="gate-run":
   q.add_argument("--kind",choices=sorted(KINDS),required=True)
 x,unused=p.parse_known_args()
 if x.action in ("run","gate-run"):
  x.command=unused
 elif unused:sys.exit("Unexpected arguments: "+repr(unused))
 d,m=read()
 if x.action=="validate":sys.exit(subprocess.run([sys.executable,str(ROOT/"tools/validate_plan.py")],cwd=ROOT).returncode)
 if x.action=="summary":summary(d,m,x.json);return
 if x.action=="split":sys.exit(subprocess.run([sys.executable,str(ROOT/"tools/split_agent_task.py"),x.id,"--plan",x.plan],cwd=ROOT).returncode)
 active=[t for t in d["tasks"] if t["status"]=="in_progress"]
 possible=[t for t in d["tasks"] if ready(t,m)]
 if x.action=="doctor":
  summary(d,m)
  print("Inspect actual repository files; task registry is authoritative. Git:",git("status","--short")[:800])
  print("RESUME:" if active else "NEXT:",active[0]["id"] if active else possible[0]["id"] if possible else "(none)");return
 if x.action=="ready":
  for t in possible:print(t["id"],t["title"])
  return
 if x.action=="next":
  if active:print("RESUME IN-PROGRESS TASK FIRST");show(active[0],m)
  elif possible:show(possible[0],m)
  else:print("No ready tasks; check blockers and phase gates.")
  return
 if x.action in ("gate","gate-run"):
  pp=x.phase.upper();tasks=[t for t in d["tasks"] if t["phase"]==pp]
  if not tasks:sys.exit("Unknown phase "+pp)
  if any(t["status"]!="completed" for t in tasks):sys.exit("Phase gate requires every task completed.")
  if x.action=="gate-run":
   if pp=="P00" and x.kind!="docs":sys.exit("P00 gate must use docs validation.")
   if pp!="P00" and x.kind=="docs":sys.exit("Documentation validation is not an application phase gate.")
   sys.exit(run_check(x.command,pp+"-gate-"+x.kind+".json",phase=pp,kind=x.kind)[0])
  current=source_fingerprint()
  kinds=set()
  for file in EVID.glob(pp+"-gate-*.json"):
   try:v=json.loads(file.read_text(encoding="utf-8"))
   except (OSError,ValueError):continue
   if v.get("exit_code")==0 and v.get("phase")==pp and v.get("source_fingerprint")==current:kinds.add(v.get("kind"))
  if pp in RISK_HIGH_PHASES and not {"integration","negative"}.issubset(kinds):
   sys.exit("High-risk phase gate requires CURRENT integration and negative evidence.")
  if pp=="P00" and "docs" not in kinds:sys.exit("P00 gate needs current docs evidence.")
  if pp not in RISK_HIGH_PHASES and pp!="P00" and not (kinds & {"unit","integration","build"}):
   sys.exit("Missing current application phase gate evidence.")
  if any(not t.get("tests_evidence") for t in tasks):sys.exit("Each task requires evidence.")
  for t in tasks:
   if effective_risk(t)=="high" and not t.get("review_record"):sys.exit("Phase contains unreviewed high-risk task.")
  for t in tasks:t["status"]="verified"
  write(d);checkpoint(tasks[-1],x.note,"phase-gate");print("Phase verified:",pp);return
 t=m.get(x.id)
 if t is None:sys.exit("Unknown task "+x.id)
 if x.action=="show":show(t,m);return
 if x.action=="start":
  if active:sys.exit("One active task at a time; resume "+active[0]["id"])
  if not ready(t,m):sys.exit("Task dependency not ready")
  t["status"]="in_progress";t["blocked_reason"]=None;t["started_at_utc"]=utc()
 elif x.action=="progress":
  if t["status"]!="in_progress":sys.exit("Task is not in progress")
  checkpoint(t,x.note,"progress");print("Checkpoint updated");return
 elif x.action=="block":
  if t["status"] not in ("in_progress","pending"):sys.exit("Task cannot be blocked")
  t["status"]="blocked";t["blocked_reason"]=x.reason
 elif x.action=="unblock":
  if t["status"]!="blocked":sys.exit("Task is not blocked")
  t["status"]="pending";t["blocked_reason"]=None
 elif x.action=="run":
  if t["status"]!="in_progress":sys.exit("Start task first.")
  rc,path=run_check(x.command,x.id+"-"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S%f")+".json",task=x.id,kind=x.kind)
  if rc==0:t.setdefault("tests_evidence",[]).append(path);write(d)
  sys.exit(rc)
 elif x.action=="review":
  if t["status"]!="in_progress" or effective_risk(t)!="high":sys.exit("Review only in-progress high-risk tasks.")
  path=pathlib.Path(x.evidence)
  if path.is_absolute() or ".." in path.parts or path.parent.as_posix()!="docs/agent/reviews" or path.name!=x.id+".md":sys.exit("Evidence path must be docs/agent/reviews/<ID>.md")
  if not x.reviewer.strip() or x.reviewer.strip().lower() in ("low agent","codex low","self"):sys.exit("Review must come from an independent reviewer.")
  try:content=(ROOT/path).read_text(encoding="utf-8")
  except OSError:sys.exit("Missing independent written review.")
  if "TASK: "+x.id not in content or "DECISION: APPROVED" not in content or len(content.strip())<120:sys.exit("Review note must contain task ID, decision and substantive findings.")
  check_proofs(t)
  record={"task_id":x.id,"decision":"APPROVED","reviewer":x.reviewer.strip(),"evidence":str(path),"fingerprint":source_fingerprint(),"timestamp_utc":utc()}
  location=ROOT/"docs/agent/reviews"/(x.id+".json");location.parent.mkdir(parents=True,exist_ok=True)
  location.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
  t["review_record"]=str(location.relative_to(ROOT));write(d)
  print("Review noted (identity not independently authenticated):",x.id);return
 elif x.action=="complete":
  if t["status"]!="in_progress":sys.exit("Task is not in progress")
  check_proofs(t);check_review(t)
  t["status"]="completed";t["completed_commit"]=git("rev-parse","HEAD")
 else:sys.exit("Unsupported action")
 write(d);checkpoint(t,getattr(x,"note","") or getattr(x,"reason",""),x.action);print(x.action.upper(),x.id)
if __name__=="__main__":main()

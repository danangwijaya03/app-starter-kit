#!/usr/bin/env python3
"""Agent task selector and checkpoint runner. Does not replace real software tests."""
import argparse, datetime as dt, json, os, pathlib, re, subprocess, sys
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
def ready(t,m): return t["status"]=="pending" and all(m[x]["status"] in ("completed","verified") for x in t.get("depends_on",[]))
def checkpoint(t,note,action):
 text="# Agent checkpoint (tool-managed)\n\n- Updated UTC: "+utc()+"\n- Last action: "+action+"\n- Current task: "+t["id"]+"\n- Status: "+t["status"]+"\n- Git: "+git("rev-parse","--short","HEAD")+"\n- Notes: "+note.replace("\n"," ")[:500]+"\n\n## Working tree\n\n```text\n"+git("status","--short")[:1500]+"\n```\n\n## Resume\nRead AGENTS.md; inspect current Git changes, task card and previous real test evidence. Do not rerun destructive operations blindly.\n"
 CHECK.write_text(text,encoding="utf-8")
def show(t,m):
 print(t["id"],"|",t["title"],"|",t["status"])
 print("Depends:",", ".join(x+"="+m[x]["status"] for x in t.get("depends_on",[])) or "(none)")
 print("Card:",t.get("card"))
 print("Scope:",t.get("scope"));print("Output:",t.get("output_artifact"))
 print("Evidence:",t.get("tests_evidence",[]))
 for s in t.get("steps",[]):print(" STEP:",s)
 if t.get("blocked_reason"):print("BLOCKED:",t["blocked_reason"])
def is_safe_command(cmd):
 if not cmd or cmd[0] not in ("npm","npx","node","python3","python","pytest"):return False
 s=" ".join(cmd).lower()
 if re.search(r"password|secret|token|database_url|://[^\\s]+:[^\\s]+@",s):return False
 if any(re.search(r"\\b"+w+r"\\b",s) for w in ("restore","migrate","deploy","bootstrap-admin","drop","delete","reset","rm","clean","install","publish")):return False
 return any(x in s for x in ("test","lint","typecheck","build","check","verify","validate_plan.py"))
def run_check(cmd,filename,task=None,phase=None):
 if cmd and cmd[0]=="--":cmd=cmd[1:]
 if not is_safe_command(cmd):sys.exit("Unsafe or non-validation command: refused. Use only focused test/lint/typecheck/build/verify.")
 try:status=subprocess.run(cmd,cwd=ROOT,timeout=900).returncode
 except (FileNotFoundError,subprocess.TimeoutExpired):status=124
 EVID.mkdir(parents=True,exist_ok=True)
 ev={"task_id":task,"phase":phase,"command":cmd,"exit_code":status,"timestamp_utc":utc(),"git_commit":git("rev-parse","HEAD")}
 target=EVID/filename;target.write_text(json.dumps(ev,indent=2)+"\n",encoding="utf-8")
 print("Evidence:",target.relative_to(ROOT),"exit:",status)
 return status,str(target.relative_to(ROOT))
def main():
 p=argparse.ArgumentParser();a=p.add_subparsers(dest="action",required=True)
 for key in ("doctor","next","ready","validate"):a.add_parser(key)
 for key in ("show","start","complete","progress","block","unblock","run"):
  q=a.add_parser(key);q.add_argument("id")
  if key in ("complete","progress","block","unblock"):q.add_argument("--note",default="")
  if key=="block":q.add_argument("--reason",required=True)
  if key=="run":q.add_argument("command",nargs=argparse.REMAINDER)
 for key in ("gate","gate-run"):
  q=a.add_parser(key);q.add_argument("phase")
  if key=="gate":q.add_argument("--note",default="")
  if key=="gate-run":q.add_argument("command",nargs=argparse.REMAINDER)
 x=p.parse_args();d,m=read()
 if x.action=="validate":sys.exit(subprocess.run([sys.executable,str(ROOT/"tools/validate_plan.py")],cwd=ROOT).returncode)
 active=[t for t in d["tasks"] if t["status"]=="in_progress"]
 possible=[t for t in d["tasks"] if ready(t,m)]
 if x.action=="doctor":
  print("Tasks:",len(m),"active:",len(active),"ready:",len(possible),"completed:",sum(t["status"] in ("completed","verified") for t in m.values()))
  print("Existing Next.js npm root scaffold; future features not yet built. Git:",git("status","--short")[:800])
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
  if x.action=="gate-run":sys.exit(run_check(x.command,pp+"-gate.json",phase=pp)[0])
  file=EVID/(pp+"-gate.json")
  if not file.exists():sys.exit("Missing successful phase gate evidence.")
  v=json.loads(file.read_text())
  if v.get("exit_code")!=0 or v.get("phase")!=pp:sys.exit("Phase gate check failed.")
  if any(not t.get("tests_evidence") for t in tasks):sys.exit("Each task requires evidence.")
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
  rc,path=run_check(x.command,x.id+"-"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")+".json",task=x.id)
  if rc==0:t.setdefault("tests_evidence",[]).append(path);write(d)
  sys.exit(rc)
 elif x.action=="complete":
  if t["status"]!="in_progress":sys.exit("Task is not in progress")
  if not t.get("tests_evidence"):sys.exit("No passing test evidence; cannot complete.")
  if t["phase"]!="P00":
   only_docs=True
   for f in t["tests_evidence"]:
    try:
     v=json.loads((ROOT/f).read_text())
     if "validate_plan.py" not in " ".join(v.get("command",[])):only_docs=False
    except Exception:pass
   if only_docs:sys.exit("Implementation task needs real implementation tests, not only docs graph check.")
  t["status"]="completed";t["completed_commit"]=git("rev-parse","HEAD")
 else:sys.exit("Unsupported action")
 write(d);checkpoint(t,getattr(x,"note","") or getattr(x,"reason",""),x.action);print(x.action.upper(),x.id)
if __name__=="__main__":main()

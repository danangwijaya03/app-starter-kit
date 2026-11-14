# Resume Coding Agent — provider-agnostic

**Ditujukan untuk: CODING AGENT (prompt disalin oleh USER saat sesi baru).**

```text
Lanjutkan app-starter-kit di branch main dari source nyata. Implementer coding agent yang dipilih, arsitektur clone-based tanpa installer. Jangan mengulang pekerjaan tervalidasi atau mengganti stack dengan starter lain.

Baca AGENTS.md, docs/agent/SINGLE-MODEL-WORKFLOW.md, docs/agent/CHECKPOINT.md dan docs/agent/REVIEW-QUEUE.md.
git status --short
git diff
git log -5 --oneline
python3 tools/bootstrap_agent.py
.venv-agent/bin/python tools/agent_tasks.py doctor
.venv-agent/bin/python tools/agent_tasks.py next
.venv-agent/bin/python tools/agent_tasks.py summary

Jika task masih in_progress, lanjut dari file dan evidence nyata; jangan reset. Jika tidak, ambil satu ready task. Baca card + spec_refs dan satu reference playbook (docs/references/REFERENCE-MAP.md) termasuk source/version/license bila adaptasi code.

Gunakan RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT. Uji source terakhir, negative/API/DB test relevan, gunakan database test disposable; jangan ulang migration/bootstrap/restore ke DB nyata tanpa inspeksi dan persetujuan. Independent reviewer diperlukan untuk risiko tinggi, bukan model High Reasoning. Jika unavailable, block task dan teruskan task independen yang aman.

Catat preview URL hanya jika diuji, status fixture/integrated, hasil dan checkpoint; commit unit teruji. No installer, no automated production deployment, no Docker requirement.
```

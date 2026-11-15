# Peta Dokumentasi — Modular Core v2, clone-based reusable starter\n\n**Accepted design / not implemented:** [Unified SPEC](../SPEC-001-app-starter-kit-modular-core.md) · [Architecture](architecture/README.md) · [16 ADRs](architecture/ADR/README.md) · [Reference v2 Index](references/INDEX-V2.md) · [v2 Task Rebase](architecture/TASK-REBASE-PLAN.md). Two Core processes (Web/API), MySQL; optional Redis/worker/Media/CMS/Operations. Core release P16-11, selected module gate P16-12.

## Untuk pengguna dan operator

- [README.md](../README.md): status baseline dan target arsitektur.
- [PANDUAN-MULAI-LOW-AGENT.md](../PANDUAN-MULAI-LOW-AGENT.md): menjalankan coding agent yang dipilih dengan coding agent.
- [MANUAL-CLONE-SETUP.md](MANUAL-CLONE-SETUP.md): membuat proyek baru secara manual.
- [README-SERVER.md](../README-SERVER.md): deployment aaPanel tanpa Docker dan tanpa installer.
- [DEVELOPMENT-ROADMAP.md](DEVELOPMENT-ROADMAP.md): preview pada tiap fase.
- [REVIEW-QUEUE.md](agent/REVIEW-QUEUE.md): status UI feedback.

## Untuk coding agent (coding agent yang dipilih)

- [AGENTS.md](../AGENTS.md): aturan utama.
- [START-AGENT-PROMPT.md](agent/START-AGENT-PROMPT.md) / [RESUME-SESSION-PROMPT.md](agent/RESUME-SESSION-PROMPT.md): prompts.
- [SINGLE-MODEL-WORKFLOW.md](agent/SINGLE-MODEL-WORKFLOW.md): satu implementer + security reviewer terpisah.
- [REFERENCE-MAP.md](references/REFERENCE-MAP.md): daftar referensi fitur dan alternatif.
- [ADOPTION-PROTOCOL.md](references/ADOPTION-PROTOCOL.md): langkah adaptasi yang harus dilalui.
- [PHASES.md](agent/PHASES.md) + [TASKS.yaml](agent/TASKS.yaml) + [tasks/](agent/tasks/) + [CHECKPOINT.md](agent/CHECKPOINT.md): task graph, runbook, bukti.
- [TEST-AND-REVIEW-POLICY.md](agent/TEST-AND-REVIEW-POLICY.md): tes dan independent review.
- [IMPLEMENTATION-CONTRACTS.md](agent/IMPLEMENTATION-CONTRACTS.md): batas arsitektur.

## Spesifikasi

[PRD](PRD.md) (produk) · [TRD](TRD.md) (teknis) · [AFD](AFD.md) (flow) · [DBD](DBD.md) (UI) · [BSD](BSD.md) (schema/API) · [IPD](IPD.md) (tahapan).

[Architecture References](architecture/REFERENCES.md) dan [Traceability](architecture/TRACEABILITY.md) adalah indeks ringkas. Referensi yang bukan requirement MUST tidak menambah scope secara otomatis.

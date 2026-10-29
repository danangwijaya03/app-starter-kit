# Resume Coding Agent — Low Reasoning

**Ditujukan untuk: CODING AGENT (prompt disalin oleh USER saat sesi baru).**

```text
Lanjutkan app-starter-kit dari keadaan repository yang sebenarnya. JANGAN mengulang task yang sudah tervalidasi.

Baca AGENTS.md dan docs/agent/LOW-REASONING-RUNBOOK.md. Dari root repository, jalankan bootstrap idempotent terlebih dahulu:
python3 tools/bootstrap_agent.py

Gunakan .venv-agent/bin/python untuk semua task CLI; jangan source activate (Fish/Bash/Zsh tidak diperlukan). Bila bootstrap gagal, laporkan blocker dan jangan memulai task. Sesudah sukses, periksa:
git status --short
git diff
git log -5 --oneline
docs/agent/CHECKPOINT.md
.venv-agent/bin/python tools/agent_tasks.py doctor
.venv-agent/bin/python tools/agent_tasks.py next
.venv-agent/bin/python tools/agent_tasks.py summary

Jika task in_progress, cocokkan file berubah, source fingerprint dan evidence sebelum editing. Jika tidak ada, ambil satu task ready. Baca hanya card aktif dan referensi terkait.

Jangan mengulang migration/seed/bootstrap/restore atau menghapus data tanpa pengecekan state, lingkungan, dan otorisasi. Gunakan npm/npx dan Lerd Node 26; test harus menggunakan DB khusus test. Periksa jenis bukti tes dan catatan reviewer task high-risk sesuai docs/agent/TEST-AND-REVIEW-POLICY.md; persetujuan lama menjadi tidak sah bila source berubah. Jalankan pemeriksaan konsistensi repo setelah mengubah script/dokumentasi.

Jalankan tes nyata setelah edit terakhir, catat complete/progress/block dengan CLI. Lanjutkan otomatis jika aman, atau checkpoint saat limit mendekat.
```

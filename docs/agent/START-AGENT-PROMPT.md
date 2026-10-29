# Start Coding Agent — Low Reasoning

**Ditujukan untuk: CODING AGENT (prompt disalin oleh USER).**

```text
Mulai implementasi app-starter-kit pada repository yang SUDAH ADA.

Baca AGENTS.md sebagai instruksi utama dan docs/agent/LOW-REASONING-RUNBOOK.md sebagai SOP. Gunakan npm/npx, Lerd, Node.js 26, MySQL/Redis yang sudah tersedia. Jangan menjalankan create-next-app atau memasang database kedua.

Dari root repo, periksa git status --short dan docs/agent/CHECKPOINT.md. LAKUKAN BOOTSTRAP PYTHON TOOLING SENDIRI SEBELUM P00:
python3 tools/bootstrap_agent.py

Jangan gunakan source activate, bahkan bila terminal Fish; gunakan interpreter .venv-agent/bin/python secara langsung. Bootstrap melakukan instalasi dependency ke virtualenv hanya bila perlu, lalu validasi, doctor, next, dan summary. Setelah sukses, jalankan bila perlu:
.venv-agent/bin/python tools/agent_tasks.py doctor
.venv-agent/bin/python tools/agent_tasks.py next
.venv-agent/bin/python tools/agent_tasks.py summary

Jika bootstrap gagal, hentikan pekerjaan sebelum mengubah status task; laporkan error yang nyata tanpa mengubah Python sistem atau Lerd.

Jika ada task in_progress, lanjutkan setelah audit perubahan dan bukti tes. Jika tidak ada, pilih hanya task ready pertama dari CLI. Baca card task itu dan referensi relevan saja. Implementasikan scope kecil, jalankan tes nyata setelah edit terakhir, verifikasi acceptance criteria, dan catat status/checkpoint melalui CLI.

Sebelum complete, gunakan jenis bukti yang benar melalui --kind; ikuti docs/agent/TEST-AND-REVIEW-POLICY.md. Task high-risk memerlukan review independen, jangan self-approve. Bila task pending terlalu luas, lihat docs/agent/TASK-SPLITTING.md dan siapkan rencana pemecahan yang direview. Jalankan tools/check_repo_contracts.py untuk pemeriksaan konsistensi yang relevan.

Lanjut otomatis ke task aman berikutnya selama sesi masih berjalan tanpa menunggu pesan "lanjutkan". Jika risikonya production/destruktif atau tidak bisa membuktikan hasil, catat blocker yang tepat. Jangan menebak schema, password, permission atau hasil tes.
```

Prompt ini bukan pengganti AGENTS.md atau task card. Jangan meminta user menempelkan seluruh dokumen dalam satu sesi.

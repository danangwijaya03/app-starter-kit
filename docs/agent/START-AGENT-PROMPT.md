# Start Coding Agent — Low Reasoning

**Ditujukan untuk: CODING AGENT (prompt disalin oleh USER).**

```text
Mulai implementasi app-starter-kit pada repository yang SUDAH ADA.

Baca AGENTS.md sebagai instruksi utama dan docs/agent/LOW-REASONING-RUNBOOK.md sebagai SOP. Gunakan npm/npx, Lerd, Node.js 26, MySQL/Redis yang sudah tersedia. Jangan menjalankan create-next-app atau memasang database kedua.

Periksa git status --short dan docs/agent/CHECKPOINT.md. Jalankan:
python3 tools/agent_tasks.py doctor
python3 tools/agent_tasks.py next

Jika ada task in_progress, lanjutkan setelah audit perubahan dan bukti tes. Jika tidak ada, pilih hanya task ready pertama dari CLI. Baca card task itu dan referensi relevan saja. Implementasikan scope kecil, jalankan tes nyata setelah edit terakhir, verifikasi acceptance criteria, dan catat status/checkpoint melalui CLI.

Lanjut otomatis ke task aman berikutnya selama sesi masih berjalan tanpa menunggu pesan "lanjutkan". Jika risikonya production/destruktif atau tidak bisa membuktikan hasil, catat blocker yang tepat. Jangan menebak schema, password, permission atau hasil tes.
```

Prompt ini bukan pengganti AGENTS.md atau task card. Jangan meminta user menempelkan seluruh dokumen dalam satu sesi.

# SOP Coding Agent Low — Satu Task per Unit

**Ditujukan untuk: CODING AGENT.** Perilaku wajib diatur [AGENTS.md](../../AGENTS.md). Dokumen untuk manusia adalah [PANDUAN-MULAI-LOW-AGENT.md](../../PANDUAN-MULAI-LOW-AGENT.md); jangan jadikan user guide sebagai instruksi implementasi.

## Startup setiap sesi

```bash
git status --short
python3 tools/agent_tasks.py doctor
python3 tools/agent_tasks.py next
```

1. Jika task `in_progress`, periksa checkpoint, Git diff dan pekerjaan yang telah ada; **resume** task itu terlebih dahulu.
2. Jika tidak ada, ambil task pertama dengan status `pending` yang semua dependency-nya `completed/verified`.
3. Baca **satu** card `docs/agent/tasks/<ID>.md`, `spec_refs` terkait dan source yang diperlukan saja. Jangan baca seluruh 157 card atau enam spesifikasi sekaligus.
4. Periksa file dan npm script sebelum dijalankan. **Saat ini** Next.js root memiliki `npm run dev`, `npm run lint`, `npm run build`; command npm workspace/migration/release baru ada setelah tugas implementasinya selesai.

## Kerjakan dan validasi satu task

```bash
python3 tools/agent_tasks.py show <ID>
python3 tools/agent_tasks.py start <ID>
# Edit hanya scope task, penuhi acceptance criteria
python3 tools/agent_tasks.py run <ID> -- <VALIDASI_YANG_BENAR_BENAR_ADA>
git diff --check
python3 tools/agent_tasks.py complete <ID> --note "<ringkasan hasil nyata tanpa rahasia>"
```

Teks dalam tanda `<...>` adalah placeholder, jangan dijalankan literal. Periksa `doctor/next` untuk mengetahui ID dan state nyata.

- Pada P00, validasi dokumentasi `python3 tools/validate_plan.py` boleh menjadi sebagian bukti.
- Task kode memerlukan test nyata dan relevan, termasuk negative test bila berkaitan dengan auth/RBAC/database. Exit code 0 **belum membuktikan cakupan benar**.
- Jalankan tes **setelah edit terakhir**; bukti lama harus dianggap kedaluwarsa ketika fingerprint source berubah.
- `agent_tasks.py run` hanya mencatat bukti, **bukan sandbox keamanan**. Jangan menjalankan skrip yang berpotensi memutasi database nyata.
- Jika tidak selesai karena limit sesi: `python3 tools/agent_tasks.py progress <ID> --note "<file berubah, hasil, langkah selanjutnya>"`. Jika blocked: `python3 tools/agent_tasks.py block <ID> --reason "<alasan aman>"`.
- Jangan menyatakan `complete` hanya karena file dibuat atau status validator dokumentasi hijau.

## Kontrak lingkungan dan scope

- npm/npx, satu `package-lock.json`. Jangan jalankan `npx create-next-app` lagi; migrasi root ke `apps/web` hanya ketika task P01 menginstruksikannya.
- Untuk task runtime/DB/queue baca [LOCAL-LERD-NODE26.md](LOCAL-LERD-NODE26.md): Lerd, Node 26, **existing** MySQL/Redis. Host/port dari Node di host berbeda dengan hostname di jaringan container. Database test berbeda dari dev/production dan wajib aman sebelum test yang menulis data.
- Jangan install service MySQL/Redis kedua, mengubah global Lerd routing/LAN, atau memodifikasi modul yang tidak relevan.
- `TASKS.yaml` adalah source of truth status; card adalah spesifikasi implementasi. Jangan menciptakan permission atau schema berbeda dari BSD.
- Setelah task: periksa status Git, test evidence dan checkpoint. Commit perubahan satu unit tervalidasi jika aman; lanjut task berikutnya otomatis sesuai dependency.

## Recovery & eskalasi

Pada sesi baru ikuti [RESUME-SESSION-PROMPT.md](RESUME-SESSION-PROMPT.md); **cek state sebelum mengulang migration/seed/bootstrap/job**. Jangan gunakan `git reset --hard` atau `git clean -fd` untuk pemulihan.

Block dan minta review independen/high reasoning pada bypass auth/session, race condition Super Admin, destructive migration, restore, secret, atau operasi production. Jalankan task independen lain hanya jika benar-benar aman.

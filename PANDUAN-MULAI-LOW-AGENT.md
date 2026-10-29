# Panduan Memulai Coding Agent dengan Reasoning Rendah

Paket ini adalah **dokumentasi untuk membangun aplikasi**, bukan aplikasi Next.js yang sudah berjalan. Ada 17 fase P00–P16 dan **157 unit pekerjaan kecil**. Agent tidak perlu membaca semuanya sekaligus.

## Langkah pengguna

1. Ekstrak ZIP ke root repository Git yang akan dipakai untuk membuat starter kit.
2. Pastikan Python 3 dan Git tersedia. Jalankan:

   ```bash
   python3 -m pip install -r tools/requirements-agent.txt
   python3 tools/validate_plan.py
   python3 tools/agent_tasks.py next
   ```

3. Buka `docs/agent/START-AGENT-PROMPT.md`, lalu berikan isinya kepada Codex/coding agent. Agent mengikuti `AGENTS.md` dan hanya membaca task card yang terpilih.
4. Coding agent mengerjakan task, menjalankan tes yang benar-benar tersedia, lalu menyimpan checkpoint. Setelah selesai, ia mengambil tugas berikutnya yang dependency-nya telah selesai.
5. Jika sesi terputus atau batas penggunaan tercapai, buka sesi baru dan gunakan `docs/agent/RESUME-SESSION-PROMPT.md`. Jangan menghapus perubahan dari sesi lama.

## Perintah penting

| Perintah | Hasil |
|---|---|
| `python3 tools/agent_tasks.py doctor` | Status task, Git, task aktif dan task siap |
| `python3 tools/agent_tasks.py next` | Menampilkan satu task yang harus dikerjakan |
| `python3 tools/agent_tasks.py show P01-01A` | Detail ringkas dan lokasi task card |
| `python3 tools/agent_tasks.py start P01-01A` | Mengunci task aktif secara logis |
| `python3 tools/agent_tasks.py progress P01-01A --note "..."` | Menyimpan checkpoint pekerjaan parsial |
| `python3 tools/agent_tasks.py run P01-01A -- <perintah-test>` | Menjalankan tes aman dan mencatat exit code |
| `python3 tools/agent_tasks.py complete P01-01A --note "..."` | Menandai selesai jika ada evidence lulus |
| `python3 tools/agent_tasks.py block P01-01A --reason "..."` | Menandai blocker nyata |
| `python3 tools/agent_tasks.py validate` | Memeriksa registry, dependency dan file dokumentasi |

P00 diawali dengan task `P00-01`, bukan `P01-01A`. Jangan menjalankan contoh dengan ID task yang bukan task aktif. Command `run` tidak dipakai untuk migration, bootstrap admin, restore, atau operasi production.

## Hal yang harus tetap ditinjau dengan reasoning lebih tinggi

- Integritas autentikasi, session, dan RBAC Super Admin.
- Migration schema yang merusak data, restore backup, dan recovery.
- Deployment production, kompatibilitas artifact, rollback dan keamanan kredensial.

Pada task berisiko tinggi, agent Low bisa menulis implementasi sesuai card, tetapi verifikasi independen tetap diperlukan sebelum release.

## Ketentuan proyek yang tidak boleh berubah

- Next.js + Hono + MySQL/Drizzle + Better Auth + BullMQ/Redis.
- Monorepo, TypeScript strict, Salt & Pepper sebagai preset awal.
- Empat menu: Dashboard, Manage Content, Manage User, Setting.
- Production **tanpa Docker**; build artifact diunggah ke aaPanel dan dijalankan dengan Node.js/PM2/Nginx.
- Bootstrap admin email `admin@codelight.id`; password dimasukkan secara aman ketika instalasi, **tidak disimpan dalam ZIP atau repository**.
- `README-SERVER.md` menjadi panduan instalasi setelah hasil build sudah berhasil diuji, bukan sebelum source code dibuat.
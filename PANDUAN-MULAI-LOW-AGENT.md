# Panduan Pengguna — Menjalankan Codex Low di app-starter-kit

**Ditujukan untuk: USER / DEVELOPER.** Dokumen ini menjelaskan langkah manusia untuk menyiapkan komputer, memulai, memantau, dan melanjutkan Codex. **Instruksi coding agent ada di [AGENTS.md](AGENTS.md)** dan [runbook](docs/agent/LOW-REASONING-RUNBOOK.md), bukan di panduan ini.

**Repository:** [danangwijaya03/app-starter-kit](https://github.com/danangwijaya03/app-starter-kit), branch `main`. Next.js 16.4.3 sudah terpasang pada root repository. Jangan membuat ulang aplikasi dengan `create-next-app`. Monorepo dan semua fitur lain masih akan dikerjakan melalui task.

## 1. Periksa lingkungan lokal

Gunakan **Lerd, Node.js 26, npm/npx, serta MySQL Lerd yang sudah tersedia**. Redis Lerd digunakan pada task BullMQ. Production tanpa Docker: hasil build diunggah ke server aaPanel.

Di terminal, dari clone Git yang sudah ada:

```bash
cd app-starter-kit
git status --short
```

Jika ada perubahan lokal, periksa dan simpan terlebih dahulu. Bila working tree bersih:

```bash
git pull --ff-only origin main
node --version
npm --version
lerd status
lerd service list
```

Node diharapkan `v26.x`. Jangan membuat MySQL/Redis tambahan atau mengubah pengaturan global Lerd. Agent akan memverifikasi host/port dan membuat pemisahan database development dan testing di fase P02.

## 2. Menjalankan Next.js yang sudah ada

```bash
npm ci
npm run dev
```

Buka `http://localhost:3000`; gunakan `Ctrl+C` untuk menghentikan proses. Perintah `npm run lint` dan `npm run build` tersedia pada instalasi awal. Setelah migrasi P01, command dapat berubah mengikuti npm workspace yang diimplementasikan dan diuji oleh agent.

## 3. Siapkan pemantauan task (sekali)

Tooling task memakai Python, bukan pnpm:

```bash
python3 -m venv .venv-agent
source .venv-agent/bin/activate
python -m pip install -r tools/requirements-agent.txt
python tools/validate_plan.py
python tools/agent_tasks.py doctor
python tools/agent_tasks.py next
python tools/agent_tasks.py summary
```

Jika virtualenv tidak tersedia, pasang dukungan `venv` sesuai distro OS, bukan menggunakan `--break-system-packages`. `validate_plan.py` hanya memverifikasi dokumentasi dan dependency; ini **bukan pengujian aplikasi**.

## 4. Jalankan Codex Low

1. Buka folder **app-starter-kit** di editor/Codex CLI; gunakan branch dan working tree yang benar.
2. Pilih reasoning **Low**.
3. Salin isi [START-AGENT-PROMPT.md](docs/agent/START-AGENT-PROMPT.md) sebagai pesan pertama kepada agent.
4. Biarkan agent membaca `AGENTS.md`, memilih **satu task aktif**, mengimplementasikan, menguji, dan menyimpan checkpoint. Tidak perlu menempelkan semua task card dalam satu prompt.

**Jangan gunakan panduan pengguna ini sebagai prompt implementasi agent.** Petunjuk teknis ditetapkan dalam dokumen khusus agent.

## 5. Pantau dan lanjutkan sesi

Lihat status dengan:

```bash
python tools/agent_tasks.py doctor
python tools/agent_tasks.py next
git status --short
git log -5 --oneline
```

`in_progress` perlu dilanjutkan, `completed` sudah memiliki bukti tes tercatat, `verified` sudah melewati gate fase. Status tidak menggantikan code review. Task dengan risiko tinggi perlu peninjau independen; Anda dapat memeriksa catatan review di `docs/agent/reviews/` sebelum task disahkan. Jika limit Codex habis, buka sesi baru di repository **yang sama** dan salin [RESUME-SESSION-PROMPT.md](docs/agent/RESUME-SESSION-PROMPT.md). Jangan reset Git atau mulai dari awal.

## 6. Kapan perlu review pengguna

Perlu persetujuan atau reasoning lebih tinggi untuk keamanan authentication/RBAC, credential, perubahan sistem global Lerd, migration destruktif, restore data, dan deployment production. Database test harus terpisah dari development dan tidak boleh memakai database proyek Lerd lain.

Akun bootstrap `admin@codelight.id` menggunakan secret instalasi; password tidak boleh disimpan di source code maupun dokumentasi.

## 7. Referensi menurut tujuan

- [README.md](README.md): ringkasan repository dan menjalankan Next.js.
- [DOCUMENTATION-MAP.md](docs/DOCUMENTATION-MAP.md): siapa membaca dokumen apa.
- [PHASES.md](docs/agent/PHASES.md): roadmap/progres.
- [PRD](docs/PRD.md), [TRD](docs/TRD.md), [IPD](docs/IPD.md): spesifikasi.
- [README-SERVER.md](README-SERVER.md): panduan **setelah** release berhasil dibuat pada P16. CLI instalasi di dalamnya belum bisa dijalankan sekarang.

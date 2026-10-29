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

## 3. Setup tooling dilakukan Codex secara otomatis

**Anda tidak perlu membuat virtual environment, menginstal PyYAML, atau mengaktifkan `.venv-agent` secara manual.** Setelah START prompt diberikan, coding agent menjalankan `python3 tools/bootstrap_agent.py` di root project. Script otomatis membuat/memeriksa virtualenv, memasang dependency Python bila diperlukan, memvalidasi dokumentasi dan repository, lalu menampilkan task berikutnya.

Ini **tidak bergantung pada shell**: Fish, Bash, dan Zsh menggunakan interpreter `.venv-agent/bin/python` secara langsung. Jangan menjalankan `source .venv-agent/bin/activate` pada Fish.

Jika ingin memeriksa setup sendiri secara opsional:

```bash
python3 tools/bootstrap_agent.py
```

Jika bootstrap gagal (misalnya Python venv belum tersedia, internet tidak tersedia untuk instalasi dependency, atau permission tidak memadai), agent akan melaporkan penyebabnya dan **tidak** menandai task selesai. Jangan memakai `--break-system-packages` untuk memaksa instalasi.

## 4. Jalankan Codex Low

1. Buka folder **app-starter-kit** di editor/Codex CLI; gunakan branch dan working tree yang benar.
2. Pilih reasoning **Low**.
3. Salin isi [START-AGENT-PROMPT.md](docs/agent/START-AGENT-PROMPT.md) sebagai pesan pertama kepada agent.
4. Agent otomatis melakukan bootstrap Python terlebih dahulu, lalu membaca `AGENTS.md`, memilih **satu task aktif**, mengimplementasikan, menguji, dan menyimpan checkpoint. Tidak perlu menempelkan semua task card dalam satu prompt.

**Jangan gunakan panduan pengguna ini sebagai prompt implementasi agent.** Petunjuk teknis ditetapkan dalam dokumen khusus agent.

## 5. Pantau dan lanjutkan sesi

Lihat status dengan:

```bash
.venv-agent/bin/python tools/agent_tasks.py doctor
.venv-agent/bin/python tools/agent_tasks.py next
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

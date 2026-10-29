# Panduan Memulai Development — Codex Low, Lerd, Node.js 26 & MySQL

> **Status repository:** \`danangwijaya03/app-starter-kit\` sudah berisi aplikasi Next.js 16.4.3 hasil \`npx create-next-app@latest\` pada **root repository**. Ini panduan untuk mengembangkan aplikasi yang ADA, bukan membuat proyek baru. Dokumentasi, task registry, dan tooling agent sudah tersedia; API, worker, CMS, RBAC, installer, npm monorepo, dan release artifact **belum diimplementasikan** sampai task-nya selesai.

## 1. Lingkungan development yang digunakan

| Komponen | Ketentuan |
|---|---|
| OS | Linux development lokal |
| Local development manager | **Lerd** (gunakan service yang sudah ada, jangan membuat ulang) |
| Node.js | **26.x** (cek \`node --version\`; catat patch yang benar-benar terpasang) |
| Package manager | **npm/npx**; satu \`package-lock.json\`; **tidak memakai pnpm/yarn/bun** |
| Frontend awal | Next.js 16.4.3 + React 19.3.0 + Tailwind v4 di root |
| Database | **MySQL melalui Lerd**; pastikan versi aktual sebelum migration |
| Queue | Redis dari Lerd, ketika fase worker membutuhkan Redis |
| Domain lokal | Gunakan \`localhost\` terlebih dahulu; \`*.test\` / HTTPS melalui Lerd hanya setelah konfigurasi diverifikasi |
| Production | Tanpa Docker: hasil build diupload; Node.js/PM2 + Nginx/aaPanel + MySQL/Redis |

Node.js 26 menjadi target lingkungan pengembangan saat ini. **Jangan menurunkan versi ke Node 24 hanya karena ada petunjuk lama.** Saat release, cocokkan versi Node/ABI dengan build artifact dan server target; jangan menganggap semua dependency sudah kompatibel sampai diuji.

Untuk instruksi Lerd lebih rinci baca [LOCAL-LERD-NODE26.md](docs/agent/LOCAL-LERD-NODE26.md). Lerd menyediakan MySQL dan Redis; agent tidak perlu memasang container atau service database kedua.

## 2. Langkah yang dijalankan pengguna (sekali pada clone lokal)

Masuk ke clone repository yang sudah ada, lalu sinkronkan dokumentasi:

\`\`\`bash
cd app-starter-kit
git status --short
git pull --ff-only origin main

node --version
npm --version
lerd status
lerd service list
\`\`\`

**Jangan melakukan \`git pull\` jika ada perubahan lokal yang belum diperiksa.** Node harus melaporkan \`v26.*\`. Jika tidak, periksa pengaturan Node milik Lerd/mise tanpa menghapus versi lain.

Instal dependency berdasarkan lockfile **hanya jika perlu**:

\`\`\`bash
npm ci
\`\`\`

Siapkan Python tooling untuk task agent di lingkungan virtual agar Python sistem tidak tercampur:

\`\`\`bash
python3 -m venv .venv-agent
source .venv-agent/bin/activate
python -m pip install -r tools/requirements-agent.txt
python tools/validate_plan.py
python tools/agent_tasks.py doctor
python tools/agent_tasks.py next
\`\`\`

Jika pembuatan virtualenv gagal karena paket OS belum tersedia, gunakan cara instalasi Python yang sesuai sistem; jangan memaksa \`pip --break-system-packages\`.

Pada **fase awal, sebelum P01 memigrasikan layout**, perintah aplikasi yang benar adalah:

\`\`\`bash
npm run dev
npm run lint
npm run build
\`\`\`

Setelah P01, gunakan **script npm workspace yang benar-benar telah dibuat dan diuji**. Agent tidak boleh menganggap \`npm run db:migrate\`, \`npm run release:build\`, atau \`npm run dev --workspaces\` sudah tersedia sejak awal.

## 3. MySQL Lerd: wajib bedakan database dev dan testing

Pada P02, agent **memeriksa ulang koneksi ke MySQL Lerd yang sudah terpasang**, bukan menginstal MySQL baru. Lakukan preflight read-only: \`lerd service list\`, status MySQL, \`mysql --version\` dan \`SELECT VERSION()\` melalui akun yang diizinkan. Jangan tampilkan password dalam terminal/log/checkpoint.

Gunakan **database khusus proyek**, dan **database testing terpisah**. Contoh nama \`app_starter_kit_dev\` dan \`app_starter_kit_test\`. Nama hanyalah usulan; agent harus memeriksa collision dan meminta izin bila pembuatan database yang baru diperlukan. Jangan menjalankan \`DROP DATABASE\`, \`TRUNCATE\`, restore, atau migration destruktif terhadap database mana pun tanpa otorisasi yang sesuai.

**Lokasi koneksi bergantung pada cara proses berjalan:**
- Jika Node berjalan di **host**, biasanya memakai host/port MySQL yang diekspos oleh Lerd ke host (sering \`127.0.0.1\` + port yang telah diverifikasi).
- Jika proses berjalan **di network container Lerd**, nama service seperti \`lerd-mysql\` dapat berlaku.
- Jangan menyalin \`DB_HOST=lerd-mysql\` atau \`DATABASE_URL=mysql://...@lerd-mysql\` untuk Node host tanpa memastikan DNS dan koneksinya.

Lerd dapat memperbarui \`.env\` ketika \`lerd init\` atau \`lerd env\` dijalankan. **Jangan menjalankan \`lerd init --fresh\`, \`lerd env\`, atau mengubah \`.lerd.yaml\` secara otomatis tanpa mengecek dampaknya**, terutama jika ada proyek lain yang menggunakan konfigurasi Lerd. \`NEXT_PUBLIC_*\` tidak boleh berisi DB/password/secret.

Sebelum test yang menulis data, agent wajib memastikan *target DB* adalah database test, bukan development, production, atau shared. Jika koneksi atau versi MySQL belum dapat diverifikasi, **block P02**, jangan berasumsi.

## 4. Redis Lerd

Redis bukan database utama, tetapi **diperlukan untuk BullMQ**. Pada P02-03 lakukan preflight \`lerd service list\` / status Redis; gunakan layanan Redis Lerd yang tersedia. Verifikasi koneksi sesuai proses host/container. Jangan membuat daemon Redis duplikat atau membuka port Redis ke LAN/internet. Jika layanan belum aktif, lakukan tindakan yang disetujui untuk development dan catat hasilnya.

## 5. Menjalankan coding agent Low

Berikan isi [START-AGENT-PROMPT.md](docs/agent/START-AGENT-PROMPT.md) kepada agent. Untuk setiap sesi:

1. Baca [AGENTS.md](AGENTS.md), [LOW-REASONING-RUNBOOK.md](docs/agent/LOW-REASONING-RUNBOOK.md), [IMPLEMENTATION-CONTRACTS.md](docs/agent/IMPLEMENTATION-CONTRACTS.md), dan **satu task card aktif**.
2. Jalankan \`git status --short\`, \`python tools/agent_tasks.py doctor\`, lalu \`python tools/agent_tasks.py next\`.
3. Mulai hanya task yang dependency-nya terpenuhi. Jangan mengulang \`npx create-next-app\` atau memindahkan source sebelum task P01.
4. Kerjakan satu unit kecil; jalankan tes yang benar-benar ada dan relevan, periksa output, \`git diff --check\`, lalu simpan evidence dan checkpoint.
5. Tandai \`completed\` **hanya jika** perubahan source memenuhi acceptance criteria dan tes lulus dengan kode **terkini**. Jangan gunakan output tes sebelum edit terakhir.
6. Lanjut otomatis ke task berikutnya yang aman. Jika tidak dapat membuktikan hasil, simpan \`progress\` atau \`block\` dengan alasan yang jelas, bukan menebak.

Task pertama adalah **P00-01**, bukan P01. Semua 157 task pada registry adalah pekerjaan rencana, bukan bukti sudah ada fitur.

Perintah agent:

| Perintah | Fungsi |
|---|---|
| \`python tools/agent_tasks.py doctor\` | Status repository dan task |
| \`python tools/agent_tasks.py next\` | Menentukan task yang aktif/siap |
| \`python tools/agent_tasks.py show P00-01\` | Membaca target task |
| \`python tools/agent_tasks.py start P00-01\` | Menandai mulai (jika siap) |
| \`python tools/agent_tasks.py progress P00-01 --note "..." \` | Checkpoint parsial |
| \`python tools/agent_tasks.py run P00-01 -- python tools/validate_plan.py\` | Bukti validasi dokumentasi untuk tugas dokumentasi |
| \`python tools/agent_tasks.py complete P00-01 --note "..." \` | Selesai jika syarat benar-benar terpenuhi |
| \`python tools/agent_tasks.py block P00-01 --reason "..."\` | Catat blocker yang sebenarnya |

**Contoh ID di atas hanya untuk P00-01.** Ganti dengan ID task aktif sesungguhnya. Jangan pakai validasi dokumen sebagai satu-satunya evidence tugas coding.

## 6. Recovery setelah limit agent habis

Di sesi baru gunakan [RESUME-SESSION-PROMPT.md](docs/agent/RESUME-SESSION-PROMPT.md). Baca \`CHECKPOINT.md\`, \`TASKS.yaml\`, status/diff Git dan evidence tes; lanjutkan unit yang sedang \`in_progress\`. Jangan mengulang migration/seed/bootstrap atau memulai task lain tanpa mengecek state sebenarnya.

Dilarang menggunakan \`git reset --hard\`, \`git clean -fd\`, menghapus data, memindahkan koneksi database, atau mengubah layanan Lerd secara spekulatif.

## 7. Pemeriksaan yang perlu reasoning lebih tinggi

Wajib review independen untuk: authentication/session security, RBAC Super Admin dan concurrency, migration destruktif, backup/restore, kompatibilitas release native, kredensial production, serta deployment/rollback ke server.

Agent Low boleh mengimplementasikan fitur rutin, tetapi tidak boleh mengklaim verification gate lulus jika belum ada tes yang relevan.

## 8. Batasan penting

- **Tidak mengubah repository menjadi monorepo pada saat memasukkan dokumentasi.** P01 yang akan melakukannya.
- Semua perintah server pada [README-SERVER.md](README-SERVER.md) masih **target** sampai installer/release selesai pada P16.
- Akun bootstrap \`admin@codelight.id\` menggunakan secret instalasi yang tidak dicatat di Git. Password production harus unik dan diganti saat login pertama.
- Site Lerd dengan domain \`.test\` adalah development **saja**, berbeda dari aaPanel production.

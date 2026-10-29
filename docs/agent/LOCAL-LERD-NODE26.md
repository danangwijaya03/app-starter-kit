# Kontrak Local Development — Lerd + Node.js 26 + MySQL

**Dokumen wajib untuk P00/P01/P02 dan task lokal yang memakai MySQL/Redis.** Repository awal sudah memiliki Next.js di root dan menggunakan npm. Dokumen ini tidak mengubah layanan atau aplikasi secara otomatis.

## Baseline yang diketahui
- Developer memakai **Lerd**, **Node.js 26**, **MySQL**.
- Lerd menyediakan MySQL dan Redis. Gunakan service existing jika tersedia; **jangan menambah Docker Compose atau database daemon kedua**.
- Package manager **npm/npx** saja. \`package-lock.json\` root dipertahankan.
- DB target produksi tetap MySQL 8.4 LTS (versi lokal harus dibuktikan; jangan diklaim hanya dari nama layanan).
- Domain \`*.test\` dan HTTPS adalah opsi local Lerd, **bukan** syarat agar Next.js dapat diuji lewat \`localhost\`.

## Preflight tanpa perubahan environment

\`\`\`bash
pwd
git status --short
node --version
npm --version
lerd status
lerd service list
mysql --version
\`\`\`

Catat versi Node patch dan MySQL aktual dalam catatan dependensi dengan menghilangkan kredensial. Node harus 26.x; jika berbeda, periksa runtime manager Lerd/mise, jangan memaksa install/uninstall.

## Konteks koneksi host vs container

| Aplikasi dieksekusi dari | Host service database | Perhatian |
|---|---|---|
| Node lokal di host | Alamat loopback dan port host dari Lerd yang benar-benar dapat diakses | Jangan asumsikan nama \`lerd-mysql\` resolve pada host |
| App di container/network Lerd | \`lerd-mysql:3306\` dan \`lerd-redis:6379\` dapat dipakai | Harus dipastikan lewat pemeriksaan koneksi |
| Production aaPanel | Endpoint MySQL dan Redis production | Sama sekali tidak menggunakan kredensial Lerd |

Periksa service routing dalam dokumentasi Lerd dan hasil tes dari proses Node yang sesungguhnya. **Jangan menebak host port atau menulis password ke stdout**.

## Database dev dan test yang benar-benar terpisah

- Pilih dua schema MySQL unik: satu **dev** dan satu **test** (mis. \`app_starter_kit_dev\`, \`app_starter_kit_test\`); jangan menggunakan schema milik proyek lain.
- Jangan menganggap MySQL Lerd bisa dihapus total karena task menyebut kata "disposable". Yang disposable hanyalah schema khusus test yang **sudah ditandai aman**.
- Penggunaan database test wajib memeriksa nama schema, host dan port sebelum mutasi; operasi reset/drop diblok secara default.
- Test yang gagal koneksi harus **fail**, bukan otomatis switch ke DB dev.
- Buat database/user baru hanya apabila telah diverifikasi tidak ada, dan bila izin operator yang sesuai tersedia.
- Gunakan \`mysql --version\` dan query read-only \`SELECT VERSION(); SELECT DATABASE();\` pada koneksi yang diverifikasi.
- Untuk backend \`mysql2\`, hindari membentuk URL dari password tanpa encoding; pisahkan host, user, port, database bila perlu.
- \`.env*\` harus gitignored; \`.env.example\` hanya placeholder tanpa credential nyata.

## Redis

BullMQ membutuhkan Redis pada fase P13. P02 hanya memverifikasi service Redis Lerd dan koneksi dari proses host/container yang benar. Tidak perlu daemon baru. Queue harus namespaced untuk proyek dan test; jangan menggunakan antrean milik proyek lain. Redis tidak dibuka ke internet atau LAN.

## Lerd-managed site dan environment

- \`lerd init\`, \`lerd env\`, dan \`lerd link\` dapat menulis \`.lerd.yaml\` / \`.env\` atau mengubah pendaftaran domain. **Review perubahan sebelum menjalankan**.
- Lerd dapat membuat database project dan varian testing secara otomatis untuk konfigurasi tertentu; cek terlebih dahulu apakah nama tersebut akan bertabrakan.
- Mulai dari \`npm run dev\` di root repo. Integrasi Lerd \`*.test\` dilakukan saat konfigurasi jelas, dan URL Better Auth/trusted origin disesuaikan setelah proxy HTTPS diverifikasi.
- Node process di host dan DB service di container memakai aturan host berbeda. Jangan hard-code \`lerd-mysql\` dalam \`.env.example\` universal.
- Jika Lerd telah mengelola Node dev process, jangan menjalankan instance kedua pada port yang sama. Jangan mengutak-atik LAN exposure, Nginx service atau routing tanpa scope task dan izin operator.
- Jangan commit \`.lerd.yaml\` yang memuat credential, private path, atau pengaturan spesifik komputer; review terlebih dahulu.

## Checklist sebelum task P02 dinyatakan selesai

1. Runtime Node 26 diverifikasi dari proses yang benar-benar menjalankan aplikasi.
2. MySQL yang dipakai terbukti existing Lerd service dan koneksi sukses.
3. Database dev dan test berbeda serta diberi guard pada script test.
4. Redis existing service tersedia dan koneksinya tervalidasi sebelum BullMQ dipakai.
5. Tidak ada rahasia dalam Git/checkpoint/log.
6. Tidak ada container/daemon tambahan atau perubahan Lerd global yang tidak diminta.
7. Testing memakai database **test**, tidak memutasi database dev/production.

Sumber eksternal:
- https://lerd.sh/getting-started/services
- https://lerd.sh/usage/sites
- https://lerd.sh/getting-started/containers
- https://nodejs.org/en/about/previous-releases

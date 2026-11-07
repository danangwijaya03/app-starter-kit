# AI Coding Agent — Workflow Ringkas

**Status: instruksi pengerjaan baru; tidak ada tooling/task registry Python lama.** Selalu baca [AGENTS.md](../AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), dan [ROADMAP.md](ROADMAP.md) sebelum implementasi.

## Pembagian kerja

- **Implementation agent** (contoh GPT-6.1 Sol Medium bila tersedia): implementasi satu tugas scoped, test terkait, catatan hasil dan commit.
- **Independent QA agent** (contoh GPT-5.6 Terra bila tersedia): negative tests, integration/E2E, review security, regression dan defect report. Identitas model hanya preferensi operator, bukan syarat stack.
- Review high-risk (authentication, RBAC, migrasi data, backup/restore, deploy/rollback) harus independen dari implementer. Tidak diperbolehkan self-approval.

## Satu siklus task

1. **RECOVER** — cek `git branch --show-current`, `git status --short`, commit terbaru, dokumen dan checkpoint aktif. Pastikan di `dev`/feature branch, tidak mengubah `main`.
2. **IMPLEMENT** — pilih task terkecil dari roadmap; tulis acceptance criteria dan dependensinya. Implementasi satu vertical slice, bukan memperluas scope tanpa alasan.
3. **TEST** — jalankan linter/typecheck/unit/integration/negative tests yang relevan setelah **edit terakhir**; jangan mengklaim tes tanpa output nyata.
4. **VERIFY** — bandingkan hasil dengan acceptance dan dokumentasikan mismatch aktual. Jalankan build jika konfigurasi/runtime berubah.
5. **CHECKPOINT** — commit hanya berkas terkait; simpan ringkasan task/status/file/test/commit/next action yang dapat dipakai sesi berikutnya.
6. **NEXT** — lanjut task ready berikutnya tanpa konfirmasi rutin kecuali ada blocker, operasi destructive, perubahan secret/production, atau pilihan arsitektur material.

Checkpoint boleh disimpan ringkas di body commit atau catatan lokal yang tercatat di Git. Tidak perlu membuat sistem tracking kompleks sebelum kebutuhan muncul. Bila memakai file checkpoint baru, jangan menyalin struktur task 157 item yang telah dihapus.

## Testing cadence

Implementer wajib menjalankan scoped tests setiap task. QA independen dapat melakukan review per milestone (foundation, security, product, release), tetapi risiko tinggi direview sebelum dinyatakan tuntas. Tes migration/restore harus pada MySQL disposable yang terisolasi dari data dev/production.

## Aturan kode

- npm/npx, satu root lockfile saat P01 selesai; jangan memperkenalkan pnpm, Docker produksi atau Turborepo tanpa keputusan tercatat.
- Source Next.js saat ini di root; **jangan** menginisialisasi ulang Next.js.
- Pisahkan Next UI, Hono business API dan worker; shared types di contracts, database hanya server-side.
- Seluruh authorization harus di API; jangan mempercayai sidebar/client checks.
- Jangan pernah menyimpan password, database URL, credential live atau token di source, docs, logs, test snapshots, maupun commit.
- Jangan auto-deploy ke server, menjalankan migration berbahaya, restore database live, atau menghapus data tanpa persetujuan eksplisit.
- Hasil produk baru dianggap selesai setelah build, tes, dan gate terverifikasi. Dokumentasi desain tidak membuktikan fitur sudah berfungsi.

Rujukan: [ROADMAP.md](ROADMAP.md), [DEPLOYMENT.md](DEPLOYMENT.md).

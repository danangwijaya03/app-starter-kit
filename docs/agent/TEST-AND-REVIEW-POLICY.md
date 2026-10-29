# Kebijakan Bukti Uji dan Review — untuk Coding Agent

**Ditujukan untuk: CODING AGENT / reviewer independen.** Aturan ini mengikat task CLI; tidak menggantikan review keamanan nyata.

## Klasifikasi risiko

- **Low**: dokumentasi, UI biasa, scaffolding; tes relevan sesuai output.
- **Medium**: validasi input, database CRUD, media/queue; tes positif dan jalur gagal sesuai kontrak.
- **High**: login/session, credential, RBAC, bootstrap Super Admin, migration penting, backup, restore, dan deployment/rollback. **Wajib review independen** (human atau agent High yang berbeda) setelah kode selesai dan tes aktual lulus.

Risiko registry `risk: low` lama tidak dapat dipakai untuk menurunkan risiko high. CLI menentukan **effective risk** berdasarkan phase/keyword dan nilai eksplisit task, mengambil tingkat tertinggi. Tool CLI tidak mengautentikasi reviewer; catatan review hanya rekaman proses, bukan bukti identitas kriptografis.

## Matriks tes minimum

| Kategori | Jenis bukti yang harus ada sebelum complete |
|---|---|
| P00 | `docs` (graph/link validator, content review) |
| P01/P02/P06/P08 UI | `unit` atau `integration` atau `build` yang benar-benar memeriksa hasil |
| P03/P04/P05/P07/P09/P10/P11/P12/P13 | `unit` atau `integration`; tambahkan `negative` untuk auth/role, upload, dan publishing |
| P14/P15 backup/restore | `integration` dalam database test disposable; `negative` untuk checksum / permission / kegagalan |
| P16 release/deploy | `integration`/isolated release smoke + `negative`; tidak boleh menjalankan production deployment sebagai bukti tes |

CLI `run` menerima `--kind unit|integration|negative|build|docs` sebelum `--` perintah pengujian; bukti berupa exit code, fingerprint isi repository saat tes, dan perintah yang dijalankan. Negative test berarti **assertion memang menguji penolakan/gagal aman**, bukan menjalankan command yang gagal lalu menganggapnya lulus. `npm run build` tidak boleh menggantikan tes keamanan.

**Contoh (setelah test script benar-benar dibuat):**

```bash
python3 tools/agent_tasks.py run P04-02 --kind integration -- npm run test --workspace=@repo/api -- auth
python3 tools/agent_tasks.py run P04-02 --kind negative -- npm run test --workspace=@repo/api -- auth-denied
```

Jangan mengeksekusi contoh jika script/nama test belum tersedia. `run` adalah recorder, **bukan sandbox**. Periksa sendiri test suite tidak memodifikasi DB dev/shared.

## Tinjauan independen risiko high

1. Agent Low menyiapkan implementasi dan tes, lalu laporkan task ke reviewer eksternal; jangan mengisi persetujuan atas pekerjaannya sendiri.
2. Reviewer High/human membaca diff, test assertions, invariants dari BSD/TRD, dan jalur gagal.
3. Reviewer membuat catatan tertulis di `docs/agent/reviews/<TASK_ID>.md`, dengan keputusan **APPROVED**, identitas reviewer, commit/diff yang ditinjau, hasil test dan temuan; bukan sekadar "looks good".
4. Operator merekam review dengan CLI `review <ID> --reviewer ... --evidence docs/agent/reviews/<ID>.md`. CLI memeriksa file dan fingerprint terkini; tidak membuktikan bahwa reviewer independen. Jika source berubah sesudah review, persetujuan gugur.
5. Tanpa review, task high tidak bisa `complete` dan gate fase ditolak. Low agent tidak boleh menyamar sebagai reviewer atau menurunkan label risiko.

Review pekerjaan yang berdampak pada live database atau deployment **tidak** otomatis memberi izin melakukan tindakan produksi. Persetujuan operasional terpisah tetap diperlukan.

## Kasus wajib per domain (contoh acceptance)

| Domain | Happy path | Negative / race / gagal aman |
|---|---|---|
| Auth | login/session valid | session dicabut, cookie tidak sah, rate limit, first-login guard |
| RBAC | role union sah | no grant 403, self-escalation ditolak, dua operasi terhadap last super_admin |
| CMS | draft/revision/publish | draft tidak bocor, konflik slug 409, block tidak valid ditolak |
| Media | unggah valid | MIME palsu, traversal, referensi published menghalangi delete |
| Worker | job sukses dan checkpoint | duplicate job, retry aman, worker restart |
| Backup | backup terenkripsi dan verify restore disposable | checksum gagal, media hilang, secrets tidak bocor |
| Restore | staging restore test terisolasi | manifest invalid, lock overlap, kegagalan import, maintenance tetap aman |
| Release | archive standalone hasil build | checksum/arsitektur/Node ABI salah ditolak, rollback kode tidak dianggap rollback DB |

## Phase gate (wajib sebelum status verified)

Untuk fase berisiko tinggi P04, P05, P14, P15, dan P16, gate memerlukan **dua pengujian pada source terkini**: integration dan negative. Catatan per-task dan review harus sudah selesai. Contoh hanya bila npm test script sesuai telah dibuat:

```bash
python3 tools/agent_tasks.py gate-run P04 --kind integration -- npm run test --workspace=@repo/api -- auth
python3 tools/agent_tasks.py gate-run P04 --kind negative -- npm run test --workspace=@repo/api -- auth-denied
python3 tools/agent_tasks.py gate P04
```

Fase P00 menggunakan gate dengan `--kind docs`. Fase non-high lain membutuhkan salah satu dari `unit/integration/build`. Semua gate menolak bukti yang fingerprint source-nya sudah berubah. Test label bukan bukti semantik: reviewer harus memeriksa assertion sesuai kasus.

## Makna Status

`completed` = implementasi dan tes minimum terekam (serta review bila high). `verified` = gate fase lulus sesuai cakupan dan tidak ada bukti usang. Hasil otomatis tetap harus diaudit untuk konteks keamanan.

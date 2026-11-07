const modules = [
  { name: "Dashboard", detail: "Ringkasan aplikasi", ready: true },
  { name: "Manage Content", detail: "CMS dan media", ready: false },
  { name: "Manage User", detail: "User dan role", ready: false },
  { name: "Setting", detail: "Tampilan dan konfigurasi", ready: false },
];

const checkpoints = [
  { id: "P00", name: "Next.js baseline", state: "Preview statis" },
  { id: "P01", name: "Monorepo dan UI shell", state: "Direncanakan" },
  { id: "P02–P03", name: "API, MySQL, health preview", state: "Direncanakan" },
  { id: "P04–P08", name: "Login, RBAC, dashboard", state: "Direncanakan" },
  { id: "P09–P12", name: "CMS, media, settings", state: "Direncanakan" },
  { id: "P13–P16", name: "Worker, recovery, installer", state: "Direncanakan" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f5f5f5] text-[#2b2b2b]">
      <div className="mx-auto flex min-h-screen max-w-[1440px] flex-col gap-6 p-4 md:flex-row md:gap-8 md:p-8">
        <aside className="w-full shrink-0 rounded-2xl border border-[#d4d4d4] bg-white p-5 md:w-64">
          <p className="text-xs font-bold tracking-[0.2em] text-[#777]">CODELIGHT</p>
          <h1 className="mt-2 text-xl font-semibold tracking-tight">app-starter-kit</h1>
          <p className="mt-2 text-xs leading-relaxed text-[#777]">Development preview · UI-only baseline</p>
          <nav aria-label="Rancangan navigasi admin" className="mt-8 space-y-2">
            {modules.map((module) => (
              <div key={module.name} className={`rounded-xl p-3 ${module.ready ? "bg-[#2b2b2b] text-white" : "bg-[#f5f5f5] text-[#777]"}`}>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium">{module.name}</span>
                  <span className="text-[10px] opacity-70">{module.ready ? "Demo" : "Planned"}</span>
                </div>
                <span className="mt-1 block text-xs opacity-70">{module.detail}</span>
              </div>
            ))}
          </nav>
          <p className="mt-8 rounded-xl border border-dashed border-[#d4d4d4] p-3 text-xs leading-relaxed text-[#777]">
            Ini adalah preview tampilan, bukan dashboard dengan autentikasi, API atau database aktif.
          </p>
        </aside>
        <main className="min-w-0 flex-1 space-y-6">
          <header className="rounded-2xl border border-[#d4d4d4] bg-white p-6 md:p-8">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#777]">Incremental development</p>
                <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">Preview sejak fase awal</h2>
                <p className="mt-3 max-w-2xl text-sm leading-relaxed text-[#666]">
                  UI dapat direview sebelum seluruh backend selesai. Setiap fitur berikutnya wajib menyertakan bukti tes,
                  status integrasi dan langkah review yang dapat direproduksi.
                </p>
              </div>
              <span className="rounded-full border border-[#d4d4d4] px-3 py-1 text-xs font-semibold">STATIC DEMO</span>
            </div>
          </header>
          <section aria-labelledby="status-heading" className="grid gap-4 sm:grid-cols-3">
            <h3 id="status-heading" className="sr-only">Status fondasi development</h3>
            {[
              { label: "Web / Next.js", value: "Tersedia", note: "Baseline preview" },
              { label: "Hono API", value: "Belum aktif", note: "Menunggu implementasi" },
              { label: "MySQL / RBAC", value: "Belum aktif", note: "Menunggu implementasi" },
            ].map((item) => (
              <div key={item.label} className="rounded-2xl border border-[#d4d4d4] bg-white p-5">
                <p className="text-xs font-medium text-[#777]">{item.label}</p>
                <p className="mt-3 text-xl font-semibold">{item.value}</p>
                <p className="mt-2 text-xs text-[#777]">{item.note}</p>
              </div>
            ))}
          </section>
          <section aria-labelledby="checkpoints-heading" className="rounded-2xl border border-[#d4d4d4] bg-white p-6">
            <div className="flex flex-wrap justify-between gap-3">
              <h3 id="checkpoints-heading" className="text-lg font-semibold">Rencana checkpoint review</h3>
              <span className="text-xs text-[#777]">Bukan status task otomatis</span>
            </div>
            <div className="mt-5 divide-y divide-[#e9e9e9]">
              {checkpoints.map((phase) => (
                <div key={phase.id} className="flex flex-wrap items-center justify-between gap-3 py-3">
                  <div className="flex items-center gap-3">
                    <span className="min-w-16 rounded-lg bg-[#ededed] px-2 py-1 text-center text-xs font-semibold">{phase.id}</span>
                    <span className="text-sm">{phase.name}</span>
                  </div>
                  <span className="text-xs text-[#777]">{phase.state}</span>
                </div>
              ))}
            </div>
          </section>
          <p className="pb-4 text-xs text-[#777]">
            Panduan review: docs/DEVELOPMENT-ROADMAP.md · Implementasi agent: AGENTS.md
          </p>
        </main>
      </div>
    </div>
  );
}

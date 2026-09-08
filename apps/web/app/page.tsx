/**
 * ClimaX Root Page — Phase 0 Architecture Status
 * Feature implementations commence in Phase 1 (Frontend Foundation & Design System).
 */
export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <div className="max-w-2xl rounded-lg border border-slate-800 bg-[#121824] p-8 shadow-xl">
        <span className="inline-block rounded-full bg-emerald-950 px-3 py-1 text-xs font-semibold text-emerald-400 border border-emerald-800">
          Phase 0: Architecture & Scaffolding Active
        </span>
        <h1 className="mt-4 text-3xl font-bold tracking-tight text-white">
          ClimaX
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Federated AI Environmental Intelligence & Action Platform
        </p>
        <p className="mt-6 text-xs text-slate-500">
          Core architectural structure, contracts, schemas, and configurations initialized.
          UI screen development commences in Phase 1.
        </p>
      </div>
    </main>
  );
}

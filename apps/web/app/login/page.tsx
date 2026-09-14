'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';

export default function LoginPage() {
  const router = useRouter(); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); const form = new FormData(event.currentTarget); setLoading(true); setError(null); try { const result = await apiClient.request<{ access_token: string }>('/auth/login', { method: 'POST', body: JSON.stringify({ email: form.get('email'), password: form.get('password') }) }); if (!result.data?.access_token) throw new Error('No access token returned'); window.localStorage.setItem('climax_access_token', result.data.access_token); router.replace('/dashboard'); } catch (reason) { setError(reason instanceof Error ? reason.message : 'Sign-in failed'); } finally { setLoading(false); } }
  return <main className="flex min-h-screen items-center justify-center p-4"><form onSubmit={submit} className="w-full max-w-sm rounded-lg border border-climax-border bg-climax-surface p-6 shadow-high"><p className="text-sm font-semibold text-teal-300">ClimaX</p><h1 className="mt-2 text-2xl font-bold text-white">Sign in</h1><p className="mt-1 text-sm text-slate-400">Access municipal and personal environmental tools.</p><label className="mt-5 grid gap-1 text-sm">Email<input required type="email" name="email" className="input"/></label><label className="mt-4 grid gap-1 text-sm">Password<input required type="password" name="password" className="input"/></label><button disabled={loading} className="mt-5 w-full rounded-md bg-teal-500 px-4 py-2 font-semibold text-slate-950 disabled:opacity-50">{loading ? 'Signing in…' : 'Sign in'}</button>{error && <p className="mt-3 text-sm text-rose-300">{error}</p>}</form></main>;
}

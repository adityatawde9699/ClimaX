'use client';

import Script from 'next/script';
import Link from 'next/link';
import { FormEvent, useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowRight, LockKeyhole, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { landingPageForRole, readTokenRole } from '@/lib/auth';

declare global {
  interface Window {
    google?: { accounts: { id: { initialize: (options: { client_id: string; callback: (response: { credential: string }) => void }) => void; renderButton: (element: HTMLElement, options: Record<string, string | number>) => void } } };
  }
}

export default function LoginPage() {
  const router = useRouter(); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  const googleButton = useRef<HTMLDivElement>(null);
  const googleClientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  const finishLogin = useCallback((token: string) => { window.localStorage.setItem('climax_access_token', token); window.dispatchEvent(new Event('climax-auth')); router.replace(landingPageForRole(readTokenRole(token))); router.refresh(); }, [router]);
  const initializeGoogle = useCallback(() => {
    if (!googleClientId || !window.google || !googleButton.current) return;
    window.google.accounts.id.initialize({ client_id: googleClientId, callback: ({ credential }) => { setLoading(true); setError(null); void apiClient.request<{ access_token: string }>('/auth/google', { method: 'POST', body: JSON.stringify({ credential }) }).then((result) => { if (!result.data?.access_token) throw new Error('No access token returned'); finishLogin(result.data.access_token); }).catch((reason) => setError(reason instanceof Error ? reason.message : 'Google sign-in failed')).finally(() => setLoading(false)); } });
    googleButton.current.replaceChildren();
    window.google.accounts.id.renderButton(googleButton.current, { type: 'standard', theme: 'outline', size: 'large', text: 'continue_with', shape: 'rectangular', width: 344 });
  }, [finishLogin, googleClientId]);
  useEffect(() => { initializeGoogle(); }, [initializeGoogle]);
  async function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); const form = new FormData(event.currentTarget); setLoading(true); setError(null); try { const result = await apiClient.request<{ access_token: string }>('/auth/login', { method: 'POST', body: JSON.stringify({ email: form.get('email'), password: form.get('password') }) }); if (!result.data?.access_token) throw new Error('No access token returned'); finishLogin(result.data.access_token); } catch (reason) { setError(reason instanceof Error ? reason.message : 'Sign-in failed'); } finally { setLoading(false); } }
  return <main className="relative grid min-h-screen place-items-center overflow-hidden bg-[#030d17] p-4"><Script src="https://accounts.google.com/gsi/client" strategy="afterInteractive" onLoad={initializeGoogle}/><div className="pointer-events-none absolute left-1/2 top-[-20%] h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-emerald-500/[.07] blur-3xl"/><form onSubmit={submit} className="relative w-full max-w-md rounded-2xl border border-slate-800 bg-[#071521]/95 p-7 shadow-2xl sm:p-9"><div className="flex items-center justify-between"><p className="text-2xl font-extrabold tracking-tight text-white">Clima<span className="text-emerald-400">X</span></p><span className="grid h-9 w-9 place-items-center rounded-lg bg-emerald-500/10 text-emerald-400"><ShieldCheck size={18}/></span></div><p className="page-eyebrow mt-8">Secure access</p><h1 className="mt-1 text-2xl font-bold text-white">Welcome back</h1><p className="mt-2 text-sm leading-6 text-slate-400">Sign in to access municipal and personal environmental intelligence tools.</p><div className="mt-6 flex min-h-10 justify-center" ref={googleButton}/>{!googleClientId && <p className="mt-2 text-center text-xs text-amber-300">Set NEXT_PUBLIC_GOOGLE_CLIENT_ID to enable Google login.</p>}<div className="my-5 flex items-center gap-3 text-[10px] uppercase tracking-widest text-slate-600"><i className="h-px flex-1 bg-slate-800"/>or use email<i className="h-px flex-1 bg-slate-800"/></div><label className="field-label">Email address<input required type="email" name="email" className="input" placeholder="you@organization.gov"/></label><label className="field-label mt-4">Password<div className="relative"><LockKeyhole size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"/><input required type="password" name="password" className="input pl-10" placeholder="Enter your password"/></div></label><button disabled={loading} className="primary-button mt-6 w-full">{loading ? 'Signing in…' : 'Sign in with email'}<ArrowRight size={15}/></button>{error && <p className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 p-3 text-sm text-red-300">{error}</p>}<p className="mt-6 text-center text-sm text-slate-400">New to ClimaX? <Link href="/register" className="font-semibold text-emerald-400 hover:text-emerald-300">Create an account</Link></p><p className="mt-3 text-center text-[10px] text-slate-600">Protected environmental operations system</p></form></main>;
}

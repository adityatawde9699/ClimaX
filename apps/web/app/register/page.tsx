'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { ArrowRight, LockKeyhole, UserPlus } from 'lucide-react';
import { landingPageForRole, type AccountRole } from '@/lib/auth';
import { apiClient } from '@/lib/api-client';

type PublicRole = Exclude<AccountRole, 'ADMIN'>;

const roles: { value: PublicRole; label: string; description: string }[] = [
  { value: 'CITIZEN', label: 'Citizen', description: 'Submit reports and receive local alerts' },
  { value: 'AUTHORITY', label: 'Authority', description: 'Coordinate incidents and public response' },
  { value: 'RESEARCHER', label: 'Researcher', description: 'Explore risk, forecasts, and environmental data' },
];

export default function RegisterPage() {
  const router = useRouter();
  const [role, setRole] = useState<PublicRole>('CITIZEN');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    if (form.get('password') !== form.get('confirm_password')) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.request<{ access_token: string }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          full_name: form.get('full_name'),
          email: form.get('email'),
          password: form.get('password'),
          role,
          authority_registration_code: role === 'AUTHORITY' ? form.get('authority_registration_code') : undefined,
        }),
      });
      if (!result.data?.access_token) throw new Error('No access token returned');
      window.localStorage.setItem('climax_access_token', result.data.access_token);
      window.dispatchEvent(new Event('climax-auth'));
      router.replace(landingPageForRole(role));
      router.refresh();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Account creation failed');
    } finally {
      setLoading(false);
    }
  }

  return <main className="relative grid min-h-screen place-items-center overflow-hidden bg-[#030d17] p-4 py-8">
    <div className="pointer-events-none absolute left-1/2 top-[-20%] h-[650px] w-[650px] -translate-x-1/2 rounded-full bg-emerald-500/[.07] blur-3xl"/>
    <form onSubmit={submit} className="relative w-full max-w-xl rounded-2xl border border-slate-800 bg-[#071521]/95 p-7 shadow-2xl sm:p-9">
      <div className="flex items-center justify-between"><Link href="/login" className="text-2xl font-extrabold tracking-tight text-white">Clima<span className="text-emerald-400">X</span></Link><span className="grid h-9 w-9 place-items-center rounded-lg bg-emerald-500/10 text-emerald-400"><UserPlus size={18}/></span></div>
      <p className="page-eyebrow mt-7">Join the network</p><h1 className="mt-1 text-2xl font-bold text-white">Create your account</h1><p className="mt-2 text-sm leading-6 text-slate-400">Choose the workspace that matches how you use environmental intelligence.</p>
      <div className="mt-6 grid gap-2 sm:grid-cols-3">{roles.map((item) => <button key={item.value} type="button" onClick={() => setRole(item.value)} className={`rounded-xl border p-3 text-left transition ${role === item.value ? 'border-emerald-500/50 bg-emerald-500/10' : 'border-slate-800 bg-[#04111d] hover:border-slate-700'}`}><strong className={`block text-xs ${role === item.value ? 'text-emerald-300' : 'text-slate-200'}`}>{item.label}</strong><span className="mt-1 block text-[10px] leading-4 text-slate-500">{item.description}</span></button>)}</div>
      <div className="mt-5 grid gap-4 sm:grid-cols-2"><label className="field-label">Full name<input required name="full_name" className="input" placeholder="Your full name"/></label><label className="field-label">Email address<input required type="email" name="email" className="input" placeholder="you@example.com"/></label></div>
      <div className="mt-4 grid gap-4 sm:grid-cols-2"><label className="field-label">Password<div className="relative"><LockKeyhole size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"/><input required minLength={12} maxLength={72} type="password" name="password" className="input pl-10" placeholder="At least 12 characters"/></div></label><label className="field-label">Confirm password<input required minLength={12} maxLength={72} type="password" name="confirm_password" className="input" placeholder="Repeat password"/></label></div>
      {role === 'AUTHORITY' && <label className="field-label mt-4">Authority registration code<input required maxLength={255} type="password" name="authority_registration_code" className="input" placeholder="Provided by your platform administrator"/></label>}
      <p className="mt-3 text-[10px] text-slate-500">Administrator accounts are provisioned by an existing administrator.</p>
      <button disabled={loading} className="primary-button mt-6 w-full">{loading ? 'Creating account…' : `Create ${roles.find((item) => item.value === role)?.label} account`}<ArrowRight size={15}/></button>
      {error && <p className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 p-3 text-sm text-red-300">{error}</p>}
      <p className="mt-6 text-center text-sm text-slate-400">Already registered? <Link href="/login" className="font-semibold text-emerald-400 hover:text-emerald-300">Sign in</Link></p>
    </form>
  </main>;
}

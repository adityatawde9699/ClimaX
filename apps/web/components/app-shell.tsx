'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Activity, Bell, ClipboardList, Gauge, Map, Settings, Sparkles } from 'lucide-react';
import { useEffect, useState, type ReactNode } from 'react';

const navigation = [{ href: '/dashboard', label: 'Dashboard', icon: Gauge, roles: ['AUTHORITY', 'ADMIN'] }, { href: '/map', label: 'Live map', icon: Map, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] }, { href: '/reports', label: 'Reports', icon: ClipboardList, roles: ['CITIZEN', 'AUTHORITY', 'ADMIN'] }, { href: '/predictions', label: 'Forecasts', icon: Sparkles, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] }, { href: '/settings', label: 'Settings', icon: Settings, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] }];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState('CITIZEN');
  useEffect(() => { const token = window.localStorage.getItem('climax_access_token'); if (token) { try { setRole(JSON.parse(atob(token.split('.')[1])).role || 'CITIZEN'); } catch { setRole('CITIZEN'); } } }, []);
  useEffect(() => {
    if (['/dashboard', '/settings'].includes(pathname) && !window.localStorage.getItem('climax_access_token')) router.replace('/login');
  }, [pathname, router]);
  if (pathname === '/login') return <>{children}</>;
  const visibleNavigation = navigation.filter((item) => item.roles.includes(role));
  return <div className="min-h-screen bg-climax-bg"><aside className="fixed inset-y-0 left-0 hidden w-60 border-r border-climax-border bg-climax-surface p-5 md:block"><Link href="/dashboard" className="flex items-center gap-2 text-xl font-bold text-white"><Activity className="text-teal-400" />ClimaX</Link><nav className="mt-8 space-y-1">{visibleNavigation.map(({ href, label, icon: Icon }) => <Link key={href} href={href} className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm transition ${pathname === href ? 'bg-teal-500/15 text-teal-300' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}><Icon size={17}/>{label}</Link>)}</nav></aside><main className="pb-20 md:ml-60 md:pb-0"><div className="flex items-center justify-between border-b border-rose-800/50 bg-rose-950/30 px-4 py-2 text-xs text-rose-200"><span>Air quality alert: limit outdoor exposure in high-AQI zones.</span><Bell size={15}/></div>{children}</main><nav className="fixed inset-x-0 bottom-0 z-20 flex justify-around border-t border-climax-border bg-climax-surface p-2 md:hidden">{visibleNavigation.map(({ href, label, icon: Icon }) => <Link key={href} href={href} className={`flex flex-col items-center gap-1 px-2 text-[10px] ${pathname === href ? 'text-teal-300' : 'text-slate-400'}`}><Icon size={18}/>{label}</Link>)}</nav></div>;
}

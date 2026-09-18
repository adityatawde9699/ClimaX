'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  BarChart3,
  Bell,
  ChevronDown,
  ClipboardList,
  Database,
  Flame,
  Globe2,
  Home,
  Languages,
  LogOut,
  Map,
  Menu,
  Search,
  Settings,
  Sparkles,
  X,
} from 'lucide-react';
import { useEffect, useState, useSyncExternalStore, type ReactNode } from 'react';
import { useAlerts, useCurrentUser } from '@/hooks/use-data';
import { readTokenRole } from '@/lib/auth';

const navigation = [
  { href: '/dashboard', label: 'Live Overview', icon: Home, roles: ['AUTHORITY', 'ADMIN'] },
  { href: '/map', label: 'Risk Map', icon: Map, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/hotspots', label: 'Hotspots', icon: Flame, roles: ['AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/predictions', label: 'Forecast', icon: Sparkles, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/alerts', label: 'Alerts', icon: Bell, roles: ['CITIZEN', 'AUTHORITY', 'ADMIN'] },
  { href: '/reports', label: 'Reports', icon: ClipboardList, roles: ['CITIZEN', 'AUTHORITY', 'ADMIN'] },
  { href: '/cross-border', label: 'Cross-Border View', icon: Globe2, roles: ['AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/analytics', label: 'Analytics', icon: BarChart3, roles: ['AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/data-explorer', label: 'Data Explorer', icon: Database, roles: ['AUTHORITY', 'RESEARCHER', 'ADMIN'] },
  { href: '/settings', label: 'Settings', icon: Settings, roles: ['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'] },
];

function Brand() {
  return <Link href="/dashboard" className="inline-flex items-center text-[27px] font-extrabold tracking-tight text-white">Clima<span className="text-emerald-400">X</span></Link>;
}

function subscribeToAuth(callback: () => void) {
  window.addEventListener('storage', callback);
  window.addEventListener('climax-auth', callback);
  return () => {
    window.removeEventListener('storage', callback);
    window.removeEventListener('climax-auth', callback);
  };
}

const getAuthToken = () => window.localStorage.getItem('climax_access_token');
const getServerAuthToken = () => null;

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);
  const [search, setSearch] = useState('');
  const token = useSyncExternalStore(subscribeToAuth, getAuthToken, getServerAuthToken);
  const authenticated = Boolean(token);
  const role = token ? readTokenRole(token) : 'CITIZEN';
  const user = useCurrentUser(authenticated);
  const alerts = useAlerts(authenticated);

  useEffect(() => {
    if (!['/login', '/register'].includes(pathname) && !window.localStorage.getItem('climax_access_token')) router.replace('/login');
  }, [pathname, router]);

  if (['/login', '/register'].includes(pathname)) return <>{children}</>;
  const visibleNavigation = navigation.filter((item) => item.roles.includes(role));
  const active = (href: string) => {
    const [path, query = ''] = href.split('?');
    return pathname === path && !query;
  };

  const sidebar = (
    <>
      <div className="border-b border-slate-800/80 px-5 pb-5 pt-4">
        <Brand />
        <p className="mt-2 max-w-[170px] text-[10px] leading-4 text-slate-400">Federated AI for<br/>Cross-Border Climate Intelligence</p>
      </div>
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {visibleNavigation.map(({ href, label, icon: Icon }) => <Link onClick={() => setMenuOpen(false)} key={href} href={href} className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs transition ${active(href) ? 'border border-emerald-500/15 bg-emerald-500/10 text-emerald-300' : 'border border-transparent text-slate-400 hover:bg-slate-800/60 hover:text-white'}`}><Icon size={16} className={active(href) ? 'text-emerald-400' : 'group-hover:text-slate-200'}/><span className="flex-1">{label}</span>{href === '/alerts' && Boolean(alerts.data?.length) && <span className="grid h-5 min-w-5 place-items-center rounded-full bg-red-500 px-1 text-[9px] font-bold text-white">{alerts.data?.length}</span>}</Link>)}
      </nav>
    </>
  );

  return (
    <div className="min-h-screen bg-[#030d17]">
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-[226px] flex-col border-r border-slate-800/80 bg-[#04111d] lg:flex">{sidebar}</aside>
      {menuOpen && <div className="fixed inset-0 z-50 lg:hidden"><button className="absolute inset-0 bg-black/70" aria-label="Close navigation" onClick={() => setMenuOpen(false)}/><aside className="relative flex h-full w-[270px] flex-col border-r border-slate-800 bg-[#04111d] shadow-2xl"><button onClick={() => setMenuOpen(false)} className="absolute right-3 top-4 rounded-md p-2 text-slate-400 hover:bg-slate-800"><X size={18}/></button>{sidebar}</aside></div>}

      <div className="lg:ml-[226px]">
        <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-slate-800/80 bg-[#04111d]/95 px-3 backdrop-blur md:px-5">
          <button onClick={() => setMenuOpen(true)} className="rounded-md p-2 text-slate-300 hover:bg-slate-800 lg:hidden" aria-label="Open navigation"><Menu size={20}/></button>
          <form onSubmit={(event) => { event.preventDefault(); if (search.trim()) router.push(`/map?q=${encodeURIComponent(search.trim())}`); }} className="relative max-w-2xl flex-1"><Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600" size={16}/><input value={search} onChange={(event) => setSearch(event.target.value)} aria-label="Search location, city, or event" placeholder="Search location, city or event..." className="h-9 w-full rounded-lg border border-transparent bg-[#020b14] pl-10 pr-3 text-xs text-slate-200 outline-none transition placeholder:text-slate-600 focus:border-emerald-500/30"/></form>
          <Link href="/alerts" className="relative rounded-lg p-2 text-slate-300 hover:bg-slate-800" aria-label="Notifications"><Bell size={18}/>{Boolean(alerts.data?.length) && <span className="absolute right-0 top-0 grid h-4 min-w-4 place-items-center rounded-full bg-red-500 px-0.5 text-[8px] font-bold text-white">{alerts.data?.length}</span>}</Link>
          <Link href="/settings" className="hidden items-center gap-2 border-l border-slate-800 pl-4 text-xs text-slate-300 sm:flex"><Languages size={17}/><span>EN</span><ChevronDown size={13}/></Link>
          <div className="hidden h-9 w-px bg-slate-800 md:block" />
          <div className="hidden items-center gap-2 md:flex"><span className="grid h-8 w-8 place-items-center rounded-full bg-gradient-to-br from-slate-200 to-slate-500 text-xs font-bold text-slate-900">{user.data?.full_name?.[0] || '?'}</span><span><strong className="block text-[11px] text-white">{user.data?.full_name || 'Signed-in user'}</strong><small className="block max-w-[115px] truncate text-[9px] text-slate-500">{user.data?.email || 'Profile loading'}</small></span><button title="Sign out" onClick={() => { window.localStorage.removeItem('climax_access_token'); window.dispatchEvent(new Event('climax-auth')); router.replace('/login'); }} className="rounded p-1.5 text-slate-500 hover:bg-slate-800 hover:text-white"><LogOut size={14}/></button></div>
        </header>
        <main>{children}</main>
      </div>

      <nav className="fixed inset-x-0 bottom-0 z-40 flex justify-around border-t border-slate-800 bg-[#04111d]/95 p-2 backdrop-blur lg:hidden">
        {visibleNavigation.slice(0, 5).map(({ href, label, icon: Icon }) => <Link key={href} href={href} className={`flex flex-col items-center gap-1 px-2 text-[9px] ${active(href) ? 'text-emerald-300' : 'text-slate-500'}`}><Icon size={17}/>{label}</Link>)}
      </nav>
    </div>
  );
}

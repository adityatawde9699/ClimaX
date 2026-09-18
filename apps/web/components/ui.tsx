'use client';

import { useMemo, useState, type ReactNode } from 'react';

const aqiBands = [
  [50, 'Good', 'bg-emerald-950 text-emerald-300 border-emerald-700'],
  [100, 'Satisfactory', 'bg-lime-950 text-lime-300 border-lime-700'],
  [200, 'Moderate', 'bg-amber-950 text-amber-300 border-amber-700'],
  [300, 'Poor', 'bg-orange-950 text-orange-300 border-orange-700'],
  [400, 'Very Poor', 'bg-red-950 text-red-300 border-red-700'],
  [Infinity, 'Severe', 'bg-rose-950 text-rose-200 border-rose-700'],
] as const;

export function AqiBadge({ aqi }: { aqi: number }) {
  const [limit, label, className] = aqiBands.find(([limit]) => aqi <= limit) ?? aqiBands[5];
  return <span title={`AQI ${aqi} (${label})`} className={`inline-flex rounded-full border px-2 py-1 text-xs font-semibold ${className}`}>{aqi} · {label}</span>;
}

export function TierBadge({ tier }: { tier: 'OBSERVED' | 'INFERRED' | 'PREDICTED' | 'VERIFIED' }) {
  const styles = { OBSERVED: 'border-emerald-700 bg-emerald-950 text-emerald-300', INFERRED: 'border-indigo-700 bg-indigo-950 text-indigo-300', PREDICTED: 'border-cyan-700 bg-cyan-950 text-cyan-300', VERIFIED: 'border-blue-700 bg-blue-950 text-blue-200' };
  return <span className={`inline-flex rounded-full border px-2 py-1 text-xs font-semibold ${styles[tier]}`}>{tier}</span>;
}

export function SeverityIndicator({ severity }: { severity: string }) {
  const critical = severity === 'CRITICAL';
  const color = critical ? 'bg-rose-500' : severity === 'HIGH' || severity === 'VERY_HIGH' ? 'bg-orange-400' : severity === 'MODERATE' ? 'bg-amber-400' : 'bg-sky-400';
  return <span className="inline-flex items-center gap-2 text-xs font-medium"><i className={`h-2 w-2 rounded-full ${color} ${critical ? 'animate-pulse' : ''}`} />{severity.replace('_', ' ')}</span>;
}

export function MetricCard({ label, value, unit, trend }: { label: string; value: string | number; unit?: string; trend?: string }) {
  return <section className="rounded-lg border border-climax-border bg-climax-surface p-4 shadow-low"><p className="text-xs uppercase tracking-wider text-slate-400">{label}</p><p className="mt-2 font-mono text-3xl font-bold text-white">{value}<span className="ml-1 text-sm font-normal text-slate-400">{unit}</span></p>{trend && <p className="mt-2 text-xs text-emerald-400">{trend}</p>}</section>;
}

export function StatusBadge({ status }: { status: string }) {
  const done = ['RESOLVED', 'COMPLETED', 'MITIGATED'].includes(status);
  return <span className={`rounded-full border px-2 py-1 text-xs ${done ? 'border-emerald-700 bg-emerald-950 text-emerald-300' : 'border-amber-700 bg-amber-950 text-amber-300'}`}>{status.replace('_', ' ')}</span>;
}

export function LoadingSkeleton({ className = '' }: { className?: string }) { return <div className={`animate-pulse rounded bg-slate-800 ${className}`} aria-label="Loading" />; }
export function EmptyState({ icon, message, cta }: { icon: ReactNode; message: string; cta?: ReactNode }) { return <div className="rounded-lg border border-dashed border-climax-border p-8 text-center text-slate-400"><div className="mb-3 text-2xl">{icon}</div><p>{message}</p>{cta && <div className="mt-4">{cta}</div>}</div>; }

export function PageHeader({ eyebrow, title, description, actions }: { eyebrow?: string; title: string; description?: string; actions?: ReactNode }) {
  return <header className="page-header"><div>{eyebrow && <p className="page-eyebrow">{eyebrow}</p>}<h1 className="page-title">{title}</h1>{description && <p className="page-description">{description}</p>}</div>{actions && <div className="flex shrink-0 flex-wrap gap-2">{actions}</div>}</header>;
}

export function DataTable({ columns, rows }: { columns: string[]; rows: ReactNode[][] }) {
  const [sortBy, setSortBy] = useState(0); const [ascending, setAscending] = useState(true); const [page, setPage] = useState(0); const pageSize = 10;
  const sorted = useMemo(() => [...rows].sort((left, right) => `${left[sortBy]}`.localeCompare(`${right[sortBy]}`) * (ascending ? 1 : -1)), [rows, sortBy, ascending]);
  const visible = sorted.slice(page * pageSize, page * pageSize + pageSize); const pages = Math.max(1, Math.ceil(rows.length / pageSize));
  return <div className="overflow-x-auto rounded-lg border border-climax-border"><table className="w-full text-left text-sm"><thead className="bg-climax-subtle text-xs uppercase tracking-wider text-slate-400"><tr>{columns.map((column, index) => <th className="px-4 py-3" key={column}><button onClick={() => { setAscending(index === sortBy ? !ascending : true); setSortBy(index); setPage(0); }} className="hover:text-white">{column}{sortBy === index ? (ascending ? ' ↑' : ' ↓') : ''}</button></th>)}</tr></thead><tbody>{visible.map((row, index) => <tr className="border-t border-climax-border text-slate-200" key={index}>{row.map((cell, cellIndex) => <td className="px-4 py-3" key={cellIndex}>{cell}</td>)}</tr>)}</tbody></table>{pages > 1 && <div className="flex items-center justify-between border-t border-climax-border px-4 py-2 text-xs text-slate-400"><span>Page {page + 1} of {pages}</span><div className="flex gap-2"><button disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button><button disabled={page + 1 === pages} onClick={() => setPage(page + 1)}>Next</button></div></div>}</div>;
}

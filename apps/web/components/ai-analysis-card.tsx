'use client';

import { useState } from 'react';
import { SeverityIndicator, TierBadge } from '@/components/ui';

export type AIAnalysis = { category: string; confidence: number; severity: string; reasoningSteps: string[]; disclaimer: string; plumeBbox?: [number, number, number, number] };

export function AIAnalysisCard({ analysis }: { analysis: AIAnalysis }) {
  const [expanded, setExpanded] = useState(false);
  return <section className="rounded-lg border border-indigo-700/70 bg-indigo-950/20 p-5"><div className="flex flex-wrap items-center justify-between gap-3"><div><TierBadge tier="INFERRED"/><p className="mt-3 text-lg font-semibold text-white">{analysis.category.replaceAll('_', ' ')}</p><p className="text-sm text-indigo-200">{Math.round(analysis.confidence * 100)}% confidence</p></div><SeverityIndicator severity={analysis.severity}/></div>{analysis.plumeBbox && <div className="relative mt-4 h-28 overflow-hidden rounded border border-indigo-800 bg-slate-950"><div className="absolute border-2 border-amber-400" style={{ left: `${analysis.plumeBbox[0] * 100}%`, top: `${analysis.plumeBbox[1] * 100}%`, width: `${(analysis.plumeBbox[2] - analysis.plumeBbox[0]) * 100}%`, height: `${(analysis.plumeBbox[3] - analysis.plumeBbox[1]) * 100}%` }}/></div>}<button onClick={() => setExpanded(!expanded)} className="mt-4 text-sm text-indigo-300 underline">{expanded ? 'Hide evidence' : 'Show evidence'}</button>{expanded && <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-300">{analysis.reasoningSteps.map((step) => <li key={step}>{step}</li>)}</ul>}<p className="mt-4 text-xs italic text-slate-500">{analysis.disclaimer}</p></section>;
}

'use client';

import { FormEvent, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { Camera, FileText, MapPinned, Send, UploadCloud } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { EmptyState, PageHeader, StatusBadge } from '@/components/ui';
import { useReports } from '@/hooks/use-data';
import type { CitizenReport } from '@/types/api';

type UploadGrant = { upload_url: string; media_uri: string; required_headers: Record<string, string> };

export default function ReportsPage() {
  const client = useQueryClient();
  const reports = useReports();
  const [message, setMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [media, setMedia] = useState<File | null>(null);

  async function uploadMedia(file: File): Promise<string> {
    const grant = await apiClient.request<UploadGrant>('/reports/upload-url', { method: 'POST', body: JSON.stringify({ filename: file.name, content_type: file.type, size_bytes: file.size }) });
    if (!grant.data) throw new Error('Storage provider did not return an upload grant.');
    const upload = await fetch(grant.data.upload_url, { method: 'PUT', headers: grant.data.required_headers, body: file });
    if (!upload.ok) throw new Error(`Media upload failed with status ${upload.status}.`);
    return grant.data.media_uri;
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    setSubmitting(true);
    setMessage(null);
    try {
      const mediaUrls = media ? [await uploadMedia(media)] : [];
      await apiClient.request<CitizenReport>('/reports/', { method: 'POST', body: JSON.stringify({ location: { latitude: Number(form.get('latitude')), longitude: Number(form.get('longitude')) }, category: form.get('category'), description: form.get('description'), media_urls: mediaUrls }) });
      await client.invalidateQueries({ queryKey: ['reports'] });
      setMessage('Report and evidence submitted successfully for analysis.');
      setMedia(null);
      formElement.reset();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to submit report. Please sign in and try again.');
    } finally { setSubmitting(false); }
  }

  return <div className="page-wrap max-w-5xl">
    <PageHeader eyebrow="Citizen intelligence" title="Report an environmental issue" description="Share geolocated evidence to help municipal teams detect and respond to pollution events." actions={<span className="secondary-button"><FileText size={15}/>Reporting guide</span>}/>
    <div className="grid gap-6 lg:grid-cols-[1fr_300px]">
      <form onSubmit={submit} className="surface-panel grid gap-5 p-5 sm:p-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4"><span className="grid h-10 w-10 place-items-center rounded-lg bg-emerald-500/10 text-emerald-400"><Camera size={19}/></span><div><h2 className="font-semibold text-white">Observation details</h2><p className="text-xs text-slate-500">Fields marked by the browser are required.</p></div></div>
        <label className="field-label">Category<select name="category" defaultValue="WASTE_INCINERATION" className="input"><option>WASTE_INCINERATION</option><option>INDUSTRIAL_EMISSION</option><option>CONSTRUCTION_DUST</option><option>VEHICULAR_CONGESTION</option><option>OTHER</option></select></label>
        <label className="field-label">What did you observe?<textarea required minLength={10} name="description" className="input min-h-32 resize-y" placeholder="Describe smoke, dust, odour, or other evidence."/></label>
        <div className="grid gap-4 sm:grid-cols-2"><label className="field-label">Latitude<input required name="latitude" type="number" min="-90" max="90" step="any" className="input" placeholder="Latitude"/></label><label className="field-label">Longitude<input required name="longitude" type="number" min="-180" max="180" step="any" className="input" placeholder="Longitude"/></label></div>
        <label className="field-label">Photo or video evidence<span className="flex min-h-24 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-slate-700 bg-[#030d17] p-4 text-center text-slate-400 transition hover:border-emerald-500/50"><UploadCloud size={20}/><span className="mt-2 text-xs">{media ? `${media.name} · ${(media.size / 1_000_000).toFixed(1)} MB` : 'Select JPEG, PNG, WebP, or MP4 up to 10 MB'}</span><input className="sr-only" type="file" accept="image/jpeg,image/png,image/webp,video/mp4" onChange={(event) => setMedia(event.target.files?.[0] ?? null)}/></span></label>
        <button disabled={submitting} className="primary-button"><Send size={15}/>{submitting ? (media ? 'Uploading and submitting…' : 'Submitting…') : 'Submit report'}</button>
        {message && <p className="rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-3 text-sm text-emerald-200">{message}</p>}
      </form>
      <aside className="space-y-4"><section className="surface-panel p-5"><MapPinned className="text-sky-400"/><h2 className="mt-3 font-semibold text-white">Location privacy</h2><p className="mt-2 text-xs leading-5 text-slate-400">Coordinates are used to correlate your observation with nearby sensors and atmospheric conditions.</p></section><section className="surface-panel p-5"><h2 className="font-semibold text-white">What happens next?</h2><ol className="mt-3 space-y-3 text-xs text-slate-400"><li><b className="mr-2 text-emerald-400">01</b>Secure evidence upload</li><li><b className="mr-2 text-emerald-400">02</b>AI and sensor correlation</li><li><b className="mr-2 text-emerald-400">03</b>Authority verification</li></ol></section></aside>
    </div>
    <section className="mt-8"><h2 className="mb-3 font-semibold text-white">Recent reports</h2><div className="surface-panel divide-y divide-slate-800">{reports.data?.length ? reports.data.map((report) => <article key={report.id} className="flex flex-wrap items-center justify-between gap-3 p-4"><div><p className="text-sm font-medium text-white">{report.category.replaceAll('_', ' ')}</p><p className="mt-1 text-xs text-slate-500">{report.description}</p>{report.media_urls.length > 0 && <p className="mt-1 text-[10px] text-sky-400">{report.media_urls.length} evidence file(s) attached</p>}</div><StatusBadge status={report.status}/></article>) : <EmptyState icon={<StatusBadge status="SUBMITTED"/>} message={reports.isLoading ? 'Loading reports…' : 'No reports have been submitted yet.'}/>}</div></section>
  </div>;
}

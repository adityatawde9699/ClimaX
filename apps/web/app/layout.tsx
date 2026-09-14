import type { Metadata } from 'next';
import '../styles/globals.css';
import { AppShell } from '@/components/app-shell';
import { Providers } from './providers';
import 'maplibre-gl/dist/maplibre-gl.css';

export const metadata: Metadata = {
  title: 'ClimaX — Federated AI Environmental Intelligence & Action Platform',
  description: 'AI-powered environmental monitoring, prediction, and municipal action platform.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0B0F17] text-slate-100 antialiased">
        <Providers><AppShell>{children}</AppShell></Providers>
      </body>
    </html>
  );
}

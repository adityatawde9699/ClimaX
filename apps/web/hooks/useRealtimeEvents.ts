'use client';

import { useEffect, useState } from 'react';

export function useRealtimeEvents() {
  const [events, setEvents] = useState<{ event: string; data?: Record<string, unknown> }[]>([]);
  useEffect(() => {
    const token = window.localStorage.getItem('climax_access_token');
    if (!token) return;
    const base = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1').replace('/api/v1', '').replace('http', 'ws');
    let socket: WebSocket | undefined;
    let reconnectTimer: ReturnType<typeof setTimeout> | undefined;
    let attempts = 0;
    let closed = false;
    const connect = () => {
      if (closed || !navigator.onLine) return;
      socket = new WebSocket(`${base}/ws/events?token=${encodeURIComponent(token)}`);
      socket.onopen = () => { attempts = 0; };
      socket.onmessage = ({ data }) => { try { const event = JSON.parse(data); if (event.event !== 'heartbeat') setEvents((current) => [event, ...current].slice(0, 20)); } catch { /* Ignore malformed provider messages. */ } };
      socket.onclose = () => {
        if (closed) return;
        attempts += 1;
        reconnectTimer = setTimeout(connect, Math.min(30_000, 1_000 * 2 ** attempts));
      };
    };
    const reconnectWhenOnline = () => { if (!socket || socket.readyState === WebSocket.CLOSED) connect(); };
    window.addEventListener('online', reconnectWhenOnline);
    connect();
    return () => { closed = true; if (reconnectTimer) clearTimeout(reconnectTimer); window.removeEventListener('online', reconnectWhenOnline); socket?.close(); };
  }, []);
  return events;
}

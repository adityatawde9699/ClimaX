'use client';

import { useEffect, useState } from 'react';

export function useRealtimeEvents() {
  const [events, setEvents] = useState<{ event: string; data?: Record<string, unknown> }[]>([]);
  useEffect(() => {
    const token = window.localStorage.getItem('climax_access_token');
    if (!token) return;
    const base = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1').replace('/api/v1', '').replace('http', 'ws');
    const socket = new WebSocket(`${base}/ws/events?token=${encodeURIComponent(token)}`);
    socket.onmessage = ({ data }) => { try { const event = JSON.parse(data); if (event.event !== 'heartbeat') setEvents((current) => [event, ...current].slice(0, 20)); } catch { /* Ignore malformed provider messages. */ } };
    return () => socket.close();
  }, []);
  return events;
}

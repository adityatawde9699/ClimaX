'use client';
import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
export function useApiData<T>(endpoint: string, fallback: T) { const [data, setData] = useState<T>(fallback); const [loading, setLoading] = useState(true); useEffect(() => { let alive = true; void apiClient.request<T>(endpoint).then((response) => { if (alive && response.data) setData(response.data); }).catch(() => undefined).finally(() => { if (alive) setLoading(false); }); return () => { alive = false; }; }, [endpoint]); return { data, loading }; }

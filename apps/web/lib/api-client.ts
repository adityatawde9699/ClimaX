/**
 * ClimaX Base API Client Architecture
 * 
 * Provides type-safe HTTP transport to FastAPI /api/v1 endpoints.
 * Uses Axios for consistent auth injection and response/error handling.
 */

import type { ApiResponse } from '@climax/types';
import axios, { type AxiosInstance } from 'axios';

export type ApiResult<T> = ApiResponse<T> & { total?: number; page?: number; per_page?: number; total_pages?: number };

export interface ApiClientConfig {
  baseUrl: string;
  timeoutMs?: number;
}

export class ClimaxApiClient {
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly http: AxiosInstance;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl;
    this.timeoutMs = config.timeoutMs ?? 10_000;
    this.http = axios.create({ baseURL: this.baseUrl, timeout: this.timeoutMs });
    this.http.interceptors.request.use((request) => {
      if (typeof window !== 'undefined') {
        const token = window.localStorage.getItem('climax_access_token');
        if (token) request.headers.Authorization = `Bearer ${token}`;
      }
      return request;
    });
    this.http.interceptors.response.use((response) => response, (error) => {
      if (error.response?.status === 401 && typeof window !== 'undefined') window.localStorage.removeItem('climax_access_token');
      const detail = error.response?.data?.detail;
      const validation = Array.isArray(detail) ? detail.map((item: { msg?: string }) => item.msg).filter(Boolean).join(', ') : detail;
      return Promise.reject(new Error(error.response?.data?.error?.message || validation || error.response?.data?.message || error.message || 'Network request failed'));
    });
  }

  public getBaseUrl(): string {
    return this.baseUrl;
  }

  public async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResult<T>> {
    const response = await this.http.request<ApiResult<T> | T>({
      url: endpoint,
      method: options.method,
      data: typeof options.body === 'string' ? JSON.parse(options.body) : options.body,
      headers: options.headers as Record<string, string>,
    });
    const body = response.data;
    if (body && typeof body === 'object' && 'success' in body && 'data' in body) return body as ApiResult<T>;
    return { success: true, data: body as T };
  }
}

export const apiClient = new ClimaxApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
});

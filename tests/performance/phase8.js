import http from 'k6/http';
import { check } from 'k6';

export const options = { vus: 100, duration: '60s', thresholds: { http_req_duration: ['p(99)<500'], http_req_failed: ['rate<0.05'] } };
const base = __ENV.API_URL || 'http://localhost:8000/api/v1';
export default function () {
  check(http.get(`${base}/sensors/nearby?lat=28.6&lng=77.2&radius_m=5000`), { sensors: (r) => r.status === 200 });
  check(http.get(`${base}/incidents/`), { incidents: (r) => r.status === 200 });
}

/** @type {import('next').NextConfig} */
if (process.env.VERCEL === '1' && !/^https:\/\/[^/]+\/api\/v1\/?$/.test(process.env.NEXT_PUBLIC_API_URL || '')) {
  throw new Error('Set NEXT_PUBLIC_API_URL to the public HTTPS API URL ending in /api/v1 before deploying on Vercel.');
}

const nextConfig = {
  // Keep `next dev` assets isolated from `next build`. Running a production
  // build must never replace CSS/JS chunks used by an active dev server.
  distDir: process.env.NEXT_DIST_DIR || '.next',
  output: 'standalone',
  async headers() {
    return [{ source: '/:path*', headers: [{ key: 'Cross-Origin-Opener-Policy', value: 'same-origin-allow-popups' }, { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' }] }];
  },
};

module.exports = nextConfig;

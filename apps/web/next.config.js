/** @type {import('next').NextConfig} */
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

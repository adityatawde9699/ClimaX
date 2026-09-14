/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    // Keep compiler diagnostics in the parent process; it is also more reliable
    // in constrained CI containers where child-process stderr is unavailable.
    webpackBuildWorker: false,
  },
};

module.exports = nextConfig;

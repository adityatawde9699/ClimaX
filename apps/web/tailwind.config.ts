import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './features/**/*.{js,ts,jsx,tsx,mdx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        climax: {
          bg: '#0B0F17',
          surface: '#121824',
          subtle: '#1B2333',
          border: '#2A364F',
          highlight: '#3E5075',
        },
        aqi: {
          good: '#10B981',
          moderate: '#F59E0B',
          unhealthySensitive: '#F97316',
          unhealthy: '#EF4444',
          veryUnhealthy: '#8B5CF6',
          hazardous: '#881337',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: { sm: '4px', md: '8px', lg: '16px', full: '9999px' },
      transitionDuration: { fast: '150ms', normal: '250ms', slow: '400ms' },
      boxShadow: {
        low: '0 1px 2px rgba(0, 0, 0, .35)',
        medium: '0 8px 16px rgba(0, 0, 0, .4)',
        high: '0 20px 25px -5px rgba(0, 0, 0, .7)',
        card: '0 4px 6px -1px rgba(0, 0, 0, .5)',
      },
    },
  },
  plugins: [],
};

export default config;

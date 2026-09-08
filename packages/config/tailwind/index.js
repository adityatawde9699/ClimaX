/** @type {import('tailwindcss').Config} */
module.exports = {
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
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  }
};

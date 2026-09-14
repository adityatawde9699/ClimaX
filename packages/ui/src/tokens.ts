/**
 * ClimaX Operational Design System Tokens
 * 
 * Aesthetic Direction: Government Technology + Environmental Intelligence + Modern Data Platform.
 * Avoids decorative glassmorphism, distracting animations, and low-contrast palettes.
 * Emphasizes high-contrast legibility, rigorous information density, and instant operational recognition.
 */

export const colors = {
  // Brand & Environmental Base (High-contrast slate/zinc neutrals)
  background: {
    primary: '#0B0F17',     // Deep midnight blue/black for command centers
    surface: '#121824',        // High-density elevated panel surface
    surfaceSubtle: '#1B2333',  // Secondary card background
    border: '#2A364F',         // Clean utility border
    borderHighlight: '#3E5075',
  },
  text: {
    primary: '#F8FAFC',        // Slate 50 (maximum contrast)
    secondary: '#94A3B8',      // Slate 400
    muted: '#64748B',          // Slate 500
    inverted: '#0F172A',       // Slate 900
  },
  
  // Standard AQI Severity Scale (CPCB / EPA Standardized Bands)
  aqi: {
    good: {
      range: [0, 50],
      label: 'Good',
      color: '#10B981',       // Emerald 500
      bgSubtle: '#064E3B',
      border: '#047857',
    },
    moderate: {
      range: [51, 100],
      label: 'Moderate',
      color: '#F59E0B',       // Amber 500
      bgSubtle: '#78350F',
      border: '#B45309',
    },
    unhealthySensitive: {
      range: [101, 150],
      label: 'Unhealthy for Sensitive Groups',
      color: '#F97316',       // Orange 500
      bgSubtle: '#7C2D12',
      border: '#C2410C',
    },
    unhealthy: {
      range: [151, 200],
      label: 'Unhealthy',
      color: '#EF4444',       // Red 500
      bgSubtle: '#7F1D1D',
      border: '#B91C1C',
    },
    veryUnhealthy: {
      range: [201, 300],
      label: 'Very Unhealthy',
      color: '#8B5CF6',       // Purple 500
      bgSubtle: '#4C1D95',
      border: '#6D28D9',
    },
    hazardous: {
      range: [301, 500],
      label: 'Hazardous',
      color: '#881337',       // Rose 900 / Maroon
      bgSubtle: '#4C0519',
      border: '#BE123C',
    },
  },

  // Operational Incident Severity Indicators
  severity: {
    LOW: { color: '#38BDF8', label: 'Low', badge: 'bg-sky-950 text-sky-400 border-sky-800' },
    MODERATE: { color: '#FBBF24', label: 'Moderate', badge: 'bg-amber-950 text-amber-400 border-amber-800' },
    HIGH: { color: '#FB923C', label: 'High', badge: 'bg-orange-950 text-orange-400 border-orange-800' },
    VERY_HIGH: { color: '#F87171', label: 'Very High', badge: 'bg-red-950 text-red-400 border-red-800' },
    CRITICAL: { color: '#FDA4AF', label: 'Critical / Emergency', badge: 'bg-rose-950 text-rose-300 border-rose-700 font-bold' },
  },

  // 4-Tier Information Hierarchy Badges
  informationTier: {
    OBSERVED: {
      label: 'Observed Truth',
      description: 'Direct measurement from physical IoT sensor or citizen media',
      badge: 'bg-emerald-950 text-emerald-300 border-emerald-700',
    },
    INFERRED: {
      label: 'AI Inferred',
      description: 'Probabilistic machine learning model deduction',
      badge: 'bg-indigo-950 text-indigo-300 border-indigo-700',
    },
    PREDICTED: {
      label: 'Model Predicted',
      description: 'Spatio-temporal atmospheric plume forecast',
      badge: 'bg-cyan-950 text-cyan-300 border-cyan-700',
    },
    VERIFIED: {
      label: 'Human Verified',
      description: 'Ground truth confirmed by municipal field officer',
      badge: 'bg-blue-950 text-blue-200 border-blue-600',
    },
  },

  // AI Confidence Indicators
  confidence: {
    LOW: { threshold: '< 60%', color: '#94A3B8', bg: 'bg-slate-800 text-slate-400' },
    MEDIUM: { threshold: '60% - 79%', color: '#FBBF24', bg: 'bg-amber-900/60 text-amber-300' },
    HIGH: { threshold: '80% - 94%', color: '#34D399', bg: 'bg-emerald-900/60 text-emerald-300' },
    CRITICAL: { threshold: '≥ 95%', color: '#38BDF8', bg: 'bg-cyan-900/60 text-cyan-200 font-semibold' },
  },
} as const;

export const typography = {
  fontFamily: {
    sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
    mono: ['JetBrains Mono', 'Fira Code', 'monospace'], // Crucial for sensor telemetry and coordinates
  },
  fontSize: {
    xs: '0.75rem',    // 12px - metadata, coordinates, timestamps
    sm: '0.875rem',   // 14px - table rows, labels
    base: '1.0rem',   // 16px - body text
    lg: '1.125rem',   // 18px - card titles
    xl: '1.25rem',    // 20px - section headers
    '2xl': '1.5rem',  // 24px - module headers
    '3xl': '1.875rem',// 30px - KPI values
    '4xl': '2.25rem', // 36px - hero metric displays (e.g. AQI 245)
  },
} as const;

export const spacing = {
  compact: '0.25rem',  // 4px
  dense: '0.5rem',     // 8px - table cells, dense command panels
  regular: '1.0rem',   // 16px
  spacious: '1.5rem',  // 24px
  section: '2.0rem',   // 32px
} as const;

export const transitions = {
  fast: '150ms',
  normal: '250ms',
  slow: '400ms',
} as const;

export const borderRadius = {
  none: '0px',
  sm: '2px',   // Sharp technical look for charts & data tables
  md: '4px',   // Default cards & inputs
  lg: '8px',   // Panels & modals
  full: '9999px', // Pill status badges
} as const;

export const shadows = {
  low: '0 1px 2px rgba(0, 0, 0, 0.35)',
  medium: '0 8px 16px rgba(0, 0, 0, 0.4)',
  high: '0 20px 25px -5px rgba(0, 0, 0, 0.7)',
  card: '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.5)',
  panel: '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.5)',
  elevationHigh: '0 20px 25px -5px rgba(0, 0, 0, 0.7), 0 8px 10px -6px rgba(0, 0, 0, 0.7)',
} as const;

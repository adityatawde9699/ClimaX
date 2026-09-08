/**
 * Standard formatters for ClimaX telemetry and UI display
 */

export function formatAQILabel(aqi: number): {
  label: string;
  category: 'good' | 'moderate' | 'unhealthySensitive' | 'unhealthy' | 'veryUnhealthy' | 'hazardous';
} {
  if (aqi <= 50) return { label: 'Good', category: 'good' };
  if (aqi <= 100) return { label: 'Moderate', category: 'moderate' };
  if (aqi <= 150) return { label: 'Unhealthy for Sensitive Groups', category: 'unhealthySensitive' };
  if (aqi <= 200) return { label: 'Unhealthy', category: 'unhealthy' };
  if (aqi <= 300) return { label: 'Very Unhealthy', category: 'veryUnhealthy' };
  return { label: 'Hazardous', category: 'hazardous' };
}

export function formatConcentration(value?: number, unit: string = 'µg/m³'): string {
  if (value === undefined || value === null) return 'N/A';
  return `${value.toFixed(1)} ${unit}`;
}

export function formatIsoTimestamp(isoString: string): string {
  try {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short',
    });
  } catch {
    return isoString;
  }
}

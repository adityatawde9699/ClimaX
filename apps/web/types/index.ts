export * from '@climax/types';

export interface ViewportState {
  center: [number, number];
  zoom: number;
  pitch?: number;
  bearing?: number;
}

export type ActiveMapLayer = 
  | 'sensors_live'
  | 'plume_predictions'
  | 'satellite_no2'
  | 'citizen_incidents'
  | 'risk_heatmap';

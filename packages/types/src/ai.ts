/**
 * ClimaX Core AI Taxonomy & Trust Contracts
 * 
 * Defines the foundational distinction between raw ground truth, model inferences,
 * future projections, and verified administrative facts.
 */

export type InformationTier = 
  | 'OBSERVED'   // Physical, un-manipulated measurement or raw citizen upload
  | 'INFERRED'   // Probabilistic interpretation output by vision/language models
  | 'PREDICTED'  // Future estimation output by spatio-temporal ML models
  | 'VERIFIED';  // Authority-certified or field-officer confirmed truth

export type VerificationStatus = 
  | 'UNVERIFIED'
  | 'FIELD_VERIFIED'
  | 'REJECTED'
  | 'DISPUTED';

export type ConfidenceTier = 
  | 'LOW'        // 0.00 - 0.59 (Insufficient certainty, advisory only)
  | 'MEDIUM'     // 0.60 - 0.79 (Probable, requires corroborating data)
  | 'HIGH'       // 0.80 - 0.94 (Strong certainty, triggers automated triage)
  | 'CRITICAL';  // 0.95 - 1.00 (Near definitive certainty)

export interface AIExplanationMetadata {
  /** Summary conclusion of the AI analysis */
  result: string;
  /** Normalized confidence score between 0.0 and 1.0 */
  confidence: number;
  /** Confidence categorization tier */
  confidence_tier: ConfidenceTier;
  /** Explicit list of visual, sensor, or meteorological justifications */
  evidence: string[];
  /** Lineage tracking: IDs or URIs of inputs that contributed to this output */
  data_sources: string[];
  /** Model identifier and checkpoint version used */
  model: string;
  /** ISO8601 timestamp of when inference occurred */
  timestamp: string;
  /** Current verification state by human authority */
  verification_status: VerificationStatus;
}

export type PollutionCategory =
  | 'BIOMASS_BURNING'
  | 'INDUSTRIAL_EMISSION'
  | 'VEHICULAR_CONGESTION'
  | 'CONSTRUCTION_DUST'
  | 'WASTE_INCINERATION'
  | 'BRICK_KILN'
  | 'ROAD_DUST'
  | 'FIRE_INCIDENT'
  | 'HAZARDOUS_CHEMICAL'
  | 'OTHER';

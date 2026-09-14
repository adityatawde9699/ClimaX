"""Consumes report-analysis events and persists Gemini inferences."""

import json
from uuid import uuid4

from ai.environmental_reasoner import EnvironmentalReasoningEngine
from ai.multimodal_analyzer import MultimodalReportAnalyzer
from integrations.gcs_adapter import GCSAdapter

from models.entities import AIAnalysis, CitizenReport, Incident


class AIDispatchWorker:
    def __init__(self, publish=None, analyzer: MultimodalReportAnalyzer | None = None):
        self.publish = publish
        self.analyzer = analyzer or MultimodalReportAnalyzer()
        self.gcs = GCSAdapter()

    async def process(self, raw_message: bytes, session) -> bool:
        payload = json.loads(raw_message)
        report = await session.get(CitizenReport, payload.get("report_id"))
        if report is None:
            return False
        media_url = next(iter(report.media_urls), None)
        if not media_url:
            return False
        explanation = await self.analyzer.analyze(
            self.gcs.download_bytes(media_url),
            report.latitude,
            report.longitude,
            report.description,
        )
        analysis = AIAnalysis(
            id=str(uuid4()),
            report_id=report.id,
            tier="INFERRED",
            classification=explanation.pollution_category.value,
            explanation=explanation.model_dump(mode="json"),
            suggested_severity=explanation.suggested_severity,
            confidence_score=explanation.confidence,
            raw_model_response=self.analyzer.last_raw_response,
        )
        session.add(analysis)
        report.status = "TRIAGED"
        if report.incident_id and explanation.suggested_severity in {
            "HIGH",
            "VERY_HIGH",
            "CRITICAL",
        }:
            incident = await session.get(Incident, report.incident_id)
            if incident:
                reasoning = await EnvironmentalReasoningEngine().reason_about_hotspot(
                    {"report_id": report.id}, {}, {}
                )
                incident.root_cause_summary = reasoning.result
        await session.commit()
        if self.publish and explanation.suggested_severity in {"HIGH", "VERY_HIGH", "CRITICAL"}:
            await self.publish(
                "climax-alerts-dispatch", json.dumps({"analysis_id": analysis.id}).encode()
            )
        return True

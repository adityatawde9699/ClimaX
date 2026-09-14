import pytest
from ai.multimodal_analyzer import MultimodalReportAnalyzer


class FakeGemini:
    model_name = "gemini-test"

    async def generate(self, _parts):
        return (
            '{"pollution_category":"CONSTRUCTION_DUST","suggested_severity":"HIGH",'
            '"confidence":0.82,"result":"Dust plume detected",'
            '"reasoning_steps":["Visible haze","Active construction","Low visibility"],'
            '"plume_bbox":[0.1,0.2,0.6,0.7]}',
            20,
        )


@pytest.mark.asyncio
async def test_multimodal_analyzer_returns_inferred_structured_analysis():
    analysis = await MultimodalReportAnalyzer(FakeGemini()).analyze(
        b"image", 28.6, 77.2, "Dust visible near a construction site"
    )
    assert analysis.pollution_category.value == "CONSTRUCTION_DUST"
    assert analysis.confidence == 0.82
    assert analysis.reasoning_steps == ["Visible haze", "Active construction", "Low visibility"]
    assert analysis.plume_bbox == [0.1, 0.2, 0.6, 0.7]

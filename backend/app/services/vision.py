"""Image-based site analysis (Epic 2) using a LLaMA vision model."""
from .. import config, llm
from ..schemas import Defect, ImageAnalysis

SYSTEM = (
    "You are a senior civil engineer and site inspector. Analyse construction site "
    "photos and answer ONLY with a single JSON object, no prose."
)

PROMPT = """Analyse this construction site image. Return JSON with exactly these keys:
{
  "stage": "excavation | foundation | structure | masonry | finishing | completed | unknown",
  "materials": ["visible materials"],
  "defects": [{"type": "...", "severity": "low|medium|high", "description": "..."}],
  "safety_issues": ["e.g. workers without helmets, unprotected edges"],
  "progress_percent": 0-100 integer estimate,
  "summary": "2-3 sentence plain-language summary"
}
Only report what is actually visible. If unsure, say so in the summary."""


def _demo() -> ImageAnalysis:
    return ImageAnalysis(
        stage="structure",
        materials=["reinforced concrete", "steel rebar", "brick masonry"],
        defects=[Defect(type="honeycombing", severity="medium",
                        description="Possible voids near the column base; verify on site.")],
        safety_issues=["No edge protection visible on upper slab"],
        progress_percent=45,
        summary="DEMO MODE: Superstructure appears under way. Set LLM_API_KEY for real analysis.",
        demo_mode=True,
    )


async def analyse_image(image_bytes: bytes, mime: str) -> ImageAnalysis:
    if config.DEMO_MODE:
        return _demo()
    data = await llm.vision_json(SYSTEM, PROMPT, image_bytes, mime)
    data["progress_percent"] = max(0, min(100, int(data.get("progress_percent", 0))))
    return ImageAnalysis(**data)

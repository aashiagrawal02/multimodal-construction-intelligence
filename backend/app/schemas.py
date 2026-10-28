from pydantic import BaseModel, Field


class Defect(BaseModel):
    type: str
    severity: str = Field(description="low | medium | high")
    description: str


class ImageAnalysis(BaseModel):
    stage: str = Field(description="e.g. excavation, foundation, structure, finishing")
    materials: list[str]
    defects: list[Defect]
    safety_issues: list[str]
    progress_percent: int = Field(ge=0, le=100)
    summary: str
    demo_mode: bool = False


class EstimateRequest(BaseModel):
    area_sqft: float = Field(gt=0)
    floors: int = Field(default=1, ge=1, le=50)
    quality: str = Field(default="standard", description="economy | standard | premium")
    city_tier: int = Field(default=2, ge=1, le=3, description="1 = metro, 3 = small town")


class CostLine(BaseModel):
    item: str
    percent: float
    amount: float


class PhaseItem(BaseModel):
    phase: str
    weeks: int


class EstimateResponse(BaseModel):
    built_up_area_sqft: float
    rate_per_sqft: float
    total_cost: float
    breakdown: list[CostLine]
    timeline: list[PhaseItem]
    total_weeks: int
    currency: str = "INR"


class AssistantRequest(BaseModel):
    question: str
    context: dict | None = None


class AssistantResponse(BaseModel):
    answer: str
    demo_mode: bool = False


class VisualizeRequest(BaseModel):
    description: str
    style: str = "photorealistic architectural render"
    width: int = 1024
    height: int = 768
    seed: int | None = None


class VisualizeResponse(BaseModel):
    image_url: str
    prompt: str

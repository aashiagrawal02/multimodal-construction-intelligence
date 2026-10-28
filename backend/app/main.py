import json

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .llm import LLMError
from .schemas import (AssistantRequest, AssistantResponse, EstimateRequest, EstimateResponse,
                      ImageAnalysis, VisualizeRequest, VisualizeResponse)
from .services import assistant, estimator, vision, visualizer

app = FastAPI(title="Multimodal Construction Intelligence Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}


@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": config.DEMO_MODE, "model": config.LLM_MODEL}


@app.post("/api/analyze-image", response_model=ImageAnalysis)
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(400, "Upload a JPEG, PNG or WebP image")
    data = await file.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image larger than 8 MB")
    try:
        return await vision.analyse_image(data, file.content_type)
    except (LLMError, json.JSONDecodeError, ValueError) as e:
        raise HTTPException(502, f"Analysis failed: {e}")


@app.post("/api/estimate", response_model=EstimateResponse)
def estimate(req: EstimateRequest):
    try:
        return estimator.estimate(req)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/assistant", response_model=AssistantResponse)
async def ask(req: AssistantRequest):
    try:
        text, demo = await assistant.answer(req.question, req.context)
    except LLMError as e:
        raise HTTPException(502, str(e))
    return AssistantResponse(answer=text, demo_mode=demo)


@app.post("/api/visualize", response_model=VisualizeResponse)
def visualize(req: VisualizeRequest):
    url, prompt = visualizer.build_image_url(req.description, req.style, req.width, req.height, req.seed)
    return VisualizeResponse(image_url=url, prompt=prompt)

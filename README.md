# Multimodal Construction Intelligence Platform

An AI-assisted platform for construction projects. Upload a site photo to get a stage/defect/safety analysis, estimate cost and timeline, generate design visualisations, and ask a construction advisor questions with your project data as context.

## Features

| Epic | Module | What it does |
|------|--------|--------------|
| 2 | Image analysis | Meta LLaMA vision model detects stage, materials, defects, safety issues and progress % |
| 3 | Planning & valuation | Rule-based INR cost breakdown and phase timeline by area, floors, quality and city tier |
| 4 | AI intelligence layer | `backend/app/llm.py`: single OpenAI-compatible client with structured-JSON extraction |
| 5 | Assistant | Advisory chat that receives the site analysis and cost estimate as context |
| 5 | Visualisation | Pollinations (Flux) image generation from a text description |
| 6 | Interface | React + Vite UI with four tabs |

## Tech stack

Python 3.9+ · FastAPI · React · Vite · Axios · Meta LLaMA (vision + text) · Pollinations / Flux

## Architecture

```
React (Vite) ──Axios──▶ FastAPI ──▶ LLaMA vision/text (OpenAI-compatible API)
                           └──────▶ Pollinations Flux (image URL)
```

## Getting started

### 1. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then add your LLM_API_KEY
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

**Demo mode:** if `LLM_API_KEY` is empty, image analysis and the assistant return mock responses so you can run the whole UI without an account. Cost estimation and visualisation work in both modes.

Any provider serving a Llama vision model through an OpenAI-compatible `/chat/completions` endpoint works (Groq, OpenRouter, Together, ...). See `.env.example`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api` to port 8000.

### 3. Tests

```bash
cd backend
pytest
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Status and demo-mode flag |
| POST | `/api/analyze-image` | Multipart image upload, returns structured analysis |
| POST | `/api/estimate` | Cost and timeline estimate |
| POST | `/api/assistant` | `{question, context}` returns advice |
| POST | `/api/visualize` | `{description}` returns Flux image URL |

## Project structure

```
backend/
  app/
    main.py            # routes
    llm.py             # LLaMA client
    schemas.py         # Pydantic models
    services/          # vision, estimator, assistant, visualizer
  tests/
frontend/
  src/
    api.js             # Axios client
    components/        # one panel per module
```

## Limitations

- Cost rates in `services/estimator.py` are indicative INR figures; tune them for your region.
- AI analysis is advisory only and does not replace a qualified site engineer.

## Roadmap

- Video/drone footage analysis
- Per-project history with a database
- BOQ export to PDF/Excel
- Docker Compose deployment

## License

MIT

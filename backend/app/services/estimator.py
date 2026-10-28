"""Rule-based cost and timeline estimator (Epic 3).

Rates are indicative INR/sq.ft values for Indian residential construction and are
meant to be tuned. Keep them here so they are easy to audit and replace.
"""
from ..schemas import CostLine, EstimateRequest, EstimateResponse, PhaseItem

BASE_RATE = {"economy": 1600, "standard": 2000, "premium": 2800}
CITY_MULTIPLIER = {1: 1.20, 2: 1.00, 3: 0.88}

COST_SPLIT = [
    ("Foundation & earthwork", 0.15),
    ("Structure (RCC, masonry)", 0.30),
    ("Electrical & plumbing", 0.15),
    ("Flooring & finishes", 0.20),
    ("Doors, windows & carpentry", 0.10),
    ("Painting & external works", 0.07),
    ("Contingency", 0.03),
]

# (phase name, share of total duration)
PHASES = [
    ("Planning & approvals", 0.08),
    ("Excavation & foundation", 0.15),
    ("Superstructure", 0.32),
    ("MEP rough-in", 0.12),
    ("Plastering & flooring", 0.16),
    ("Finishing & handover", 0.17),
]


def estimate(req: EstimateRequest) -> EstimateResponse:
    if req.quality not in BASE_RATE:
        raise ValueError(f"quality must be one of {list(BASE_RATE)}")

    built_up = req.area_sqft * req.floors
    rate = BASE_RATE[req.quality] * CITY_MULTIPLIER[req.city_tier]
    total = built_up * rate

    breakdown = [
        CostLine(item=name, percent=round(share * 100, 1), amount=round(total * share, 2))
        for name, share in COST_SPLIT
    ]

    # ~ 10 weeks base + 1 week per 150 sq.ft built-up, minimum 16 weeks
    total_weeks = max(16, round(10 + built_up / 150))
    timeline = [PhaseItem(phase=n, weeks=max(1, round(total_weeks * s))) for n, s in PHASES]

    return EstimateResponse(
        built_up_area_sqft=built_up,
        rate_per_sqft=round(rate, 2),
        total_cost=round(total, 2),
        breakdown=breakdown,
        timeline=timeline,
        total_weeks=sum(p.weeks for p in timeline),
    )

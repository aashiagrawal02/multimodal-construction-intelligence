import io

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import EstimateRequest
from app.services.estimator import estimate

client = TestClient(app)


def test_estimate_totals_are_consistent():
    r = estimate(EstimateRequest(area_sqft=1000, floors=2, quality="standard", city_tier=2))
    assert r.built_up_area_sqft == 2000
    assert r.total_cost == 2000 * 2000
    assert abs(sum(line.amount for line in r.breakdown) - r.total_cost) < 1
    assert r.total_weeks >= 16


def test_premium_costs_more_than_economy():
    lo = estimate(EstimateRequest(area_sqft=1000, quality="economy"))
    hi = estimate(EstimateRequest(area_sqft=1000, quality="premium"))
    assert hi.total_cost > lo.total_cost


def test_health():
    assert client.get("/api/health").status_code == 200


def test_estimate_endpoint_rejects_bad_quality():
    r = client.post("/api/estimate", json={"area_sqft": 900, "quality": "gold"})
    assert r.status_code == 400


def test_visualize_returns_url():
    r = client.post("/api/visualize", json={"description": "two storey house"})
    assert r.status_code == 200
    assert "image.pollinations.ai" in r.json()["image_url"]


def test_analyze_rejects_non_image():
    r = client.post("/api/analyze-image", files={"file": ("a.txt", io.BytesIO(b"hi"), "text/plain")})
    assert r.status_code == 400

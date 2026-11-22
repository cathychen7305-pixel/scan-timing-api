import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def submit(times, deadline=100):
    return client.post("/analyze", json={"timestamps_us": times, "deadline_us": deadline})


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_summary():
    response = submit([0, 100, 260, 350])
    assert response.status_code == 200
    assert response.json() == dict(interval_count=3, deadline_misses=1,
                                   miss_rate_pct=33.333, max_gap_us=160, p95_gap_us=160)


def test_percentile_excludes_single_outlier():
    result = submit([*range(20), 100]).json()
    assert result["p95_gap_us"] == 1
    assert result["max_gap_us"] == 81


def test_maximum_trace():
    result = submit(list(range(10000)), 1).json()
    assert result["interval_count"] == 9999
    assert result["deadline_misses"] == 0


@pytest.mark.parametrize("times", [[], [1], [0, 0], [2, 1], [-1, 1],
                                    [0, True], [0, "1"], [0, 1.5], [0, 2**63],
                                    list(range(10001))], ids=["empty", "single", "duplicate",
                                    "reversed", "negative", "bool", "string", "float",
                                    "overflow", "oversize"])
def test_invalid_trace(times):
    assert submit(times).status_code == 422


@pytest.mark.parametrize("value", [0, -1, True, "100", 1.5])
def test_invalid_deadline(value):
    assert submit([0, 1], value).status_code == 422

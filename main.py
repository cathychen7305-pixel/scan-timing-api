from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from timing import summarize

app = FastAPI(title="Scan Timing API", version="1.0.0")
Timestamp = Annotated[int, Field(strict=True, ge=0, le=2**63 - 1)]


class Trace(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timestamps_us: Annotated[list[Timestamp], Field(min_length=2, max_length=10000)]
    deadline_us: Annotated[int, Field(strict=True, gt=0, le=2**63 - 1)]


class Summary(BaseModel):
    interval_count: int
    deadline_misses: int
    miss_rate_pct: float
    max_gap_us: int
    p95_gap_us: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=Summary)
def analyze(trace: Trace):
    try:
        return summarize(trace.timestamps_us, trace.deadline_us)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

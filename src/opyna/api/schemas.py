"""Esquemas Pydantic de la API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    review: str = Field(..., examples=["La batería dura poco pero la pantalla es excelente."])
    aspects: list[str] = Field(default_factory=lambda: ["batería", "pantalla"])


class AspectSentiment(BaseModel):
    aspect: str
    label: str
    score: float


class AnalyzeResponse(BaseModel):
    review: str
    results: list[AspectSentiment]

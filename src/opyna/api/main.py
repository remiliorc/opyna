"""API FastAPI de Opyna."""
from __future__ import annotations

from fastapi import FastAPI

from opyna import __version__
from opyna.api.schemas import AnalyzeRequest, AnalyzeResponse, AspectSentiment

app = FastAPI(
    title="Opyna API",
    version=__version__,
    description="Inteligencia de cliente sobre reseñas de Amazon (ABSA, temas, IA generativa).",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """Analiza el sentimiento por aspecto de una reseña.

    Stub: de momento devuelve etiquetas neutras. En la Semana 3 se conecta
    con ``opyna.models.absa.analyze_aspect``.
    """
    results = [
        AspectSentiment(aspect=a, label="neutral", score=0.0)
        for a in req.aspects
    ]
    return AnalyzeResponse(review=req.review, results=results)

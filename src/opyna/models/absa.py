"""Análisis de sentimiento basado en aspectos (ABSA) con transformers.

Envuelve un modelo ABSA preentrenado. Dada una reseña y un aspecto
(p.ej. "batería", "pantalla"), devuelve el sentimiento hacia ese aspecto.
"""
from __future__ import annotations

from functools import lru_cache

from opyna.settings import settings


@lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import pipeline
    return pipeline("text-classification", model=settings.model_absa)


def analyze_aspect(review: str, aspect: str) -> dict:
    """Sentimiento de ``review`` hacia ``aspect``.

    El modelo ABSA espera el formato "<texto> [SEP] <aspecto>".
    """
    clf = _load_pipeline()
    result = clf(f"{review} [SEP] {aspect}")[0]
    return {"aspect": aspect, "label": result["label"], "score": result["score"]}

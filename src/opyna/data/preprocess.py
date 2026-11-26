"""Limpieza y normalización básica de reseñas."""
from __future__ import annotations

import re

import pandas as pd

_WS = re.compile(r"\s+")


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    return _WS.sub(" ", text)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve un DataFrame limpio listo para modelar."""
    df = df.copy()
    df["text"] = df["text"].map(clean_text)
    df["title"] = df["title"].map(clean_text)
    df = df[df["text"].str.len() > 0]
    df["review"] = (df["title"] + ". " + df["text"]).str.strip(". ")
    # etiqueta de sentimiento derivada del rating (baseline)
    df["sentiment"] = pd.cut(df["rating"], bins=[0, 2, 3, 5],
                             labels=["negativo", "neutral", "positivo"])
    return df.reset_index(drop=True)

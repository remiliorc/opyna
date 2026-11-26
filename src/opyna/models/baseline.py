"""Baseline de sentimiento: TF-IDF + regresión logística.

Sirve como línea base clásica frente a la que comparar el modelo ABSA.
"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_baseline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_features=50_000)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])

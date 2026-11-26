"""Detección de temas emergentes con BERTopic (stub)."""
from __future__ import annotations

from collections.abc import Sequence


def fit_topics(docs: Sequence[str]):
    """Ajusta un modelo de temas sobre una colección de reseñas."""
    from bertopic import BERTopic

    model = BERTopic(language="multilingual", calculate_probabilities=False)
    topics, _ = model.fit_transform(list(docs))
    return model, topics

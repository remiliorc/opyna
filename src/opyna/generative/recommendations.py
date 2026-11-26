"""Capa generativa: convierte señales de ABSA/temas en recomendaciones (stub).

Recibe un resumen estructurado (aspectos con su sentimiento agregado, temas
emergentes) y produce recomendaciones de negocio en lenguaje natural.
"""
from __future__ import annotations


def build_prompt(aspect_summary: dict, topics: list[str]) -> str:
    return (
        "Eres un analista de producto. A partir de este resumen de opiniones "
        "de clientes, propón 3 recomendaciones de negocio priorizadas.\n\n"
        f"Aspectos y sentimiento: {aspect_summary}\n"
        f"Temas emergentes: {topics}\n"
    )


def recommend(aspect_summary: dict, topics: list[str]) -> str:
    """Devuelve recomendaciones. TODO: conectar con el proveedor LLM elegido."""
    prompt = build_prompt(aspect_summary, topics)
    # Placeholder hasta cablear OpenAI/Anthropic/modelo abierto.
    return f"[PENDIENTE conectar LLM]\n\nPrompt preparado:\n{prompt}"

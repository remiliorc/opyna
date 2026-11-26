"""Panel web con Gradio (stub)."""
from __future__ import annotations

import gradio as gr


def _analyze(review: str, aspects: str) -> str:
    aspect_list = [a.strip() for a in aspects.split(",") if a.strip()]
    return f"[stub] Analizaría {aspect_list} sobre: {review!r}"


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Opyna") as demo:
        gr.Markdown("# Opyna\nInteligencia de cliente sobre reseñas de Amazon.")
        review = gr.Textbox(label="Reseña")
        aspects = gr.Textbox(label="Aspectos (separados por comas)",
                             value="batería, pantalla")
        out = gr.Textbox(label="Resultado")
        gr.Button("Analizar").click(_analyze, [review, aspects], out)
    return demo


if __name__ == "__main__":
    build_ui().launch()

"""Opyna - Capa generativa de recomendaciones de negocio.

Toma los hallazgos estructurados del pipeline (sentimiento por aspecto del ABSA,
temas emergentes de BERTopic y el modelo de utilidad de resenas) y produce
recomendaciones de negocio priorizadas. Dos modos:

  * determinista (0 EUR, reproducible): prioridad = menciones * |neto negativo|.
  * generativo (LLM redactor, p.ej. Gemini): redacta los insights en lenguaje
    natural a partir de la misma tabla estructurada.

El modo determinista es el que se defiende ante el jurado (no depende de un LLM);
el generativo es una capa opcional para pulir la redaccion.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict


# --- Hallazgos por aspecto (salida real del ABSA, 200k resenas) -------------
ASPECTOS = {
    "atencion_cliente": {"neto": -48.1, "menciones": 13258},
    "pantalla":         {"neto": -21.8, "menciones": 15865},
    "bateria":          {"neto": -15.0, "menciones": 27427},
    "rendimiento":      {"neto":  -7.4, "menciones": 14638},
    "envio_embalaje":   {"neto":  -4.1, "menciones": 4640},
    "calidad":          {"neto":   3.6, "menciones": 35103},
    "precio":           {"neto":   6.7, "menciones": 38245},
    "facilidad_uso":    {"neto":  19.0, "menciones": 17422},
}

# Temas emergentes (BERTopic sobre resenas negativas) cruzados con aspectos.
TEMAS = {
    "atencion_cliente": "dejo de funcionar a los pocos meses (durabilidad -> garantia/reembolso)",
    "bateria":          "problemas de carga: cables y cargadores incluidos",
    "rendimiento":      "lentitud, lag y cuelgues",
    "conectividad":     "router/wifi/modem/signal (tema fuera de los 8 aspectos)",
}


@dataclass
class Recomendacion:
    aspecto: str
    tipo: str            # "problema" | "fortaleza"
    neto: float
    menciones: int
    prioridad: float
    tema: str
    accion: str


ACCIONES = {
    "atencion_cliente": "Reforzar postventa (tiempos de respuesta, garantia clara, reembolsos proactivos) y auditar proveedores con mas fallos tempranos.",
    "pantalla":         "Control de calidad de paneles (brillo, pixeles, tactil) y gestion de expectativas de resolucion.",
    "bateria":          "Mejorar cables/cargadores incluidos y autonomia; comunicar expectativas realistas.",
    "rendimiento":      "Optimizacion de firmware y pruebas de estres previas al lanzamiento.",
    "envio_embalaje":   "Embalaje mas protector y seguimiento de entrega en categorias con incidencias.",
    "calidad":          "Vigilar durabilidad (ligada a los fallos tempranos que alimentan el soporte).",
    "precio":           "Reforzar el posicionamiento calidad-precio: es el aspecto mas mencionado y con net positivo.",
    "facilidad_uso":    "Explotar como argumento de venta ('facil de instalar y usar') en fichas y campanas.",
}


def priorizar(aspectos: dict = ASPECTOS) -> list[Recomendacion]:
    """Ordena los aspectos: problemas por menciones*|neto negativo| (desc),
    y luego las fortalezas por neto positivo (desc)."""
    recs = []
    for asp, d in aspectos.items():
        es_problema = d["neto"] < 0
        prioridad = d["menciones"] * abs(d["neto"]) if es_problema else 0.0
        recs.append(Recomendacion(
            aspecto=asp,
            tipo="problema" if es_problema else "fortaleza",
            neto=d["neto"],
            menciones=d["menciones"],
            prioridad=round(prioridad / 1000, 1),
            tema=TEMAS.get(asp, ""),
            accion=ACCIONES.get(asp, ""),
        ))
    problemas = sorted([r for r in recs if r.tipo == "problema"],
                       key=lambda r: r.prioridad, reverse=True)
    fortalezas = sorted([r for r in recs if r.tipo == "fortaleza"],
                        key=lambda r: r.neto, reverse=True)
    return problemas + fortalezas


def exportar_json(recs: list[Recomendacion], ruta: str) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in recs], f, ensure_ascii=False, indent=2)


def construir_prompt(recs: list[Recomendacion]) -> str:
    """Prompt para el LLM redactor a partir de la tabla priorizada."""
    tabla = "\n".join(
        f"- {r.aspecto} ({r.tipo}): neto {r.neto}, {r.menciones} menciones, "
        f"prioridad {r.prioridad}. Tema: {r.tema or 'n/a'}."
        for r in recs
    )
    return (
        "Eres analista de Voz del Cliente. A partir de esta tabla de aspectos "
        "de producto (sentimiento neto, volumen de menciones y prioridad ya "
        "calculada) redacta recomendaciones de negocio priorizadas, en espanol, "
        "orientadas a un comite de producto. Para cada problema: evidencia, "
        "accion concreta e impacto esperado. Anade una seccion de fortalezas a "
        "explotar. Se conciso y accionable.\n\n" + tabla
    )


def redactar_gemini(prompt: str, api_key: str, modelo: str = "gemini-1.5-flash") -> str:
    """Capa generativa opcional. Requiere google-generativeai y una API key
    (el usuario gestiona la clave; no se hardcodea)."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(modelo).generate_content(prompt).text


if __name__ == "__main__":
    recs = priorizar()
    print("PRIORIZACION (modo determinista, 0 EUR):")
    for r in recs:
        print(f"  [{r.prioridad:>6}] {r.aspecto:<18} {r.tipo:<10} neto={r.neto:+.1f} menciones={r.menciones}")
    exportar_json(recs, "recomendaciones.json")
    print("\nrecomendaciones.json generado. Prompt para el LLM listo via construir_prompt().")

"""Opyna - motor de inferencia compartido.

Un unico punto de carga de modelos y logica de analisis, reutilizado por los tres
clientes: la API (FastAPI), el dashboard (Gradio) y el bot (Telegram).

Los modelos se resuelven por variable de entorno para poder apuntar a:
  * IDs del Hugging Face Hub (despliegue en Spaces), o
  * rutas locales (p.ej. los modelos de Google Drive en Colab).
"""
from __future__ import annotations

import os

from transformers import pipeline

# Modelos (sobreescribibles por entorno). En despliegue apuntan al HF Hub;
# en local pueden ser rutas a /content/drive/MyDrive/Opyna_TFM/modelos/...
SENT_MODEL = os.getenv("OPYNA_SENT_MODEL", "rerc86/opyna-sentimiento-200k")
RATE_MODEL = os.getenv("OPYNA_RATE_MODEL", "rerc86/opyna-rating-200k")
ABSA_MODEL = os.getenv("OPYNA_ABSA_MODEL", "yangheng/deberta-v3-base-absa-v1.1")

ASPECTOS = {
    "bateria": ["battery", "charge", "charging", "batteries"],
    "pantalla": ["screen", "display", "resolution", "touchscreen", "lcd"],
    "precio": ["price", "cost", "expensive", "cheap", "overpriced"],
    "calidad": ["quality", "build", "durable", "sturdy", "flimsy"],
    "facilidad_uso": ["easy to use", "intuitive", "user-friendly", "setup", "install"],
    "envio_embalaje": ["shipping", "packaging", "delivery", "packaged"],
    "atencion_cliente": ["customer service", "warranty", "refund", "support"],
    "rendimiento": ["performance", "fast", "slow", "lag", "responsive"],
}
ASP_EN = {
    "bateria": "battery", "pantalla": "screen", "precio": "price",
    "calidad": "build quality", "facilidad_uso": "ease of use",
    "envio_embalaje": "shipping", "atencion_cliente": "customer service",
    "rendimiento": "performance",
}
SENT_MAP = {"LABEL_0": "Negativo", "LABEL_1": "Neutral", "LABEL_2": "Positivo"}
ACCIONES = {
    "atencion_cliente": "Reforzar postventa (tiempos de respuesta, garantia clara, reembolsos proactivos).",
    "pantalla": "Control de calidad de paneles y gestion de expectativas de resolucion.",
    "bateria": "Mejorar cables/cargadores incluidos y autonomia; comunicar expectativas realistas.",
    "rendimiento": "Optimizacion de firmware y pruebas de estres previas al lanzamiento.",
    "envio_embalaje": "Embalaje mas protector y seguimiento de entrega.",
    "calidad": "Vigilar durabilidad (ligada a los fallos tempranos que alimentan el soporte).",
}


class OpynaAnalyzer:
    """Carga los modelos una sola vez y analiza reseñas."""

    def __init__(self, device: int = -1):
        self.sent = pipeline("text-classification", model=SENT_MODEL,
                             device=device, truncation=True, max_length=256)
        self.rate = pipeline("text-classification", model=RATE_MODEL,
                             device=device, truncation=True, max_length=256)
        self.absa = pipeline("text-classification", model=ABSA_MODEL,
                             device=device, truncation=True, max_length=256)

    def analizar(self, texto: str) -> dict:
        # --- Traduccion automatica ES->EN sin dependencias externas ---
        def _es_espanol(t):
            if any(c in t for c in u"áéíóúñüÁÉÍÓÚÑÜ¿¡"):
                return True
            _pal = {"la","el","los","las","un","una","muy","pero","fue","es","son","que","de","del","por","con","no","al","se","lo","este","esta","mas","pesimo","malo","bueno","calidad","precio","envio","pantalla","bateria","atencion","cliente","producto","compra","funciona","dura","tarde","caro","barato"}
            _w = set((t or "").lower().replace(",", " ").replace(".", " ").split())
            return len(_w & _pal) >= 2
        if _es_espanol(texto):
            if not hasattr(self, "_trad_md") or self._trad_md is None:
                from transformers import AutoTokenizer as _ATk
                from transformers import AutoModelForSeq2SeqLM as _AM
                _M = "Helsinki-NLP/opus-mt-es-en"  # en CPU: preserva cuota ZeroGPU
                self._trad_tk = _ATk.from_pretrained(_M)
                self._trad_md = _AM.from_pretrained(_M)
            _b = self._trad_tk([texto], return_tensors="pt", truncation=True, max_length=512)
            _o = self._trad_md.generate(**_b, max_length=512)
            texto = self._trad_tk.batch_decode(_o, skip_special_tokens=True)[0]
        # --- Fin traduccion ---
        t = (texto or "").strip()
        if len(t) < 3:
            return {"error": "Texto demasiado corto."}
        s = self.sent(t)[0]
        r = self.rate(t)[0]
        low = t.lower()
        aspectos, recomendaciones = [], []
        for asp, kws in ASPECTOS.items():
            if any(k in low for k in kws):
                etiqueta = self.absa(f"{t} [SEP] {ASP_EN[asp]}")[0]["label"]
                aspectos.append({"aspecto": asp, "sentimiento": etiqueta})
                if etiqueta == "Negative" and asp in ACCIONES:
                    recomendaciones.append({"aspecto": asp, "accion": ACCIONES[asp]})
        return {
            "sentimiento": SENT_MAP.get(s["label"], s["label"]),
            "confianza": round(float(s["score"]), 3),
            "rating_estimado": int(r["label"].split("_")[-1]) + 1,
            "aspectos": aspectos,
            "recomendaciones": recomendaciones,
        }

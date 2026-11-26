"""Opyna - Calculadora de ROI (caso de negocio, seccion 8).

Modelo transparente y parametrizable: a partir de supuestos declarados sobre el
vendedor (ingresos, devoluciones, coste de VoC evitado y coste de operar Opyna)
calcula el valor anual, el ROI y el payback, con tres escenarios de sensibilidad.

No pretende dar una cifra cerrada, sino un orden de magnitud defendible: basta
cambiar los supuestos para recalcular.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Supuestos:
    ingresos_anuales: float = 10_000_000.0
    pedido_medio: float = 50.0
    resenas_anuales: int = 120_000
    tasa_devolucion: float = 0.10          # 10% de los pedidos
    coste_por_devolucion: float = 40.0     # logistica + inspeccion + margen perdido
    reduccion_devoluciones: float = 0.10   # relativa, al actuar sobre lo priorizado
    coste_voc_evitado: float = 25_000.0    # SaaS/manual que Opyna sustituye
    coste_opyna_anual: float = 1_000.0     # computo + hosting + LLM
    uplift_conversion: float = 0.0         # p.ej. 0.005 = +0,5% de ingresos


def calcular(s: Supuestos) -> dict:
    pedidos = s.ingresos_anuales / s.pedido_medio
    devoluciones = pedidos * s.tasa_devolucion
    coste_devoluciones = devoluciones * s.coste_por_devolucion
    ahorro_devoluciones = coste_devoluciones * s.reduccion_devoluciones
    ahorro_analisis = max(s.coste_voc_evitado - s.coste_opyna_anual, 0.0)
    valor_retencion = s.ingresos_anuales * s.uplift_conversion
    valor_total = ahorro_devoluciones + ahorro_analisis + valor_retencion
    beneficio_neto = valor_total - s.coste_opyna_anual
    roi = beneficio_neto / s.coste_opyna_anual if s.coste_opyna_anual else float("inf")
    payback_dias = 365 * s.coste_opyna_anual / valor_total if valor_total else float("inf")
    return {
        "pedidos": round(pedidos),
        "devoluciones": round(devoluciones),
        "coste_devoluciones": round(coste_devoluciones),
        "ahorro_devoluciones": round(ahorro_devoluciones),
        "ahorro_analisis": round(ahorro_analisis),
        "valor_retencion": round(valor_retencion),
        "valor_total": round(valor_total),
        "beneficio_neto": round(beneficio_neto),
        "roi_x": round(roi, 1),
        "payback_dias": round(payback_dias, 1),
    }


ESCENARIOS = {
    "conservador": Supuestos(reduccion_devoluciones=0.05, coste_voc_evitado=1_000.0),
    "base":        Supuestos(),
    "optimista":   Supuestos(reduccion_devoluciones=0.15, uplift_conversion=0.005),
}


if __name__ == "__main__":
    for nombre, s in ESCENARIOS.items():
        r = calcular(s)
        print(f"[{nombre:>11}] valor {r['valor_total']:>9,} EUR/anio | "
              f"ROI {r['roi_x']:>6}x | payback {r['payback_dias']} dias")

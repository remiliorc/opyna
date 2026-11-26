# Opyna — Caso de negocio y ROI

*Modelo ilustrativo con supuestos conservadores y declarados. El objetivo no es un número exacto, sino mostrar el orden de magnitud del retorno y que la lógica es defendible y ajustable (ver `opyna_roi.py`).*

## El problema, en números

Un vendedor de electrónica de tamaño medio recibe decenas de miles de reseñas al año en texto libre. Leerlas y clasificarlas a mano por aspecto (precio, batería, pantalla, soporte…) no escala: a un ritmo realista de ~30 reseñas/hora con etiquetado cuidadoso, 120.000 reseñas/año son ~4.000 horas de analista. En la práctica, las empresas **no las leen todas** —muestrean o las ignoran— y pierden la señal justo donde está el problema. Las herramientas comerciales de Voice of Customer cubren ese hueco, pero a un coste de decenas de miles de euros al año.

## Dos palancas de valor

**1. Ahorro en el análisis.** Opyna sustituye el análisis manual/SaaS por un pipeline automático cuyo coste marginal es mínimo (cómputo + hosting + una API de LLM opcional). Es el ahorro más **robusto y directo**.

**2. Reducción de devoluciones y churn.** Es la palanca grande, pero depende de que la marca **actúe** sobre lo que Opyna prioriza. En este dataset, el problema nº1 es **atención al cliente** (neto −48), alimentado por el tema *"dejó de funcionar a los pocos meses"* (durabilidad → devoluciones y garantías). Actuar ahí reduce devoluciones y protege la retención.

## Supuestos del escenario base (declarados)

| Parámetro | Valor | Comentario |
|---|---|---|
| Ingresos anuales | 10.000.000 € | Vendedor de tamaño medio |
| Pedido medio | 50 € | → 200.000 pedidos/año |
| Reseñas/año | 120.000 | ~10.000/mes |
| Tasa de devolución | 10 % | → 20.000 devoluciones/año |
| Coste por devolución | 40 € | Logística + inspección + pérdida de margen |
| Coste devoluciones/año | 800.000 € | Base sobre la que se actúa |
| Reducción de devoluciones vía Opyna | 10 % relativo | Al priorizar y corregir los problemas top |
| Coste VoC evitado (SaaS/manual) | 25.000 €/año | Alternativa que Opyna sustituye |
| Coste de operar Opyna | ~1.000 €/año | Cómputo + hosting + LLM (el desarrollo fue el TFM, <100 €) |

## Resultado — escenario base

- **Ahorro por menos devoluciones:** 20.000 × 10 % × 40 € = **80.000 €/año**
- **Ahorro en análisis (VoC evitado):** 25.000 − 1.000 = **24.000 €/año**
- **Valor total:** ≈ **104.000 €/año** · **Coste:** ≈ 1.000 €/año
- **ROI ≈ 100× (payback en días).** Aun siendo 10 veces demasiado optimistas, el retorno sigue siendo claramente positivo.

## Sensibilidad

| Escenario | Reducción devoluciones | Ahorro análisis | Retención | Valor anual |
|---|---|---|---|---|
| Conservador | 5 % (40.000 €) | 0 € (no había VoC) | — | **~40.000 €** |
| Base | 10 % (80.000 €) | 24.000 € | — | **~104.000 €** |
| Optimista | 15 % (120.000 €) | 24.000 € | +0,5 % conversión (~50.000 €) | **~194.000 €** |

Incluso en el escenario conservador, el valor (~40.000 €) frente a un coste de ~1.000 € deja un retorno de dos órdenes de magnitud.

## Qué aporta Opyna (y qué no)

Opyna **identifica y prioriza dónde actuar** —qué aspecto, respaldado por volumen y sentimiento, y con el problema concreto detrás vía BERTopic— y automatiza a coste casi nulo un análisis que a mano no escala. **No arregla el producto por sí mismo**: la palanca de devoluciones se materializa solo si la marca ejecuta las mejoras. Por eso el caso de negocio separa la palanca robusta (ahorro de análisis) de la palanca de alto impacto pero dependiente de ejecución (devoluciones/retención).

## Reproducibilidad

Los números salen de un modelo parametrizable (`opyna_roi.py`): basta cambiar los supuestos (ingresos, tasa de devolución, reducción esperada…) para recalcular el ROI y la sensibilidad. Es un modelo transparente, no una cifra cerrada.

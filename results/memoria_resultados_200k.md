# Opyna - Memoria de resultados (200.000 resenas, GPU A100)

_Generado: 2026-07-11 17:29_

Pipeline reproducible sobre **Amazon Reviews 2023** (Electronics), 200.000 resenas balanceadas.

## 0. Datos
- 200,000 resenas balanceadas (40.000/estrella) de Amazon Electronics.
- Columnas: rating, title, text, asin, parent_asin, timestamp, helpful_vote, verified_purchase.
- Copia guardada en Drive: `resultados/reviews_electronics_200k.parquet`

## 1. EDA
- Total 200,000 resenas, **0 nulos** en columnas clave.
- Compra verificada: **84.9%**.
- Longitud: mediana 44.0 palabras / media 76.7.
- Helpful votes: media 1.68, 29.8% con >=1 voto.
- Longitud media por estrella: {1: 67.5, 2: 83.6, 3: 84.0, 4: 88.4, 5: 60.2}.
- Guardado: `resultados/eda_200k.json`

## 2. Baseline (TF-IDF ngram(1,2) min_df=5 + Regresion Logistica balanceada, split 80/20)
- **Accuracy 0.767 / F1-macro 0.734**.
```
              precision    recall  f1-score   support

    negativo      0.831     0.789     0.809     16000
     neutral      0.487     0.589     0.533      8000
    positivo      0.882     0.836     0.858     16000

    accuracy                          0.767     40000
   macro avg      0.733     0.738     0.734     40000
weighted avg      0.783     0.767     0.774     40000

```
- Guardado: `resultados/baseline_200k.txt`

## 3. Sentimiento (DistilBERT fine-tuned, 3 clases, 2 epocas, batch 64)
- **Accuracy 0.818 / F1-macro 0.768** (entreno 5.5 min en A100).
```
              precision    recall  f1-score   support

    negativo      0.821     0.900     0.859     16000
     neutral      0.613     0.491     0.545      8000
    positivo      0.898     0.900     0.899     16000

    accuracy                          0.818     40000
   macro avg      0.777     0.764     0.768     40000
weighted avg      0.810     0.818     0.812     40000

```
- Modelo guardado en Drive: `modelos/sentimiento_200k/`

## 4. Rating 5 estrellas (DistilBERT fine-tuned, 2 epocas, batch 64)
- **Accuracy exacta 0.649 / F1-macro 0.648 / Accuracy +-1 estrella 0.958**.
```
              precision    recall  f1-score   support

          1*      0.699     0.717     0.708      8000
          2*      0.526     0.555     0.540      8000
          3*      0.577     0.549     0.563      8000
          4*      0.664     0.600     0.630      8000
          5*      0.776     0.824     0.799      8000

    accuracy                          0.649     40000
   macro avg      0.648     0.649     0.648     40000
weighted avg      0.648     0.649     0.648     40000

```
- Modelo guardado en Drive: `modelos/rating_200k/`

## 5. ABSA - Sentimiento por aspecto (DeBERTa deberta-v3-base-absa-v1.1)
- 166,598 pares resena x aspecto en 12.9 min (A100).
- Distribucion global: Negative 84,712, Positive 76,612, Neutral 5,274.
- Sentimiento neto (Pos-Neg) por aspecto: atencion_cliente -48 | pantalla -22 | bateria -15 | rendimiento -7 | envio_embalaje -4 | calidad +4 | precio +7 | facilidad_uso +19.
```
sentimiento       Negative  Neutral  Positive  menciones  neto
aspecto                                                       
atencion_cliente      73.5      1.1      25.4      13258 -48.1
pantalla              57.6      6.6      35.8      15865 -21.8
bateria               53.5      8.1      38.5      27427 -15.0
rendimiento           52.9      1.6      45.5      14638  -7.4
envio_embalaje        51.1      1.9      47.0       4640  -4.1
calidad               47.6      1.2      51.2      35103   3.6
precio                45.4      2.5      52.1      38245   6.7
facilidad_uso         40.0      1.0      59.0      17422  19.0
```
- Guardado: `resultados/absa_resultados_200k.parquet`, `resultados/absa_por_aspecto_200k.csv`, `figuras/absa_por_aspecto_200k.png`


## 6. Validacion ABSA (gold set)
- Muestra estratificada de 160 pares (20/aspecto) para etiquetado humano ciego.
- Ficheros: absa_goldset_etiquetar_200k.csv (a rellenar) y absa_goldset_clave_200k.csv.

## 7. Validacion ABSA vs anotador LLM (Claude)
- 160 pares etiquetados por Claude como anotador independiente (LLM-as-annotator, NO ground-truth humano).
- **Acuerdo con DeBERTa: accuracy 0.756 / F1-macro 0.589**.
- Validacion orientativa por LLM; para rigor pleno se recomienda ademas etiquetado humano.
```
              precision    recall  f1-score   support

    Negative      0.811     0.948     0.874        77
     Neutral      0.400     0.067     0.114        30
    Positive      0.708     0.868     0.780        53

    accuracy                          0.756       160
   macro avg      0.640     0.628     0.589       160
weighted avg      0.700     0.756     0.700       160

```


## 8. Modelo predictivo de utilidad de reseña (helpful)
Tarea supervisada binaria: predecir si una reseña recibira >=1 voto de utilidad. Refuerza el objetivo del TFM (predecir) con lectura de negocio (priorizar reseñas utiles en el dashboard).
- Datos: 200k reseñas; target helpful_vote>=1 (base rate 29.8%).
- Modelo: TF-IDF(1-2g)+metadatos + LogReg balanceada calibrada (isotonica).
- Test (40k): accuracy 0.744 | F1-macro 0.628 | ROC-AUC 0.746 | PR-AUC 0.569 | Brier 0.174.
- Artefactos: modelos/helpful_200k.joblib, figuras/helpful_eval_200k.png, resultados/helpful_200k.txt.
- Caveat: helpful_vote sesgado a cero y correlacionado con visibilidad/antiguedad; el modelo capta señal de contenido util, no causalidad.

## 8. Modelo predictivo utilidad (helpful, balanceado + calibrado)
- Target helpful_vote>=1 (base 29.8%). TF-IDF+meta+LogReg balanceada, calibrada isotonica.
- Test: acc 0.744 | F1m 0.628 | ROC-AUC 0.746 | PR-AUC 0.569 | Brier 0.174.
- Artefactos: modelos/helpful_200k.joblib, resultados/helpful_200k.txt.

## 9. Temas/problemas emergentes (BERTopic) - cumple 5.3 de la propuesta
- Fase de inteligencia (no supervisada): agrupamiento de resenas negativas (rating<=2, n=15000).
- headphones, ear, sound, br, ears (1183 resenas) -> aspecto: -
- charge, battery, cable, charger, cord (1112 resenas) -> aspecto: bateria
- work, working, stopped, money, months (1064 resenas) -> aspecto: precio
- camera, br, cameras, lens, br br (1062 resenas) -> aspecto: -
- tv, br, remote, tablet, br br (928 resenas) -> aspecto: -
- star, stars, work, star did, didn (763 resenas) -> aspecto: -
- sound, speakers, speaker, quality, sound quality (538 resenas) -> aspecto: calidad
- case, ipad, cover, fit, like (479 resenas) -> aspecto: -
- router, wifi, br, modem, signal (468 resenas) -> aspecto: -
- drive, br, computer, br br, windows (414 resenas) -> aspecto: -
- Caveat: muestra balanceada por estrellas, no es corte temporal; seguimiento temporal como linea futura.
- Artefactos: modelos/bertopic_negativas_200k, figuras/temas_emergentes_200k.png, resultados/temas_emergentes_200k.csv.

## 10. Baseline ensemble (TF-IDF 30k + LightGBM) - completa 5.1 (lineales y ensemble)
- Mismo split 80/20 (seed 42), 3 clases neg/neu/pos. TF-IDF reducido a 30k features por tratabilidad del boosting.
- LightGBM (200 arboles): acc 0.771 / F1-macro 0.707 (entreno 5.4 min).
- Comparativa 3-clases (acc/F1m): LogReg 0.767/0.734 | LightGBM 0.771/0.707 | DistilBERT 0.818/0.768.
- Guardado: resultados/baseline_ensemble_200k.txt

## 11. Interpretabilidad (6): SHAP (lineal) + atencion (DistilBERT)
- SHAP (LinearExplainer) sobre TF-IDF(20k)+LogReg; tokens mas influyentes por clase:
  - negativo: great, not, good, three stars, works, stars, nice, two stars, well, but, no, love
  - neutral: three stars, but, three, not, this, great, five stars, two stars, and, okay, four stars, my
  - positivo: great, not, three stars, good, works, nice, my, well, love, five stars, perfect, three
- Atencion del transformer (ultima capa, CLS->tokens) en ejemplos:
  - The battery drains way too fast and the screen is dim, very  -> pred negativo | atiende: disappointed, very, the, is, and, the
  - Excellent sound quality and easy setup, works perfectly. -> pred positivo | atiende: perfectly, excellent, works, ., easy, ,

## 12. Capa generativa de recomendaciones (2a)
- Priorizacion determinista (menciones x |neto negativo|) + capa LLM opcional (Gemini).
- Entregables: resultados/recomendaciones.md, resultados/recomendaciones.json, opyna_recomendaciones.py.

## 13. Caso de negocio / ROI (8 de la propuesta)
- Modelo parametrizable (opyna_roi.py). Escenario base: valor ~104.000 EUR/anio, coste ~1.000 EUR, ROI ~100x.
- Palanca robusta: ahorro de analisis (VoC evitado). Palanca de impacto: reduccion de devoluciones (soporte/durabilidad).
- Entregables: resultados/caso_negocio_roi.md, resultados/roi_escenarios.json, opyna_roi.py.

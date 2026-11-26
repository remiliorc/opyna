# -*- coding: utf-8 -*-
"""Guia de integracion API de Opyna (ES/EN) -- contrato verificado contra el Space."""
from weasyprint import HTML

SPACE = "rerc86/opyna"

CSS = """
@page {
  size: A4;
  margin: 16mm 15mm 20mm 15mm;
  @bottom-center {
    content: "%FOOT% \\00b7  p\\00e1g. " counter(page) " / " counter(pages);
    font-family: Helvetica, Arial, sans-serif; font-size: 7pt; color: #94a3b8;
    border-top: 0.5pt solid #e2e8f0; padding-top: 4pt; width: 100%;
  }
}
* { box-sizing: border-box; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 9.5pt; color: #334155; line-height: 1.5; margin: 0; }
h1 { font-size: 20pt; color: #7a1f2b; margin: 0 0 2pt 0; letter-spacing: -0.5pt; }
.sub { font-size: 7.5pt; color: #64748b; letter-spacing: 2.5pt; text-transform: uppercase; margin-bottom: 10pt; }
.hero { background: #fff1f2; border: 1pt solid #fecdd3; border-radius: 6pt; padding: 10pt 14pt; margin-bottom: 12pt; }
.hero p { margin: 0; font-size: 9.5pt; color: #7a1f2b; }
h2 { font-size: 13pt; color: #7a1f2b; margin: 15pt 0 6pt 0; padding-left: 7pt;
     border-left: 3.5pt solid #7a1f2b; page-break-after: avoid; }
h3 { font-size: 8pt; color: #7a1f2b; text-transform: uppercase; letter-spacing: 1.2pt;
     margin: 11pt 0 5pt 0; page-break-after: avoid; }
p { margin: 0 0 7pt 0; }
.code { background: #0f172a; color: #e2e8f0; font-family: "DejaVu Sans Mono", Courier, monospace;
        font-size: 7pt; line-height: 1.45; padding: 8pt 10pt; white-space: pre-wrap;
        word-break: break-word; page-break-inside: avoid; border-radius: 5pt; margin: 4pt 0 8pt 0; }
.k { color: #c4b5fd; } .s { color: #86efac; } .f { color: #7dd3fc; }
.n { color: #fdba74; } .c { color: #64748b; }
table.t { width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 8pt; }
table.t th { background: #f8fafc; color: #64748b; font-size: 6.8pt; font-weight: bold;
             letter-spacing: 1pt; text-transform: uppercase; text-align: left; padding: 6pt 8pt;
             border-bottom: 1pt solid #e2e8f0; }
table.t td { padding: 5pt 8pt; border-bottom: 0.5pt solid #f1f5f9; vertical-align: top; }
code.fn { font-family: "DejaVu Sans Mono", Courier, monospace; font-size: 7.5pt; color: #1d4ed8;
          background: #eff6ff; padding: 1pt 4pt; border-radius: 3pt; }
span.ft { font-family: "DejaVu Sans Mono", Courier, monospace; font-size: 7.5pt; color: #b45309; }
.card { border: 1pt solid #e2e8f0; border-radius: 6pt; padding: 9pt 11pt; margin-bottom: 8pt;
        page-break-inside: avoid; }
.card .ti { font-size: 10.5pt; font-weight: bold; color: #0f172a; margin: 0; }
.card .st { font-size: 7.5pt; color: #7a1f2b; font-weight: bold; margin: 1pt 0 5pt 0; }
.card .d { font-size: 8.5pt; color: #64748b; margin: 0 0 5pt 0; }
.tag { float: right; font-size: 6.5pt; color: #475569; text-transform: uppercase;
       letter-spacing: 1pt; font-weight: bold; }
.warn { background: #fffbeb; border: 1pt solid #fde68a; border-radius: 5pt;
        padding: 8pt 11pt; font-size: 8.5pt; color: #78350f; margin: 8pt 0; }
.note { background: #fff1f2; border: 1pt solid #fecdd3; border-radius: 5pt;
        padding: 8pt 11pt; font-size: 8.5pt; color: #7a1f2b; margin-top: 10pt; }
.fin { border-top: 1pt solid #e2e8f0; margin-top: 12pt; padding-top: 8pt;
       text-align: center; font-size: 8pt; color: #94a3b8; }
""".replace("%FOOT%", "TFM M\u00e1ster Big Data, Data Science e Inteligencia Artificial \\00b7  UCM - NTIC "
            "\\00b7  2026 \\00b7  Rogelio Emilio Rivero Contreras")

CLIENTE = {
 "es": ('<span class="c"># pip install gradio_client</span>\n'
        '<span class="k">from</span> gradio_client <span class="k">import</span> Client\n\n'
        '<span class="c"># El Space esta protegido: hacen falta credenciales</span>\n'
        'client = Client(<span class="s">"' + SPACE + '"</span>, auth=(<span class="s">"USUARIO"</span>, <span class="s">"CLAVE"</span>))\n\n'
        '<span class="k">def</span> <span class="f">analizar</span>(texto: str) -&gt; dict:\n'
        '    <span class="s">"""Devuelve sentimiento, rating, aspectos y recomendaciones."""</span>\n'
        '    <span class="k">return</span> client.predict(texto, api_name=<span class="s">"/predict_json"</span>)\n\n'
        'res = analizar(<span class="s">"La bater&iacute;a dura muy poco y la atenci&oacute;n al cliente fue p&eacute;sima"</span>)\n'
        'print(res[<span class="s">"sentimiento"</span>])       <span class="c"># Negativo</span>\n'
        'print(res[<span class="s">"rating_estimado"</span>])   <span class="c"># 2</span>\n'
        'print(res[<span class="s">"confianza"</span>])         <span class="c"># 0.853</span>\n'
        '<span class="k">for</span> a <span class="k">in</span> res[<span class="s">"aspectos"</span>]:\n'
        '    print(a[<span class="s">"aspecto"</span>], a[<span class="s">"sentimiento"</span>])\n'
        '    <span class="c"># bateria Negative / atencion_cliente Negative</span>'),
 "en": ('<span class="c"># pip install gradio_client</span>\n'
        '<span class="k">from</span> gradio_client <span class="k">import</span> Client\n\n'
        '<span class="c"># The Space is protected: credentials are required</span>\n'
        'client = Client(<span class="s">"' + SPACE + '"</span>, auth=(<span class="s">"USERNAME"</span>, <span class="s">"PASSWORD"</span>))\n\n'
        '<span class="k">def</span> <span class="f">analyze</span>(text: str) -&gt; dict:\n'
        '    <span class="s">"""Returns sentiment, rating, aspects and recommendations."""</span>\n'
        '    <span class="k">return</span> client.predict(text, api_name=<span class="s">"/predict_json"</span>)\n\n'
        'res = analyze(<span class="s">"The battery lasts very little and customer service was awful"</span>)\n'
        'print(res[<span class="s">"sentimiento"</span>])       <span class="c"># Negativo</span>\n'
        'print(res[<span class="s">"rating_estimado"</span>])   <span class="c"># 2</span>\n'
        'print(res[<span class="s">"confianza"</span>])         <span class="c"># 0.821</span>\n'
        '<span class="k">for</span> a <span class="k">in</span> res[<span class="s">"aspectos"</span>]:\n'
        '    print(a[<span class="s">"aspecto"</span>], a[<span class="s">"sentimiento"</span>])\n'
        '    <span class="c"># bateria Negative / atencion_cliente Negative</span>'),
}

RESP = ('{\n'
        '  <span class="f">"sentimiento"</span>: <span class="s">"Negativo"</span>,\n'
        '  <span class="f">"confianza"</span>: <span class="n">0.853</span>,\n'
        '  <span class="f">"rating_estimado"</span>: <span class="n">2</span>,\n'
        '  <span class="f">"aspectos"</span>: [\n'
        '    {<span class="f">"aspecto"</span>: <span class="s">"bateria"</span>, <span class="f">"sentimiento"</span>: <span class="s">"Negative"</span>},\n'
        '    {<span class="f">"aspecto"</span>: <span class="s">"atencion_cliente"</span>, <span class="f">"sentimiento"</span>: <span class="s">"Negative"</span>}\n'
        '  ],\n'
        '  <span class="f">"recomendaciones"</span>: [\n'
        '    {<span class="f">"aspecto"</span>: <span class="s">"bateria"</span>, <span class="f">"accion"</span>: <span class="s">"Mejorar cables/cargadores&hellip;"</span>}\n'
        '  ]\n'
        '}')

T = {
 "es": dict(
   title="Opyna &middot; Gu&iacute;a de integraci&oacute;n API",
   sub="An&aacute;lisis de sentimiento de rese&ntilde;as &middot; TFM",
   hero=("Opyna expone sus modelos como API sobre Hugging Face Spaces. Cualquier sistema puede "
         "enviar una rese&ntilde;a y recibir el sentimiento, la valoraci&oacute;n estimada, los "
         "aspectos detectados y las acciones recomendadas. La rese&ntilde;a puede estar en "
         "espa&ntilde;ol o en ingl&eacute;s: Opyna detecta el idioma y traduce internamente."),
   warn=("<b>El Space est&aacute; protegido con autenticaci&oacute;n.</b> No es posible llamar al "
         "endpoint con una petici&oacute;n HTTP an&oacute;nima: hay que usar <code>gradio_client</code> "
         "con credenciales, que gestiona el inicio de sesi&oacute;n y la cookie de forma transparente."),
   h_ep="Endpoints disponibles",
   h_cli="Cliente Python &mdash; punto de partida",
   h_resp="Respuesta &mdash; ejemplo real",
   h_fields="Campos de la respuesta",
   h_int="Integraci&oacute;n con sistemas",
   h_no="Sistemas que no son Python",
   no_d=("Salesforce, Power BI o Tableau no pueden autenticarse con <code>gradio_client</code> "
         "directamente. El patr&oacute;n recomendado es un <b>middleware Python</b>: un peque&ntilde;o "
         "servicio que llama a Opyna y deja los resultados donde esos sistemas ya saben leer "
         "(una tabla SQL, un CSV o un endpoint propio). Es el mismo patr&oacute;n de la tarjeta "
         "&laquo;Base de datos&raquo;."),
   note=("<b>Endpoint de evaluaci&oacute;n del TFM.</b> Para uso en producci&oacute;n conviene "
         "desplegar los modelos en infraestructura propia: est&aacute;n publicados en Hugging Face "
         "(<code>rerc86/opyna-sentimiento-200k</code> y <code>rerc86/opyna-rating-200k</code>)."),
   fin="Opyna &middot; TFM M&aacute;ster Big Data, Data Science e IA &middot; UCM - NTIC &middot; 2026",
   c_campo="Campo", c_tipo="Tipo", c_desc="Descripci&oacute;n",
   c_ep="Endpoint", c_dev="Devuelve", c_uso="Uso",
   eps=[("/predict_json", "dict (JSON)", "Integraci&oacute;n. Es el que debes usar."),
        ("/predict", "str (HTML)", "El bloque visual del dashboard. No apto para integrar.")],
   fields=[
     ("sentimiento", "string", "Positivo / Negativo / Neutral"),
     ("confianza", "float [0&ndash;1]", "Probabilidad del clasificador (DistilBERT)"),
     ("rating_estimado", "int [1&ndash;5]", "Valoraci&oacute;n predicha (1 a 5 estrellas)"),
     ("aspectos", "array", "Aspectos detectados en el texto"),
     ("aspectos[].aspecto", "string", "bateria, pantalla, precio, calidad, envio_embalaje, atencion_cliente, rendimiento, facilidad_uso"),
     ("aspectos[].sentimiento", "string", "Positive / Negative / Neutral <i>(en ingl&eacute;s, del modelo ABSA)</i>"),
     ("recomendaciones", "array", "Acciones sugeridas para los aspectos negativos"),
     ("recomendaciones[].accion", "string", "Texto de la acci&oacute;n recomendada"),
   ],
 ),
 "en": dict(
   title="Opyna &middot; API Integration Guide",
   sub="Customer review sentiment analysis &middot; TFM",
   hero=("Opyna exposes its models as an API on Hugging Face Spaces. Any system can send a review "
         "and get back the sentiment, the estimated rating, the detected aspects and the "
         "recommended actions. Reviews may be written in Spanish or English: Opyna detects the "
         "language and translates internally."),
   warn=("<b>The Space is protected with authentication.</b> The endpoint cannot be called with an "
         "anonymous HTTP request: use <code>gradio_client</code> with credentials, which handles "
         "login and session cookie transparently."),
   h_ep="Available endpoints",
   h_cli="Python client &mdash; starting point",
   h_resp="Response &mdash; real example",
   h_fields="Response fields",
   h_int="System integration",
   h_no="Non-Python systems",
   no_d=("Salesforce, Power BI or Tableau cannot authenticate with <code>gradio_client</code> "
         "directly. The recommended pattern is a <b>Python middleware</b>: a small service that "
         "calls Opyna and leaves the results where those systems already read from (a SQL table, "
         "a CSV or your own endpoint). Same pattern as the &laquo;Database&raquo; card."),
   note=("<b>TFM evaluation endpoint.</b> For production use you should deploy the models on your "
         "own infrastructure: they are published on Hugging Face "
         "(<code>rerc86/opyna-sentimiento-200k</code> and <code>rerc86/opyna-rating-200k</code>)."),
   fin="Opyna &middot; TFM M&aacute;ster Big Data, Data Science &amp; AI &middot; UCM - NTIC &middot; 2026",
   c_campo="Field", c_tipo="Type", c_desc="Description",
   c_ep="Endpoint", c_dev="Returns", c_uso="Use",
   eps=[("/predict_json", "dict (JSON)", "Integration. This is the one to use."),
        ("/predict", "str (HTML)", "The dashboard visual block. Not suitable for integration.")],
   fields=[
     ("sentimiento", "string", "Positivo / Negativo / Neutral"),
     ("confianza", "float [0&ndash;1]", "Classifier probability (DistilBERT)"),
     ("rating_estimado", "int [1&ndash;5]", "Predicted rating (1 to 5 stars)"),
     ("aspectos", "array", "Aspects detected in the text"),
     ("aspectos[].aspecto", "string", "bateria, pantalla, precio, calidad, envio_embalaje, atencion_cliente, rendimiento, facilidad_uso"),
     ("aspectos[].sentimiento", "string", "Positive / Negative / Neutral <i>(English, from the ABSA model)</i>"),
     ("recomendaciones", "array", "Suggested actions for negative aspects"),
     ("recomendaciones[].accion", "string", "Recommended action text"),
   ],
 ),
}

CARDS = {
 "es": [
  ("SAP / ERP", "Middleware Python", "Python",
   "Un script intermedio lee reclamaciones del m&oacute;dulo CRM, las analiza con Opyna y escribe "
   "el resultado de vuelta en el sistema de tickets.",
   '<span class="k">for</span> ticket <span class="k">in</span> sap.leer_reclamaciones():\n'
   '    res = analizar(ticket.texto)\n'
   '    sap.actualizar(ticket.id,\n'
   '                   sentimiento=res[<span class="s">"sentimiento"</span>],\n'
   '                   prioridad=<span class="n">1</span> <span class="k">if</span> res[<span class="s">"rating_estimado"</span>] &lt;= <span class="n">2</span> <span class="k">else</span> <span class="n">3</span>)'),
  ("Slack / Teams", "Bot de canal", "Python (Slack Bolt)",
   "Un bot escucha los canales de feedback. Cuando alguien pega una rese&ntilde;a, responde con el "
   "an&aacute;lisis formateado.",
   '@app.message(<span class="s">"review:"</span>)\n'
   '<span class="k">def</span> <span class="f">on_review</span>(message, say):\n'
   '    texto = message[<span class="s">"text"</span>].replace(<span class="s">"review:"</span>, <span class="s">""</span>).strip()\n'
   '    res = analizar(texto)\n'
   '    say(<span class="s">f"Sentimiento: {res[\'sentimiento\']} "</span>\n'
   '        <span class="s">f"({res[\'confianza\']:.0%}) | {res[\'rating_estimado\']}/5"</span>)'),
  ("Alertas / Webhooks", "HTTP POST gen&eacute;rico", "Python",
   "Dispara un aviso autom&aacute;tico cuando llega una rese&ntilde;a negativa, incluyendo las "
   "acciones que Opyna recomienda.",
   'res = analizar(resena)\n'
   '<span class="k">if</span> res[<span class="s">"sentimiento"</span>] == <span class="s">"Negativo"</span> <span class="k">and</span> res[<span class="s">"rating_estimado"</span>] &lt;= <span class="n">2</span>:\n'
   '    requests.post(WEBHOOK_URL, json={\n'
   '        <span class="f">"alerta"</span>: <span class="s">"Rese&ntilde;a negativa"</span>,\n'
   '        <span class="f">"confianza"</span>: res[<span class="s">"confianza"</span>],\n'
   '        <span class="f">"aspectos"</span>: res[<span class="s">"aspectos"</span>],\n'
   '        <span class="f">"acciones"</span>: res[<span class="s">"recomendaciones"</span>]})'),
  ("Base de datos", "PostgreSQL / MySQL / SQLite", "Python (SQLAlchemy)",
   "Guarda cada an&aacute;lisis para hist&oacute;ricos y cuadros de mando. Es tambi&eacute;n la v&iacute;a "
   "por la que Power BI o Tableau leen los resultados.",
   '<span class="k">from</span> sqlalchemy <span class="k">import</span> insert\n\n'
   'res = analizar(texto)\n'
   'conn.execute(insert(resenas).values(\n'
   '    texto=texto,\n'
   '    sentimiento=res[<span class="s">"sentimiento"</span>],\n'
   '    rating=res[<span class="s">"rating_estimado"</span>],\n'
   '    confianza=res[<span class="s">"confianza"</span>],\n'
   '    aspectos=json.dumps(res[<span class="s">"aspectos"</span>])))'),
 ],
 "en": [
  ("SAP / ERP", "Python middleware", "Python",
   "An intermediate script reads complaints from the CRM module, analyses them with Opyna and "
   "writes the result back into the ticketing system.",
   '<span class="k">for</span> ticket <span class="k">in</span> sap.read_complaints():\n'
   '    res = analyze(ticket.text)\n'
   '    sap.update(ticket.id,\n'
   '               sentiment=res[<span class="s">"sentimiento"</span>],\n'
   '               priority=<span class="n">1</span> <span class="k">if</span> res[<span class="s">"rating_estimado"</span>] &lt;= <span class="n">2</span> <span class="k">else</span> <span class="n">3</span>)'),
  ("Slack / Teams", "Channel bot", "Python (Slack Bolt)",
   "A bot listens to feedback channels. When someone pastes a review, it replies with the "
   "formatted analysis.",
   '@app.message(<span class="s">"review:"</span>)\n'
   '<span class="k">def</span> <span class="f">on_review</span>(message, say):\n'
   '    text = message[<span class="s">"text"</span>].replace(<span class="s">"review:"</span>, <span class="s">""</span>).strip()\n'
   '    res = analyze(text)\n'
   '    say(<span class="s">f"Sentiment: {res[\'sentimiento\']} "</span>\n'
   '        <span class="s">f"({res[\'confianza\']:.0%}) | {res[\'rating_estimado\']}/5"</span>)'),
  ("Alerts / Webhooks", "Generic HTTP POST", "Python",
   "Fires an automatic alert when a negative review arrives, including the actions Opyna "
   "recommends.",
   'res = analyze(review)\n'
   '<span class="k">if</span> res[<span class="s">"sentimiento"</span>] == <span class="s">"Negativo"</span> <span class="k">and</span> res[<span class="s">"rating_estimado"</span>] &lt;= <span class="n">2</span>:\n'
   '    requests.post(WEBHOOK_URL, json={\n'
   '        <span class="f">"alert"</span>: <span class="s">"Negative review"</span>,\n'
   '        <span class="f">"confidence"</span>: res[<span class="s">"confianza"</span>],\n'
   '        <span class="f">"aspects"</span>: res[<span class="s">"aspectos"</span>],\n'
   '        <span class="f">"actions"</span>: res[<span class="s">"recomendaciones"</span>]})'),
  ("Database", "PostgreSQL / MySQL / SQLite", "Python (SQLAlchemy)",
   "Store every analysis for history and dashboards. It is also the way Power BI or Tableau read "
   "the results.",
   '<span class="k">from</span> sqlalchemy <span class="k">import</span> insert\n\n'
   'res = analyze(text)\n'
   'conn.execute(insert(reviews).values(\n'
   '    text=text,\n'
   '    sentiment=res[<span class="s">"sentimiento"</span>],\n'
   '    rating=res[<span class="s">"rating_estimado"</span>],\n'
   '    confidence=res[<span class="s">"confianza"</span>],\n'
   '    aspects=json.dumps(res[<span class="s">"aspectos"</span>])))'),
 ],
}


def build(lang):
    t = T[lang]
    h = ['<!DOCTYPE html><html lang="' + lang + '"><head><meta charset="utf-8">',
         '<title>' + t["title"] + '</title><style>' + CSS + '</style></head><body>']
    h.append('<h1>' + t["title"] + '</h1><p class="sub">' + t["sub"] + '</p>')
    h.append('<div class="hero"><p>' + t["hero"] + '</p></div>')
    h.append('<div class="warn">' + t["warn"] + '</div>')

    h.append('<h2>' + t["h_ep"] + '</h2>')
    h.append('<table class="t"><tr><th>' + t["c_ep"] + '</th><th>' + t["c_dev"] +
             '</th><th>' + t["c_uso"] + '</th></tr>')
    for e, d, u in t["eps"]:
        h.append('<tr><td><code class="fn">' + e + '</code></td>'
                 '<td><span class="ft">' + d + '</span></td><td>' + u + '</td></tr>')
    h.append('</table>')

    h.append('<h2>' + t["h_cli"] + '</h2>')
    h.append('<div class="code">' + CLIENTE[lang] + '</div>')

    h.append('<h3>' + t["h_resp"] + '</h3>')
    h.append('<div class="code">' + RESP + '</div>')

    h.append('<h3>' + t["h_fields"] + '</h3>')
    h.append('<table class="t"><tr><th>' + t["c_campo"] + '</th><th>' + t["c_tipo"] +
             '</th><th>' + t["c_desc"] + '</th></tr>')
    for f, ty, d in t["fields"]:
        h.append('<tr><td><code class="fn">' + f + '</code></td>'
                 '<td><span class="ft">' + ty + '</span></td><td>' + d + '</td></tr>')
    h.append('</table>')

    h.append('<h2>' + t["h_int"] + '</h2>')
    for ti, st, tag, d, code in CARDS[lang]:
        h.append('<div class="card"><span class="tag">' + tag + '</span>'
                 '<p class="ti">' + ti + '</p><p class="st">' + st + '</p>'
                 '<p class="d">' + d + '</p><div class="code">' + code + '</div></div>')

    h.append('<h3>' + t["h_no"] + '</h3>')
    h.append('<p>' + t["no_d"] + '</p>')
    h.append('<div class="note">' + t["note"] + '</div>')
    h.append('<div class="fin">' + t["fin"] + '</div>')
    h.append('</body></html>')
    return "".join(h)


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else "/content"
    for lang in ["es", "en"]:
        p = out + "/api_guide_" + lang + ".pdf"
        HTML(string=build(lang)).write_pdf(p)
        print(lang.upper(), "->", p, os.path.getsize(p), "bytes")

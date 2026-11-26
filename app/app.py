# -*- coding: utf-8 -*-
"""Opyna v5 - SaaS moderno, head= para toggle y Google Fonts. ASCII-safe."""
import os
import gradio as gr
from inference import OpynaAnalyzer

analyzer = OpynaAnalyzer(device=int(os.getenv("OPYNA_DEVICE", "-1")))

# -- Logo Broadcast en granate sobre fondo claro --
LOGO_SVG = (
    '<svg viewBox="0 0 44 44" height="42" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="4" cy="22" r="4.2" fill="#7a1f2b"/>'
    '<path d="M 4 13 A 9 9 0 0 1 4 31" fill="none" stroke="#7a1f2b" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M 4 7 A 15 15 0 0 1 4 37" fill="none" stroke="#7a1f2b" stroke-width="2.2" stroke-linecap="round" opacity="0.5"/>'
    '<path d="M 4 1 A 21 21 0 0 1 4 43" fill="none" stroke="#7a1f2b" stroke-width="1.7" stroke-linecap="round" opacity="0.25"/>'
    '</svg>'
)

_ucm = os.getenv("OPYNA_LOGO", "")
UCM_IMG = (
    f'<img src="{_ucm}" style="height:36px;opacity:.65;object-fit:contain;">'
    if _ucm else ""
)

# -- Estilos globales + Google Fonts (inyectados en <head>) --
HEAD = """<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* Forzar modo claro - sin dark mode */
html, html[data-theme="dark"] {
  color-scheme: light !important;
  background: #ffffff !important;
}
body, #root, .gradio-container, .wrap, .main, footer {
  background: #ffffff !important;
  color: #0f172a !important;
}
*, body, .gradio-container, .gradio-container * {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}
input, textarea, select { background:#fff !important; color:#0f172a !important; }
/* Etiquetas de los componentes de Gradio: su gris por defecto (#71717a)
   tiene poco contraste sobre fondo blanco */
.gradio-container label span, .gradio-container .label-wrap span,
.gradio-container [data-testid="block-label"] span,
.gradio-container .label { color: #334155 !important; }
/* Resultado bilingue: se muestra solo el idioma activo */
/* heredan color y tipografia del contenedor: Gradio los pisaria */
.op-l-es, .op-l-en { color: inherit !important; font: inherit !important;
  letter-spacing: inherit !important; text-transform: inherit !important; }
.op-l-en { display: none !important; }
body.op-en .op-l-en { display: inline !important; }
body.op-en .op-l-es { display: none !important; }
/* Las negritas inyectadas al cambiar de idioma deben conservar color visible */
#opyna-desc b, #opyna-desc strong {
  color: #0f172a !important; font-weight: 700 !important; }
.gradio-container { max-width: 860px !important; margin: 0 auto !important; padding: 0 16px !important; }
button#analizar-btn { background:#7a1f2b !important; border:none !important; color:#fff !important;
  font-weight:600 !important; letter-spacing:.3px !important; height:44px !important; border-radius:8px !important; }
button#analizar-btn:hover { background:#5e1720 !important; }
textarea { border-radius:8px !important; border:1.5px solid #e2e8f0 !important; font-size:.9rem !important; }
textarea:focus { border-color:#7a1f2b !important; outline:none !important; box-shadow:0 0 0 3px rgba(122,31,43,.1) !important; }
.block, .panel, .form { background:#fff !important; }

/* Reducir gap excesivo entre bloques */
.gradio-container .column { gap: 0px !important; }
/* Mantener separacion minima entre textarea y boton */
.gradio-container .form { margin-top: 4px !important; }
/* Ocultar footer nativo de Gradio */
footer.svelte-apbfr4, .footer, footer { display: none !important; }
/* Ocultar "Usar via API" etc */
.api-docs, [class*="footer"] { display: none !important; }
</style>
<script>
(function(){
var T={
  es:{
    desc:"Convierte miles de rese&ntilde;as en <b>sentimiento</b>, <b>valoraci&oacute;n</b>, <b>aspectos de producto</b> y <b>recomendaciones de negocio</b> accionables.",
    inp:"Rese\u00f1a de cliente",
    ph:"Pega aqu\u00ed una rese\u00f1a de producto en ingl\u00e9s\u2026",
    btn:"Analizar",
    usr:"Usuario",pwd:"Contrase\u00f1a",lg:"Entrar",eg:"Ejemplos",p1:"200k rese\u00f1as entrenamiento",p2:"8 aspectos de producto",p3:"DistilBERT + DeBERTa fine-tuned"
  },
  en:{
    desc:"Turn customer reviews into <b>sentiment</b>, <b>rating</b>, <b>product aspects</b> and actionable <b>business recommendations</b>.",
    inp:"Customer review",
    ph:"Paste a product review in English here\u2026",
    btn:"Analyze",
    usr:"Username",pwd:"Password",lg:"Log in",eg:"Examples",p1:"200k training reviews",p2:"8 product aspects",p3:"DistilBERT + DeBERTa fine-tuned"
  }
};
var L=localStorage.getItem('op_lang')||'es';
function dc(s){var d=document.createElement('div');d.innerHTML=s;return d.textContent;}
function ap(){
  var t=T[L];
  var d=document.getElementById('opyna-desc');if(d)d.innerHTML=t.desc;
  var ta=document.querySelector('textarea');if(ta)ta.placeholder=t.ph;
  document.querySelectorAll('label span').forEach(function(s){
    var x=s.textContent.trim();
    if(x==='Rese\u00f1a de cliente'||x==='Customer review')s.textContent=dc(t.inp);
  });
  document.querySelectorAll('button').forEach(function(b){
    var x=b.textContent.trim();
    if(x==='Analizar'||x==='Analyze')b.textContent=t.btn;
    if(b.type==='submit'&&(b.textContent.trim()==='Entrar'||b.textContent.trim()==='Log in'))b.textContent=t.lg;
  });
  document.querySelectorAll('input[type=text]').forEach(function(i){i.placeholder=t.usr;});
  document.querySelectorAll('input[type=password]').forEach(function(i){i.placeholder=t.pwd;});
  var es=document.getElementById('op-es'),en=document.getElementById('op-en');
  if(es){es.style.background=L==='es'?'#7a1f2b':'transparent';es.style.color=L==='es'?'#fff':'#64748b';es.style.fontWeight=L==='es'?'700':'500';}
  if(en){en.style.background=L==='en'?'#7a1f2b':'transparent';en.style.color=L==='en'?'#fff':'#64748b';en.style.fontWeight=L==='en'?'700':'500';}
  // Traducir label de la seccion de Ejemplos/Examples
  document.querySelectorAll('span').forEach(function(s){
    var x=s.textContent.trim();
    if(x==='Ejemplos'||x==='Examples')s.textContent=t.eg;
  });
  // Traducir pills del header
  var el1=document.getElementById('op-pill-1');if(el1)el1.textContent=t.p1;
  var el2=document.getElementById('op-pill-2');if(el2)el2.textContent=t.p2;
  var el3=document.getElementById('op-pill-3');if(el3)el3.textContent=t.p3;
}
window.opSL=function(l){L=l;localStorage.setItem('op_lang',l);ap();};
// Enlazar botones via addEventListener (evita onclick inline que rompe Svelte)
function bindToggleBtns(){
  var be=document.getElementById('op-es');
  var bn=document.getElementById('op-en');
  if(be&&!be._opBound){be.addEventListener('click',function(){window.opSL('es');});be._opBound=1;}
  if(bn&&!bn._opBound){bn.addEventListener('click',function(){window.opSL('en');});bn._opBound=1;}
}
window.addEventListener('load',function(){ap();bindToggleBtns();setTimeout(ap,800);setTimeout(ap,2200);setTimeout(bindToggleBtns,2500);});
setInterval(function(){ap();bindToggleBtns();},3000);

// ---- Branding dinamico pantalla login ----
var LOGO_HTML='<svg viewBox="0 0 44 44" height="46" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="22" r="4.2" fill="#7a1f2b"/><path d="M 4 13 A 9 9 0 0 1 4 31" fill="none" stroke="#7a1f2b" stroke-width="3" stroke-linecap="round"/><path d="M 4 7 A 15 15 0 0 1 4 37" fill="none" stroke="#7a1f2b" stroke-width="2.2" stroke-linecap="round" opacity="0.5"/><path d="M 4 1 A 21 21 0 0 1 4 43" fill="none" stroke="#7a1f2b" stroke-width="1.7" stroke-linecap="round" opacity="0.25"/></svg>';
function injectLoginBranding(){
  var pwdInput=document.querySelector('input[type=password]');
  if(!pwdInput||document.getElementById('opyna-login-brand'))return;
  var form=pwdInput.closest('form')||pwdInput.parentElement;
  while(form&&form.tagName!=='FORM')form=form.parentElement;
  var container=form?form.parentElement:null;
  if(!container)return;
  var brand=document.createElement('div');
  brand.id='opyna-login-brand';
  brand.style.cssText='font-family:Inter,system-ui,sans-serif;background:#fff;padding:32px 24px 20px;text-align:center;border-bottom:1px solid #f1f5f9;margin-bottom:8px;';
  brand.innerHTML='<div style="display:inline-flex;align-items:center;gap:14px;justify-content:center;margin-bottom:14px;">'+LOGO_HTML+'<div style="text-align:left;"><div style="font-size:1.9rem;font-weight:800;color:#0f172a;letter-spacing:-.5px;line-height:1;">Opyna</div><div style="font-size:.6rem;font-weight:700;color:#7a1f2b;letter-spacing:3px;text-transform:uppercase;margin-top:4px;">Customer Intelligence</div></div></div><div style="margin:0 auto;max-width:360px;"><div style="font-size:.82rem;color:#475569;margin-bottom:10px;">Plataforma de an&aacute;lisis de rese&ntilde;as con IA</div><div style="display:inline-flex;flex-wrap:wrap;gap:6px;justify-content:center;"><span style="font-size:.7rem;font-weight:600;color:#7a1f2b;background:#fff1f2;border:1px solid #fecdd3;border-radius:99px;padding:3px 10px;">TFM</span><span style="font-size:.7rem;color:#64748b;background:#f8fafc;border:1px solid #e2e8f0;border-radius:99px;padding:3px 10px;">M&aacute;ster Big Data, DS e IA</span><span style="font-size:.7rem;color:#64748b;background:#f8fafc;border:1px solid #e2e8f0;border-radius:99px;padding:3px 10px;">UCM &ndash; NTIC</span><span style="font-size:.7rem;color:#64748b;background:#f8fafc;border:1px solid #e2e8f0;border-radius:99px;padding:3px 10px;">2026</span></div></div><div style="display:flex;justify-content:center;margin-top:16px;"><div style="display:inline-flex;background:#fff;border:1px solid #e2e8f0;border-radius:99px;overflow:hidden;"><button type="button" id="op-es" onclick="opSL('es')" style="border:none;padding:5px 16px;cursor:pointer;font-size:11px;letter-spacing:1.5px;">ES</button><div style="width:1px;background:#e2e8f0;margin:5px 0;"></div><button type="button" id="op-en" onclick="opSL('en')" style="border:none;padding:5px 16px;cursor:pointer;font-size:11px;letter-spacing:1.5px;">EN</button></div></div>';
  container.insertBefore(brand,container.firstChild);
  ap();
}
setInterval(injectLoginBranding,400);
})();
</script>"""

# -- Toggle ES/EN (solo botones, script ya esta en HEAD) --
TOGGLE_HTML = """<div id="opyna-lang"
  style="position:fixed;bottom:20px;left:20px;z-index:9999;display:flex;
         background:#fff;border:1px solid #e2e8f0;border-radius:99px;
         overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);font-family:Inter,sans-serif;">
  <button type="button" id="op-es" data-lang="es"
    style="border:none;padding:6px 18px;cursor:pointer;font-size:11px;letter-spacing:1.5px;transition:all .18s;">ES</button>
  <div style="width:1px;background:#e2e8f0;margin:6px 0;"></div>
  <button type="button" id="op-en" data-lang="en"
    style="border:none;padding:6px 18px;cursor:pointer;font-size:11px;letter-spacing:1.5px;transition:all .18s;">EN</button>
</div>"""

# -- Header principal --
HEADER_MAIN = f"""<div style="padding:20px 0 16px;border-bottom:1.5px solid #f1f5f9;margin-bottom:8px;">
  <div style="display:flex;align-items:center;gap:16px;">
    {LOGO_SVG}
    <div style="width:1px;height:36px;background:#e2e8f0;"></div>
    <div>
      <div style="font-size:1.5rem;font-weight:800;color:#0f172a;letter-spacing:-.5px;line-height:1;">Opyna</div>
      <div style="font-size:.65rem;font-weight:700;color:#7a1f2b;letter-spacing:3px;text-transform:uppercase;margin-top:2px;">Customer Intelligence</div>
    </div>
    <div style="flex:1;"></div>
    <div style="display:flex;align-items:center;gap:12px;">
      {UCM_IMG}
      <div style="font-size:.7rem;color:#94a3b8;line-height:1.5;text-align:right;">
        TFM &middot; M&aacute;ster Big Data<br>Data Science e IA &middot; UCM&nbsp;&ndash;&nbsp;NTIC
      </div>
    </div>
  </div>
  <p id="opyna-desc" style="margin:12px 0 0;color:#64748b;font-size:.875rem;line-height:1.6;max-width:640px;">
    Convierte miles de rese&ntilde;as en <b style="color:#0f172a;">sentimiento</b>,
    <b style="color:#0f172a;">valoraci&oacute;n</b>,
    <b style="color:#0f172a;">aspectos de producto</b> y
    <b style="color:#0f172a;">recomendaciones de negocio</b> accionables.
  </p>
  <div style="display:flex;gap:20px;margin-top:14px;">
    <div style="display:flex;align-items:center;gap:7px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#7a1f2b;"></div>
      <span id="op-pill-1" style="font-size:.75rem;color:#64748b;font-weight:500;">200k rese&ntilde;as entrenamiento</span>
    </div>
    <div style="display:flex;align-items:center;gap:7px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#7a1f2b;opacity:.7;"></div>
      <span id="op-pill-2" style="font-size:.75rem;color:#64748b;font-weight:500;">8 aspectos de producto</span>
    </div>
    <div style="display:flex;align-items:center;gap:7px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#7a1f2b;opacity:.45;"></div>
      <span id="op-pill-3" style="font-size:.75rem;color:#64748b;font-weight:500;">DistilBERT + DeBERTa fine-tuned</span>
    </div>
  </div>
</div>"""

# -- auth_message: texto simple (Gradio renderiza Markdown, no HTML complejo)
# El branding real lo inyecta el JS en head= via MutationObserver sobre el formulario
HEADER_LOGIN = (
    "<h2 style=\"margin:0 0 4px;\">Opyna</h2>"
    "<p style=\"margin:0 0 12px;font-size:.8rem;color:#7a1f2b;font-weight:600;letter-spacing:2px;text-transform:uppercase;\">Customer Intelligence Platform</p>"
    "<hr style=\"margin:0 0 12px;border:none;border-top:1px solid #e2e8f0;\">"
    "<p style=\"margin:0;font-size:.78rem;color:#64748b;\">"
    "M\u00e1ster Big Data, Data Science e IA"
    " &middot; UCM &ndash; NTIC &middot; 2026"
    "</p>"
)

SCRIPT_JS = """(function(){var L=localStorage.getItem("op_lang")||"es";var T={es:{desc:"Convierte miles de rese\u00f1as en <b>sentimiento</b>, <b>valoraci\u00f3n</b>, <b>aspectos de producto</b> y <b>recomendaciones de negocio</b> accionables.",inp:"Rese\u00f1a de cliente",ph:"Pega aqu\u00ed una rese\u00f1a en espa\u00f1ol o en ingl\u00e9s.",btn:"Analizar",eg:"Ejemplos",p1:"200k rese\u00f1as entrenamiento",p2:"8 aspectos de producto",p3:"DistilBERT + DeBERTa fine-tuned"},en:{desc:"Turn customer reviews into <b>sentiment</b>, <b>rating</b>, <b>product aspects</b> and actionable <b>business recommendations</b>.",inp:"Customer review",ph:"Paste a product review in English or Spanish here.",btn:"Analyze",eg:"Examples",p1:"200k training reviews",p2:"8 product aspects",p3:"DistilBERT + DeBERTa fine-tuned"}};function ap(){var t=T[L];var d=document.getElementById("opyna-desc");if(d)d.innerHTML=t.desc;var ta=document.querySelector("textarea");if(ta)ta.placeholder=t.ph;document.querySelectorAll("label span").forEach(function(s){var x=s.textContent.trim();if(x==="Rese\u00f1a de cliente"||x==="Customer review")s.textContent=t.inp;});document.querySelectorAll("button").forEach(function(b){var x=b.textContent.trim();if(x==="Analizar"||x==="Analyze")b.textContent=t.btn;});var es=document.getElementById("op-es"),en=document.getElementById("op-en");if(es){es.style.background=L==="es"?"#7a1f2b":"transparent";es.style.color=L==="es"?"#fff":"#64748b";es.style.fontWeight=L==="es"?"700":"500";}if(en){en.style.background=L==="en"?"#7a1f2b":"transparent";en.style.color=L==="en"?"#fff":"#64748b";en.style.fontWeight=L==="en"?"700":"500";}document.querySelectorAll("span,div.label").forEach(function(s){var x=s.textContent.trim();if(x==="Ejemplos"||x==="Examples")s.textContent=t.eg;});var e1=document.getElementById("op-pill-1");if(e1)e1.textContent=t.p1;var e2=document.getElementById("op-pill-2");if(e2)e2.textContent=t.p2;var e3=document.getElementById("op-pill-3");if(e3)e3.textContent=t.p3;var tN=["The battery life is very short and customer service was terrible.","Excellent screen, very sharp. The battery lasts all week without issues.","Good value for the features. The build quality is solid."];var tS=["La bateria dura muy poco y el servicio al cliente fue pesimo.","Pantalla excelente, muy nitida. La bateria dura toda la semana sin problemas.","Buen precio para las caracteristicas que ofrece. Calidad de construccion buena."];var gI=document.querySelectorAll("button.gallery-item");gI.forEach(function(b,i){var tx=(L!=="en")?tS:tN;if(tx[i])b.textContent=tx[i];});document.body.classList.remove("op-es","op-en");document.body.classList.add("op-"+L);var gu=document.getElementById("op-guia");if(gu){gu.href="https://huggingface.co/spaces/rerc86/opyna/resolve/main/api_guide_"+L+".pdf";}}window.opSL=function(l){L=l;localStorage.setItem("op_lang",l);ap();};function bind(){var be=document.getElementById("op-es"),bn=document.getElementById("op-en");if(be&&!be._ob){be.addEventListener("click",function(){window.opSL("es");});be._ob=1;}if(bn&&!bn._ob){bn.addEventListener("click",function(){window.opSL("en");});bn._ob=1;}}window.addEventListener("load",function(){ap();bind();setTimeout(ap,800);setTimeout(ap,2200);setTimeout(bind,2500);});setInterval(function(){ap();bind();},3000);})();"""

# -- Colores de resultado --
_ASP_ES = {
    "bateria":"Bater\u00eda","pantalla":"Pantalla","precio":"Precio",
    "calidad":"Calidad","facilidad_uso":"Facilidad de uso",
    "envio_embalaje":"Env\u00edo / embalaje","atencion_cliente":"Atenci\u00f3n al cliente",
    "rendimiento":"Rendimiento",
}
_COL = {
    "Positivo":("#f0fdf4","#16a34a","#bbf7d0"),"Positive":("#f0fdf4","#16a34a","#bbf7d0"),
    "Neutral": ("#fefce8","#ca8a04","#fef08a"),
    "Negativo":("#fff1f2","#e11d48","#fecdd3"),"Negative":("#fff1f2","#e11d48","#fecdd3"),
}
_POL_ES={"Positive":"Positivo","Neutral":"Neutral","Negative":"Negativo"}
_POL_EN={"Positive":"Positive","Neutral":"Neutral","Negative":"Negative"}
_SENT_EN={"Positivo":"Negative" if False else "Positive","Neutral":"Neutral","Negativo":"Negative"}
_ASP_EN = {
    "bateria":"Battery","pantalla":"Screen","precio":"Price",
    "calidad":"Build quality","facilidad_uso":"Ease of use",
    "envio_embalaje":"Shipping / packaging","atencion_cliente":"Customer service",
    "rendimiento":"Performance",
}
_ACC_EN = {
    "atencion_cliente":"Strengthen after-sales: response times, clear warranty, proactive refunds.",
    "pantalla":"Panel quality control and management of resolution expectations.",
    "bateria":"Improve bundled cables/chargers and battery life; set realistic expectations.",
    "rendimiento":"Firmware optimisation and stress testing before launch.",
    "envio_embalaje":"More protective packaging and delivery tracking.",
    "calidad":"Monitor durability, linked to the early failures that drive support complaints.",
}

def _bi(es, en):
    """Devuelve los dos idiomas; el CSS muestra solo el activo."""
    return f'<span class="op-l-es">{es}</span><span class="op-l-en">{en}</span>'
_G="#7a1f2b"

_SENT_ICON={"Positivo":"&#9650;","Neutral":"&#9644;","Negativo":"&#9660;",
            "Positive":"&#9650;","Negative":"&#9660;"}


def _resultado_html(r):
    if "error" in r:
        return f'<p style="color:#94a3b8;font-size:.85rem;padding:16px 0;">{r["error"]}</p>'
    n=r["rating_estimado"]
    sent=r["sentimiento"]
    conf=r["confianza"]
    bg,fg,border=_COL.get(sent,("#f8fafc","#334155","#e2e8f0"))
    icon=_SENT_ICON.get(sent,"")
    stars="&#9733;"*n+"&#9734;"*(5-n)

    H=['<div style="margin-top:4px;">']

    # -- Fila superior: sentimiento + rating --
    H.append(f'''<div style="display:flex;align-items:stretch;gap:12px;margin-bottom:14px;">
  <div style="flex:1;background:{bg};border:1.5px solid {border};border-radius:10px;
       padding:16px 20px;display:flex;align-items:center;gap:12px;">
    <div style="font-size:1.6rem;">{icon}</div>
    <div>
      <div style="font-size:.7rem;font-weight:600;color:{fg};letter-spacing:1.5px;text-transform:uppercase;">{_bi('Sentimiento','Sentiment')}</div>
      <div style="font-size:1.2rem;font-weight:700;color:{fg};margin-top:1px;">{_bi(sent, _SENT_EN.get(sent, sent))}</div>
    </div>
    <div style="margin-left:auto;text-align:right;">
      <div style="font-size:.65rem;color:{fg};opacity:.7;letter-spacing:1px;">{_bi('CONFIANZA','CONFIDENCE')}</div>
      <div style="font-size:1.4rem;font-weight:800;color:{fg};">{conf*100:.0f}<span style="font-size:.75rem;font-weight:500;">%</span></div>
    </div>
  </div>
  <div style="background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:10px;
       padding:16px 20px;min-width:140px;text-align:center;">
    <div style="font-size:.7rem;font-weight:600;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;">Rating</div>
    <div style="font-size:1.3rem;color:{_G};letter-spacing:4px;margin:6px 0 2px;">{stars}</div>
    <div style="font-size:.85rem;font-weight:700;color:#0f172a;">{n} / 5</div>
  </div>
</div>''')

    # -- Aspectos --
    if r["aspectos"]:
        H.append('<div style="background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:10px;padding:16px 20px;margin-bottom:12px;">')
        H.append('<div style="font-size:.7rem;font-weight:700;letter-spacing:1.5px;color:#94a3b8;text-transform:uppercase;margin-bottom:12px;">' + _bi("Aspectos detectados", "Detected aspects") + '</div>')
        H.append('<div style="display:flex;flex-wrap:wrap;gap:8px;">')
        for a in r["aspectos"]:
            s=a["sentimiento"]
            abg,afg,ab=_COL.get(s,("#f8fafc","#334155","#e2e8f0"))
            label=_bi(_ASP_ES.get(a["aspecto"],a["aspecto"]), _ASP_EN.get(a["aspecto"],a["aspecto"]))
            pol=_bi(_POL_ES.get(s,s), _POL_EN.get(s,s))
            ic=_SENT_ICON.get(s,"")
            H.append(f'<span style="display:inline-flex;align-items:center;gap:5px;padding:6px 12px;'
                     f'background:{abg};border:1px solid {ab};border-radius:99px;'
                     f'font-size:.8rem;font-weight:500;color:{afg};">'
                     f'{ic} <b style="font-weight:600;color:{afg};">{label}</b> &middot; {pol}</span>')
        H.append('</div></div>')

    # -- Plan de accion --
    if r["recomendaciones"]:
        H.append('<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:10px;padding:16px 20px;">')
        H.append(f'<div style="font-size:.7rem;font-weight:700;letter-spacing:1.5px;color:#94a3b8;text-transform:uppercase;margin-bottom:12px;">' + _bi("Plan de acci&oacute;n", "Action plan") + '</div>')
        for rec in r["recomendaciones"]:
            asp=_bi(_ASP_ES.get(rec["aspecto"],rec["aspecto"]), _ASP_EN.get(rec["aspecto"],rec["aspecto"]))
            H.append(f'<div style="display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start;">'
                     f'<div style="width:6px;height:6px;border-radius:50%;background:{_G};margin-top:6px;flex-shrink:0;"></div>'
                     f'<div><span style="font-weight:600;color:#0f172a;">{asp}</span>'
                     f'<span style="color:#64748b;"> &mdash; {_bi(rec["accion"], _ACC_EN.get(rec["aspecto"], rec["accion"]))}</span></div></div>')
        H.append('</div>')

    H.append('</div>')
    return "".join(H)


def _run(texto):
    return analyzer.analizar(texto)


def analizar(texto):
    return _resultado_html(_run(texto))


def analizar_api(texto: str) -> dict:
    """Misma logica que el dashboard, devuelve los datos crudos (JSON)."""
    return _run(texto)


EJEMPLOS=[
    "The battery drains way too fast and customer service was useless.",
    "Great screen and very easy to set up, works perfectly.",
    "La bateria se agota muy rapido y el servicio al cliente fue pesimo.",
]

PANEL_HTML = (
    "<div style='margin-top:24px;padding:18px 20px;background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:12px;'>"
    "<div style='display:flex;align-items:center;gap:10px;margin-bottom:14px;'>"
    "<div style='width:8px;height:8px;background:#7a1f2b;border-radius:50%;'></div>"
    "<span style='font-size:.68rem;font-weight:700;letter-spacing:2px;color:#94a3b8;text-transform:uppercase;'>"
    "<span class='op-l-es'>Integraci&oacute;n API &mdash; Conecta Opyna a tu pipeline empresarial</span><span class='op-l-en'>API Integration &mdash; Connect Opyna to your enterprise pipeline</span></span></div>"
    "<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>"
    "<div style='background:#fff;border:1.5px solid #e2e8f0;border-radius:10px;padding:15px 16px;'>"
    "<div style='font-size:.67rem;font-weight:700;color:#7a1f2b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;'>&#128229; <span class='op-l-es'>API Entrada</span><span class='op-l-en'>API Input</span></div>"
    "<div style='background:#0f172a;border-radius:8px;padding:10px 12px;font-family:monospace;font-size:.7rem;line-height:1.75;color:#e2e8f0;margin-bottom:10px;'>"
    "<span style='color:#94a3b8;'>POST</span> <span style='color:#7dd3fc;'>/predict_json</span><br>"
    "<span style='color:#fbbf24;'>{</span><br>&nbsp;&nbsp;<span style='color:#7dd3fc;'>&quot;data&quot;</span>: [<span style='color:#86efac;'><span class='op-l-es'>&quot;La bateria dura poco...&quot;</span><span class='op-l-en'>&quot;The battery drains fast...&quot;</span></span>]<br><span style='color:#fbbf24;'>}</span></div>"
    "<div style='display:flex;flex-wrap:wrap;gap:4px;'>"
    "<span style='background:#fff1f2;color:#7a1f2b;border:1px solid #fecdd3;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Salesforce</span>"
    "<span style='background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>SAP/ERP</span>"
    "<span style='background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Slack/Teams</span>"
    "<span style='background:#fefce8;color:#854d0e;border:1px solid #fef08a;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Telegram</span>"
    "</div></div>"
    "<div style='background:#fff;border:1.5px solid #e2e8f0;border-radius:10px;padding:15px 16px;'>"
    "<div style='font-size:.67rem;font-weight:700;color:#7a1f2b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;'>&#128228; <span class='op-l-es'>API Salida</span><span class='op-l-en'>API Output</span></div>"
    "<div style='background:#0f172a;border-radius:8px;padding:10px 12px;font-family:monospace;font-size:.7rem;line-height:1.75;color:#e2e8f0;margin-bottom:10px;'>"
    "<span style='color:#fbbf24;'>{</span><br>&nbsp;&nbsp;<span style='color:#7dd3fc;'>&quot;sentimiento&quot;</span>: <span style='color:#86efac;'>&quot;Negativo&quot;</span>,<br>"
    "&nbsp;&nbsp;<span style='color:#7dd3fc;'>&quot;confianza&quot;</span>: <span style='color:#fb923c;'>0.94</span>,<br>&nbsp;&nbsp;<span style='color:#7dd3fc;'>&quot;aspectos&quot;</span>: [<span style='color:#fbbf24;'>{...}</span>]<br><span style='color:#fbbf24;'>}</span></div>"
    "<div style='display:flex;flex-wrap:wrap;gap:4px;'>"
    "<span style='background:#fff1f2;color:#7a1f2b;border:1px solid #fecdd3;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Power BI</span>"
    "<span style='background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Tableau</span>"
    "<span style='background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'>Webhooks</span>"
    "<span style='background:#f8fafc;color:#475569;border:1px solid #e2e8f0;border-radius:99px;padding:2px 8px;font-size:.65rem;font-weight:600;'><span class='op-l-es'>Bases de datos</span><span class='op-l-en'>Databases</span></span>"
    "</div></div></div>"
    "<div style='margin-top:10px;padding:8px 12px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;font-size:.72rem;color:#475569;'>"
    "&#128279; <code style='background:#f1f5f9;padding:1px 6px;border-radius:4px;color:#7a1f2b;font-weight:600;'>gradio_client &middot; api_name=&quot;/predict_json&quot;</code>"
    " &mdash; <span class='op-l-es'>API de Gradio &mdash; requiere credenciales</span><span class='op-l-en'>Gradio API &mdash; credentials required</span> &mdash; <a id='op-guia' href='https://huggingface.co/spaces/rerc86/opyna/resolve/main/api_guide_es.pdf' target='_blank' style='color:#7a1f2b;font-weight:700;text-decoration:none;'><span class='op-l-es'>Ver gu&iacute;a &rarr;</span><span class='op-l-en'>View guide &rarr;</span></a></div></div>"
)

with gr.Blocks(title="Opyna", head=HEAD, theme=gr.themes.Base(), js=SCRIPT_JS) as demo:
    gr.HTML(HEADER_MAIN)
    gr.HTML(TOGGLE_HTML)
    inp=gr.Textbox(lines=4, label="Rese\u00f1a de cliente",
                   placeholder="Pega aqu\u00ed una rese\u00f1a de producto en ingl\u00e9s\u2026")
    btn=gr.Button("Analizar", variant="primary", elem_id="analizar-btn")
    out=gr.HTML()
    gr.Examples(examples=EJEMPLOS, inputs=inp, label="Ejemplos")
    btn.click(fn=analizar, inputs=inp, outputs=out, api_name="predict")
    inp.submit(fn=analizar, inputs=inp, outputs=out, api_name=False)
    gr.api(analizar_api, api_name="predict_json")

    gr.HTML(PANEL_HTML)
    gr.HTML('<div style="margin-top:28px;padding-top:14px;border-top:1px solid #f1f5f9;'
            'display:flex;justify-content:space-between;align-items:center;">'
            '<span style="font-size:.72rem;color:#cbd5e1;">Opyna &middot; UCM&nbsp;&ndash;&nbsp;NTIC 2026 &middot; Rogelio Emilio Rivero Contreras</span>'
            '<span style="font-size:.72rem;color:#cbd5e1;">DistilBERT + DeBERTa + LightGBM</span></div>')
if __name__=="__main__":
    _u=os.getenv("OPYNA_AUTH_USER")
    _p=os.getenv("OPYNA_AUTH_PASS")
    demo.launch(auth=(_u,_p) if _u and _p else None, auth_message=HEADER_LOGIN)

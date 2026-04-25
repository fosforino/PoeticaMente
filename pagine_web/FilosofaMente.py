import streamlit as st
from fpdf import FPDF
import os
import base64
import urllib.parse
import urllib.request
import json

# =========================
# FUNZIONI AUSILIARIE
# =========================

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def genera_pdf(titolo, autore, testo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 24)
    t_enc   = titolo.encode('latin-1', 'replace').decode('latin-1')
    a_enc   = f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1')
    txt_enc = testo.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 20, t_enc, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, a_enc, ln=True, align='R')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, txt_enc)
    return bytes(pdf.output(dest='S'))

def cerca_wikipedia(termine):
    try:
        termine_enc = urllib.parse.quote(termine)
        url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{termine_enc}"
        req = urllib.request.Request(url, headers={"User-Agent": "PoeticaMente/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            estratto = data.get("extract", "Nessun risultato trovato.")
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            return estratto, page_url
    except Exception:
        return "Nessun risultato trovato o errore di connessione.", ""

def apply_sacred_style():
    img_base64 = get_base64_image("assets/Fronte_3d.png")
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark">' if img_base64 else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital,wght@0,400;1,400&display=swap');

        .bg-watermark {{
            position: fixed; top:50%; left:50%;
            transform: translate(-50%, -50%);
            width: 70vw; opacity:0.05; filter: grayscale(100%);
            z-index:-1; pointer-events:none;
        }}
        .titolo-filosofaMente {{
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #1a1a1a;
            font-size: 3rem;
            letter-spacing: 10px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        .marmo-focus {{
            background: rgba(255,255,255,0.55);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(180,140,80,0.25);
            padding: 36px 40px;
            border-radius: 4px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.06);
            text-align: center;
            margin-bottom: 20px;
            position: relative; z-index:1;
        }}
        .nome-autore {{
            font-family: 'Cinzel', serif;
            font-size: 2rem;
            color: #5d4037;
            margin-bottom: 4px;
        }}
        .opera-unica {{
            font-family: 'Cinzel', serif;
            font-size: 0.85rem;
            color: #8d6e63;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .testo-stimolo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.85rem;
            line-height: 1.65;
            font-style: italic;
            color: #1a1a1a;
        }}
        .wiki-estratto {{
            font-family: 'EB Garamond', serif;
            font-size: 1.05rem;
            color: #2a1200;
            line-height: 1.7;
            background: rgba(255,251,240,0.9);
            border-left: 3px solid #c9a227;
            padding: 10px 14px;
            border-radius: 3px;
            max-height: 300px;
            overflow-y: auto;
        }}
        .link-risorsa {{
            display: inline-block;
            margin: 6px 4px 4px 0;
            padding: 5px 12px;
            background: #1a1008;
            color: #c9a227 !important;
            border: 1px solid #c9a227;
            border-radius: 4px;
            font-family: 'Cinzel', serif;
            font-size: 0.78rem;
            text-decoration: none;
            letter-spacing: 0.08em;
        }}
        .etichetta-sezione {{
            font-family: 'Cinzel', serif;
            font-size: 0.82rem;
            color: #5d4037;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-weight: 700;
        }}
        .stTextArea textarea {{
            background-color: rgba(255,255,255,0.5) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
            line-height: 1.8 !important;
        }}
        </style>
        {img_html}
    """, unsafe_allow_html=True)

# =========================
# FILOSOFI
# =========================
FILOSOFI = {
    "Socrate": {
        "opera": "Apologia",
        "testo": "L'unica vera sapienza è sapere di non sapere. Una vita senza ricerca non è degna di essere vissuta.",
        "anni": "470–399 a.C."
    },
    "Platone": {
        "opera": "Simposio",
        "testo": "Al tocco dell'amore, ognuno diventa poeta.",
        "anni": "428–348 a.C."
    },
    "Aristotele": {
        "opera": "Poetica",
        "testo": "La poesia è più filosofica e più seria della storia: la poesia tende a rappresentare l'universale, la storia il particolare.",
        "anni": "384–322 a.C."
    },
    "Kant": {
        "opera": "Critica della ragion pura",
        "testo": "Il cielo stellato sopra di me, la legge morale dentro di me.",
        "anni": "1724–1804"
    },
    "Hegel": {
        "opera": "Fenomenologia dello Spirito",
        "testo": "Ciò che è razionale è reale, e ciò che è reale è razionale.",
        "anni": "1770–1831"
    },
    "Schopenhauer": {
        "opera": "Il mondo come volontà e rappresentazione",
        "testo": "La vita è un pendolo che oscilla tra dolore e noia.",
        "anni": "1788–1860"
    },
    "Nietzsche": {
        "opera": "Così parlò Zarathustra",
        "testo": "Bisogna avere ancora un caos dentro di sé per partorire una stella danzante.",
        "anni": "1844–1900"
    },
    "Marx": {
        "opera": "Il Capitale",
        "testo": "La filosofia non ha mai fatto altro che interpretare il mondo; si tratta di trasformarlo.",
        "anni": "1818–1883"
    },
    "Leopardi": {
        "opera": "Zibaldone",
        "testo": "Il più solido piacere di questa vita è il piacer vano delle illusioni.",
        "anni": "1798–1837"
    },
    "Dante": {
        "opera": "Divina Commedia",
        "testo": "Considerate la vostra semenza: fatti non foste a viver come bruti, ma per seguir virtute e canoscenza.",
        "anni": "1265–1321"
    },
}

# =========================
# MAIN SHOW()
# =========================
def show():
    apply_sacred_style()

    st.markdown("<div class='titolo-filosofaMente'>FilosofaMente</div>", unsafe_allow_html=True)
    st.markdown("---")

    col_main, col_res = st.columns([1.7, 1])

    # ══════════════════════════════
    # COLONNA SINISTRA — FILOSOFO + SCRITTURA
    # ══════════════════════════════
    with col_main:
        nomi = ["Scegli una Scintilla..."] + list(FILOSOFI.keys())
        selezione = st.selectbox("✨ Quale anima vuoi consultare?", options=nomi)

        if selezione != "Scegli una Scintilla...":
            dati = FILOSOFI[selezione]

            st.markdown(f"""
                <div class="marmo-focus">
                    <div class="nome-autore">{selezione}</div>
                    <div class="opera-unica">{dati['opera']} &nbsp;·&nbsp; {dati['anni']}</div>
                    <div class="testo-stimolo">"{dati['testo']}"</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### ✍️ Le tue riflessioni")
            testo_key = f"filo_text_{selezione}"
            testo_iniziale = st.session_state.get(testo_key, "")
            testo = st.text_area(
                "Riflessioni",
                value=testo_iniziale,
                height=260,
                placeholder="Lascia che il pensiero del maestro illumini la tua penna...",
                key=f"area_{selezione}",
                label_visibility="collapsed"
            )
            st.session_state[testo_key] = testo

            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("💾 Salva", key=f"save_{selezione}", use_container_width=True):
                    st.success("Riflessione custodita.")
            with c2:
                if st.button("🗑️ Svuota", key=f"del_{selezione}", use_container_width=True):
                    st.session_state[testo_key] = ""
                    st.rerun()
            with c3:
                if testo:
                    pdf_data = genera_pdf(
                        f"Riflessione su {selezione}",
                        st.session_state.get('utente', 'Autore'),
                        testo
                    )
                    st.download_button(
                        "🖨️ PDF", data=pdf_data,
                        file_name=f"Riflessione_{selezione}.pdf",
                        key=f"pdf_{selezione}",
                        use_container_width=True
                    )
                else:
                    st.button("🖨️ PDF", disabled=True, use_container_width=True)

        else:
            st.markdown("""
                <div style='text-align:center; margin-top:60px; font-family: EB Garamond, serif;
                            font-size:1.3rem; color:#8d6e63; font-style:italic;'>
                    Scegli un'anima dal menu per evocarla...<br><br>
                    <span style='font-size:2.5rem;'>🕯️</span>
                </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════
    # COLONNA DESTRA — RISORSE
    # ══════════════════════════════
    with col_res:

        # ── PANNELLO WIKIPEDIA ──
        with st.expander("📖 Approfondisci su Wikipedia", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca un termine</div>", unsafe_allow_html=True)
            default_wiki = selezione if selezione != "Scegli una Scintilla..." else ""
            termine_wiki = st.text_input(
                "Termine Wikipedia",
                value=default_wiki,
                placeholder="es. Socrate, Nietzsche, esistenzialismo...",
                key="filo_wiki_cerca",
                label_visibility="collapsed"
            )
            if st.button("🔍 Cerca", key="filo_btn_wiki"):
                if termine_wiki.strip():
                    with st.spinner("Consultando Wikipedia..."):
                        estratto, wiki_url = cerca_wikipedia(termine_wiki.strip())
                    st.session_state["filo_wiki_risultato"] = estratto
                    st.session_state["filo_wiki_url"] = wiki_url
                else:
                    st.warning("Inserisci un termine.")

            if st.session_state.get("filo_wiki_risultato"):
                st.markdown(
                    f"<div class='wiki-estratto'>{st.session_state['filo_wiki_risultato']}</div>",
                    unsafe_allow_html=True
                )
                if st.session_state.get("filo_wiki_url"):
                    st.markdown(
                        f"<a class='link-risorsa' href='{st.session_state['filo_wiki_url']}' target='_blank'>🔗 Pagina completa</a>",
                        unsafe_allow_html=True
                    )
                if st.button("✖ Chiudi", key="filo_wiki_close"):
                    st.session_state["filo_wiki_risultato"] = ""
                    st.session_state["filo_wiki_url"] = ""
                    st.rerun()

        # ── PANNELLO ACCESSO RAPIDO ──
        with st.expander("🏛️ Accesso rapido ai Maestri", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca direttamente</div>", unsafe_allow_html=True)
            for nome in list(FILOSOFI.keys())[:5]:
                wiki_url = f"https://it.wikipedia.org/wiki/{urllib.parse.quote(nome)}"
                st.markdown(
                    f"<a class='link-risorsa' href='{wiki_url}' target='_blank'>📜 {nome}</a>",
                    unsafe_allow_html=True
                )

        # ── PANNELLO ATMOSFERA ──
        with st.expander("🎨 Personalizza Atmosfera", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Immagine di sfondo</div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Carica un'immagine", type=['png', 'jpg', 'jpeg'],
                key="filo_uploader"
            )
            link_image = st.text_input(
                "Oppure incolla un URL", placeholder="https://...",
                key="filo_bg_url"
            )
            if uploaded_file:
                st.image(uploaded_file, caption="Anteprima", use_container_width=True)
            elif link_image and link_image.startswith("http"):
                st.image(link_image, caption="Anteprima", use_container_width=True)


if __name__ == "__main__":
    show()
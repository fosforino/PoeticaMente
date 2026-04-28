import streamlit as st
from supabase import create_client
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

def genera_pdf(titolo, categoria, contenuto, autore):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, titolo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, contenuto.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Opera di: {autore}", ln=True, align='R')
    return pdf.output()

def cerca_wikipedia(termine):
    """Cerca su Wikipedia in italiano e restituisce estratto + URL."""
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

def cerca_immagini_unsplash(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://unsplash.com/s/photos/{termine_enc}"

def cerca_immagini_pixabay(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://pixabay.com/it/images/search/{termine_enc}/"

# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

        .titolo-scrittoio {
            font-family: 'Cinzel', serif !important;
            text-align: center;
            color: #432818;
            font-size: 2.4rem;
            margin-bottom: 10px;
            letter-spacing: 0.15em;
        }
        .pannello-risorse {
            background: rgba(255,251,240,0.85);
            border: 1px solid #d2b48c;
            border-radius: 6px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .wiki-estratto {
            font-family: 'EB Garamond', serif;
            font-size: 1.05rem;
            color: #2a1200;
            line-height: 1.7;
            background: rgba(255,251,240,0.9);
            border-left: 3px solid #c9a227;
            padding: 10px 14px;
            border-radius: 3px;
            max-height: 280px;
            overflow-y: auto;
        }
        .link-risorsa {
            display: inline-block;
            margin: 4px 4px 4px 0;
            padding: 5px 12px;
            background: #1a1008;
            color: #c9a227 !important;
            border: 1px solid #c9a227;
            border-radius: 4px;
            font-family: 'Cinzel', serif;
            font-size: 0.78rem;
            text-decoration: none;
            letter-spacing: 0.08em;
        }
        .link-risorsa:hover {
            background: #c9a227;
            color: #1a1008 !important;
        }
        .etichetta-sezione {
            font-family: 'Cinzel', serif;
            font-size: 0.85rem;
            color: #5d4037;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-weight: 700;
        }
        [data-testid="stWidgetLabel"] p {
            font-family: 'Cinzel', serif !important;
            font-size: 1rem !important;
            color: #5d4037 !important;
            font-weight: bold !important;
        }
        .stTextArea textarea {
            background-color: rgba(255,255,255,0.5) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
            line-height: 1.8 !important;
        }
        .stTextInput input {
            background: rgba(255,251,240,0.9) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Connessione ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home.")
        return

    nome_poeta = st.session_state.utente
    st.markdown(f"<div class='titolo-scrittoio'>Lo Scrittoio di {nome_poeta}</div>", unsafe_allow_html=True)
    st.markdown("---")

    # --- Recupero opere ---
    try:
        res = supabase.table("Opere").select("*").eq("autore", nome_poeta).execute()
        opere = res.data if res.data else []
    except:
        opere = []

    scelta = st.session_state.get("opera_selezionata", "✨ Nuova Opera")
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
    st.session_state["opere_lista"] = ["✨ Nuova Opera"] + [o['titolo'] for o in opere]

    v_titolo = opera_corrente['titolo'] if opera_corrente else ""
    v_testo  = opera_corrente['versi']  if opera_corrente else ""
    v_cat    = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"
    v_bg     = opera_corrente.get('sfondo', "")          if opera_corrente else ""

    # ─────────────────────────────────────────
    # LAYOUT: colonna scrittura | colonna risorse
    # ─────────────────────────────────────────
    col_write, col_res = st.columns([1.7, 1])

    # ══════════════════════════════
    # COLONNA SINISTRA — SCRITTURA
    # ══════════════════════════════
    with col_write:
        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
        with col_c:
            cat_list = ["Poesia", "Romanzo", "Canzone", "Saggio", "Racconto"]
            cat_idx  = cat_list.index(v_cat) if v_cat in cat_list else 0
            categoria = st.selectbox("Categoria", cat_list, index=cat_idx)

        contenuto = st.text_area(
            "✍️ Versi e Pensieri",
            value=v_testo,
            height=380,
            placeholder="Lascia scorrere le parole..."
        )

        pubblica = st.toggle(
            "📢 Affiggi in Bacheca",
            value=opera_corrente.get('pubblica', False) if opera_corrente else False
        )

        st.markdown("---")

        # --- Bottoni azione ---
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("💾 Custodisci", use_container_width=True):
                if titolo and contenuto:
                    dati = {
                        "titolo": titolo,
                        "versi": contenuto,
                        "categoria": categoria,
                        "autore": nome_poeta,
                        "pubblica": pubblica,
                        "sfondo": st.session_state.get("sfondo_url", v_bg)
                    }
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                        st.success("✅ Opera aggiornata.")
                    else:
                        supabase.table("Opere").insert(dati).execute()
                        st.success("✅ Opera custodita.")
                    st.rerun()
                else:
                    st.warning("✍️ Compila titolo e testo prima di custodire.")

        with b2:
            if titolo and contenuto:
                pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
                st.download_button(
                    "🖨️ Scarica PDF", 
                    bytes(pdf_data),  # Questa è la correzione fondamentale
                    f"{titolo}.pdf", 
                    "application/pdf",
                    use_container_width=True
                )
            else:
                st.button("🖨️ Scarica PDF", disabled=True, use_container_width=True)

        with b3:
            if opera_corrente:
                if st.button("🔥 Brucia", use_container_width=True):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.success("🔥 Opera eliminata.")
                    st.rerun()
            else:
                st.button("🔥 Brucia", disabled=True, use_container_width=True)

    # ══════════════════════════════
    # COLONNA DESTRA — RISORSE
    # ══════════════════════════════
    with col_res:

        # ── PANNELLO WIKIPEDIA ──
        with st.expander("📖 Cerca su Wikipedia", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca un termine</div>", unsafe_allow_html=True)
            termine_wiki = st.text_input(
                "Termine Wikipedia",
                placeholder="es. Leopardi, luna, esilio...",
                key="wiki_cerca",
                label_visibility="collapsed"
            )
            if st.button("🔍 Cerca", key="btn_wiki"):
                if termine_wiki.strip():
                    with st.spinner("Consultando Wikipedia..."):
                        estratto, wiki_url = cerca_wikipedia(termine_wiki.strip())
                    st.session_state["wiki_risultato"] = estratto
                    st.session_state["wiki_url"] = wiki_url
                else:
                    st.warning("Inserisci un termine.")

            if "wiki_risultato" in st.session_state and st.session_state["wiki_risultato"]:
                st.markdown(
                    f"<div class='wiki-estratto'>{st.session_state['wiki_risultato']}</div>",
                    unsafe_allow_html=True
                )
                if st.session_state.get("wiki_url"):
                    st.markdown(
                        f"<a class='link-risorsa' href='{st.session_state['wiki_url']}' target='_blank'>🔗 Apri pagina completa</a>",
                        unsafe_allow_html=True
                    )
                if st.button("✖ Chiudi risultato", key="btn_wiki_close"):
                    st.session_state["wiki_risultato"] = ""
                    st.session_state["wiki_url"] = ""
                    st.rerun()

        # ── PANNELLO IMMAGINI / SFONDO ──
        with st.expander("🖼️ Sfondo dell'Opera", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca ispirazione visiva</div>", unsafe_allow_html=True)
            termine_img = st.text_input(
                "Cerca immagini",
                placeholder="es. foresta, tramonto, manoscritto...",
                key="img_cerca",
                label_visibility="collapsed"
            )
            if termine_img.strip():
                u_link = cerca_immagini_unsplash(termine_img.strip())
                p_link = cerca_immagini_pixabay(termine_img.strip())
                st.markdown(
                    f"<a class='link-risorsa' href='{u_link}' target='_blank'>🌅 Unsplash</a>"
                    f"<a class='link-risorsa' href='{p_link}' target='_blank'>🖼 Pixabay</a>",
                    unsafe_allow_html=True
                )

            st.markdown("<div class='etichetta-sezione' style='margin-top:12px'>Incolla URL immagine</div>", unsafe_allow_html=True)
            bg_url = st.text_input(
                "URL sfondo",
                value=v_bg,
                placeholder="https://...",
                key="sfondo_url",
                label_visibility="collapsed"
            )
            if bg_url and bg_url.startswith("http"):
                st.image(bg_url, caption="Anteprima sfondo", use_container_width=True)

        # ── PANNELLO CONTEGGIO ──
        with st.expander("📊 Conteggio Opera", expanded=False):
            if contenuto:
                parole    = len(contenuto.split())
                caratteri = len(contenuto)
                versi     = contenuto.count('\n') + 1
                st.markdown(f"""
                    <div class='pannello-risorse'>
                        <div class='etichetta-sezione'>Statistiche</div>
                        📝 <b>Parole:</b> {parole}<br>
                        🔤 <b>Caratteri:</b> {caratteri}<br>
                        📜 <b>Versi/Righe:</b> {versi}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Inizia a scrivere per vedere le statistiche.")


if __name__ == "__main__":
    show()
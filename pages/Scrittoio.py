import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import base64

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
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, contenuto.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(20)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')


# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():

    # --- Watermark di sfondo ---
    path_icona = "PoeticaMente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = (
        f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-scrittoio">'
        if img_base64 else ""
    )

    # --- CSS globale Scrittoio ---
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

        .stApp {{
            background-color: #fdf5e6 !important;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
        }}

        .bg-watermark-scrittoio {{
            position: fixed; top: 50%; left: 55%;
            transform: translate(-50%, -50%);
            width: 50vw; opacity: 0.05;
            filter: blur(12px); z-index: -1;
            pointer-events: none;
        }}

        .stTextArea textarea {{
            border: 1px solid #c19a6b !important;
            border-radius: 5px !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.3rem !important;
            color: #3e2723 !important;
        }}

        /* === BOTTONI: colore per colonna === */
        div.stButton > button,
        div.stDownloadButton > button {{
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            padding: 0.6em 1.2em !important;
            border-radius: 8px !important;
            text-transform: uppercase;
            width: 100%;
            font-family: 'EB Garamond', serif !important;
            font-size: 1rem !important;
            transition: transform 0.1s ease, box-shadow 0.1s ease;
        }}

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {{
            transform: translateY(-2px);
            opacity: 0.92;
        }}

        /* Colonna 1 → Verde (Custodisci) */
        div[data-testid="column"]:nth-of-type(1) div.stButton > button {{
            background: #2e7d32 !important;
            box-shadow: 0 4px 0 #1b5e20 !important;
        }}

        /* Colonna 2 → Grigio ardesia (Stampa PDF) */
        div[data-testid="column"]:nth-of-type(2) div.stDownloadButton > button {{
            background: #455a64 !important;
            box-shadow: 0 4px 0 #263238 !important;
        }}

        /* Colonna 3 → Rosso scuro (Brucia) */
        div[data-testid="column"]:nth-of-type(3) div.stButton > button {{
            background: #8e0000 !important;
            box-shadow: 0 4px 0 #4a0000 !important;
        }}

        /* Bottoni conferma cancellazione */
        div[data-testid="column"]:nth-of-type(1) div.stButton > button[kind="secondary"],
        div[data-testid="column"]:nth-of-type(2) div.stButton > button[kind="secondary"] {{
            background: #555 !important;
            box-shadow: 0 4px 0 #333 !important;
        }}
        </style>
        {img_html}
    """, unsafe_allow_html=True)

    # --- Connessione Supabase ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # --- Controllo sessione ---
    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home per accedere allo Scrittoio.")
        return

    nome_poeta = st.session_state.utente
    st.markdown(
        f"<h1 style='text-align: center; color: #3e2723; font-family: EB Garamond, serif;'>"
        f"✒️ Lo Scrittoio di {nome_poeta}</h1>",
        unsafe_allow_html=True
    )

    # --- Recupero opere dell'autore ---
    try:
        res = (
            supabase.table("Opere")
            .select("*")
            .filter("autore", "eq", st.session_state.utente)
            .order("created_at", desc=True)
            .execute()
        )
        opere = res.data if res.data else []
    except Exception as e:
        st.error(f"Errore nel recupero delle opere: {e}")
        opere = []

    # --- Selezione opera dalla sidebar ---
    scelta = st.sidebar.selectbox(
        "📖 Carica un'opera:",
        ["✨ Nuova Opera"] + [o['titolo'] for o in opere]
    )
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)

    # --- Valori precompilati ---
    v_titolo   = opera_corrente['titolo']              if opera_corrente else ""
    v_testo    = opera_corrente['versi']               if opera_corrente else ""
    v_cat      = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"
    v_pubblica = opera_corrente.get('pubblica', False) if opera_corrente else False
    v_img      = opera_corrente.get('immagine_url', "") if opera_corrente else ""
    v_stile    = opera_corrente.get('stile_layout', {}) if opera_corrente else {}

    # --- Titolo e Categoria ---
    col_t, col_c = st.columns([2, 1])
    with col_t:
        titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
    with col_c:
        cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
        idx = cats.index(v_cat) if v_cat in cats else 0
        categoria = st.selectbox("Categoria", cats, index=idx)

    # --- Impostazioni grafiche ---
    with st.expander("🎨 Impostazioni Grafiche"):
        file_pc = st.file_uploader("💻 Carica immagine dal computer:", type=["jpg", "png", "jpeg"])
        img_url_manual = st.text_input("🔗 Oppure inserisci un link immagine:", value=v_img if v_img != "PC" else "")

        c1, c2 = st.columns(2)
        with c1:
            width_img = st.slider("Larghezza immagine (%)", 10, 100, int(v_stile.get("width", 100)))
        with c2:
            opac_img = st.slider("Opacità sfondo", 0.1, 1.0, float(v_stile.get("opacity", 0.4)))

        posizione = st.selectbox(
            "Posizione immagine",
            ["Sfondo", "Sopra il testo", "Sotto il testo"],
            index=["Sfondo", "Sopra il testo", "Sotto il testo"].index(v_stile.get("position", "Sfondo"))
        )

    # --- Gestione immagine ---
    img_final = img_url_manual
    if file_pc:
        b64 = base64.b64encode(file_pc.read()).decode()
        img_final = f"data:image/png;base64,{b64}"

    if img_final and posizione == "Sfondo":
        st.markdown(f"""
            <style>
            .stTextArea textarea {{
                background-image: url("{img_final}") !important;
                background-size: {width_img}% !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: local !important;
                background-blend-mode: lighten !important;
                background-color: rgba(255, 250, 240, {1 - opac_img}) !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    elif img_final and posizione != "Sfondo":
        st.markdown(
            f'<div style="text-align:center; opacity:{opac_img};">'
            f'<img src="{img_final}" style="width:{width_img}%;"></div>',
            unsafe_allow_html=True
        )

    # --- Area di scrittura ---
    contenuto = st.text_area("✍️ Versi e Pensieri", value=v_testo, height=400)
    pubblica = st.toggle("📢 Affiggi in Bacheca (Pubblica)", value=v_pubblica)

    # --- Inizializza stato conferma cancellazione ---
    if "conferma_cancella" not in st.session_state:
        st.session_state.conferma_cancella = False

    st.markdown("---")

    # ==============================
    # BOTTONI AZIONE
    # ==============================
    b1, b2, b3 = st.columns([1, 1, 1])

    # --- BOTTONE 1: Custodisci (Salva / Aggiorna) ---
    with b1:
        if st.button("💾 Custodisci", key="btn_salva", use_container_width=True):
            if titolo and contenuto:
                try:
                    stile_data = {"width": width_img, "opacity": opac_img, "position": posizione}
                    dati = {
                        "titolo": titolo,
                        "versi": contenuto,
                        "categoria": categoria,
                        "autore": nome_poeta,
                        "pubblica": pubblica,
                        "immagine_url": img_url_manual if not file_pc else "PC",
                        "stile_layout": stile_data
                    }
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                        st.success("✅ Opera aggiornata con cura.")
                    else:
                        supabase.table("Opere").insert(dati).execute()
                        st.success("✅ Opera custodita per l'eternità.")
                    st.session_state.conferma_cancella = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore durante il salvataggio: {e}")
            else:
                st.warning("⚠️ Mancano il titolo o i versi.")

    # --- BOTTONE 2: Scarica PDF ---
    with b2:
        if titolo and contenuto:
            pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
            st.download_button(
                label="🖨️ Scarica PDF",
                data=pdf_data,
                file_name=f"{titolo}.pdf",
                mime="application/pdf",
                key="btn_stampa",
                use_container_width=True
            )
        else:
            st.button("🖨️ Scarica PDF", disabled=True, use_container_width=True)

    # --- BOTTONE 3: Brucia (Elimina con conferma) ---
    with b3:
        if opera_corrente:
            if not st.session_state.conferma_cancella:
                if st.button("🗑️ Brucia", key="btn_cancella", use_container_width=True):
                    st.session_state.conferma_cancella = True
                    st.rerun()
            else:
                st.warning("⚠️ Sei sicuro di voler bruciare quest'opera?")
                c_si, c_no = st.columns(2)
                with c_si:
                    if st.button("🔥 Sì, brucia", use_container_width=True):
                        try:
                            supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                            st.session_state.conferma_cancella = False
                            st.toast("🔥 Opera bruciata.", icon="🔥")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Errore durante l'eliminazione: {e}")
                with c_no:
                    if st.button("❌ Annulla", use_container_width=True):
                        st.session_state.conferma_cancella = False
                        st.rerun()
        else:
            st.button("🗑️ Brucia", disabled=True, use_container_width=True)


# =========================
if __name__ == "__main__":
    show()
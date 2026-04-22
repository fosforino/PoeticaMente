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

    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, titolo, ln=True, align='C')

    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, contenuto)

    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Opera di: {autore}", ln=True, align='R')

    return pdf.output()

# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():
    st.markdown("""
        <style>
        .titolo-scrittoio {
            font-family: 'Cinzel', serif !important;
            text-align: center;
            color: #432818;
            font-size: 2.8rem;
            margin-bottom: 30px;
        }

        [data-testid="stWidgetLabel"] p {
            font-family: 'Cinzel', serif !important;
            font-size: 1.1rem !important;
            color: #5d4037 !important;
            font-weight: bold !important;
        }

        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.4) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.3rem !important;
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

    # --- Recupero opere ---
    try:
        res = supabase.table("Opere").select("*").eq("autore", nome_poeta).execute()
        opere = res.data if res.data else []
    except:
        opere = []

    # Il selectbox opere viene passato tramite session_state da app.py
    scelta = st.session_state.get("opera_selezionata", "✨ Nuova Opera")
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)

    # Aggiorna le opzioni disponibili in session_state per app.py
    st.session_state["opere_lista"] = ["✨ Nuova Opera"] + [o['titolo'] for o in opere]

    v_titolo = opera_corrente['titolo'] if opera_corrente else ""
    v_testo = opera_corrente['versi'] if opera_corrente else ""
    v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"
    v_bg = opera_corrente.get('sfondo', "") if opera_corrente else ""

    # --- Input ---
    col_t, col_c = st.columns([2, 1])
    with col_t:
        titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
    with col_c:
        categoria = st.selectbox("Categoria", ["Poesia", "Romanzo", "Canzone"], index=0)

    contenuto = st.text_area("✍️ Versi e Pensieri", value=v_testo, height=300)

    # =========================
    # SEZIONE SFONDO
    # =========================
    st.markdown("### 🖼️ Sfondo dell'Opera")

    bg_url = st.text_input(
        "Inserisci URL immagine (opzionale)",
        value=v_bg,
        placeholder="https://..."
    )

    if bg_url:
        st.image(bg_url, caption="Anteprima", use_container_width=True)

    pubblica = st.toggle("📢 Affiggi in Bacheca", value=opera_corrente.get('pubblica', False) if opera_corrente else False)

    st.markdown("---")

    # --- Bottoni ---
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
                    "sfondo": bg_url
                }
                if opera_corrente:
                    supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    st.success("Aggiornata")
                else:
                    supabase.table("Opere").insert(dati).execute()
                    st.success("Salvata")
                st.rerun()
            else:
                st.warning("Compila titolo e testo")

    with b2:
        if titolo and contenuto:
            pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
            st.download_button("🖨️ Scarica PDF", pdf_data, f"{titolo}.pdf", "application/pdf", use_container_width=True)
        else:
            st.button("🖨️ Scarica PDF", disabled=True, use_container_width=True)

    with b3:
        if opera_corrente:
            if st.button("🗑️ Brucia", use_container_width=True):
                supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                st.success("Cancellata")
                st.rerun()
        else:
            st.button("🗑️ Brucia", disabled=True, use_container_width=True)


if __name__ == "__main__":
    show()
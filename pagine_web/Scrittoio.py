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
    
    # Usiamo font standard che non danno problemi di codifica
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, titolo, ln=True, align='C')
    
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=12)
    # multi_cell gestisce i ritorni a capo del contenuto
    pdf.multi_cell(0, 10, contenuto)
    
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Opera di: {autore}", ln=True, align='R')
    
    # CORREZIONE CRUCIALE: output() senza argomenti restituisce già i byte
    return pdf.output()
    

# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():
    # --- CSS Specifico per lo Scrittoio (Sovrascrive il moderno con l'antico) ---
    st.markdown("""
        <style>
        /* Titolo della pagina solenne */
        .titolo-scrittoio {
            font-family: 'Cinzel', serif !important;
            text-align: center;
            color: #432818;
            font-size: 2.8rem;
            margin-bottom: 30px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }

        /* Etichette dei campi più nobili */
        [data-testid="stWidgetLabel"] p {
            font-family: 'Cinzel', serif !important;
            font-size: 1.1rem !important;
            color: #5d4037 !important;
            font-weight: bold !important;
        }

        /* Area di testo stile pergamena */
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.4) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.3rem !important;
            color: #1a1008 !important;
            line-height: 1.6 !important;
        }

        /* Uniformare tutti i bottoni dello scrittoio */
        div.stButton > button, div.stDownloadButton > button {
            background-color: #ffffff !important;
            color: #432818 !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'Cinzel', serif !important;
            font-weight: bold !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background-color: #bb9457 !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
        }

        /* Bottone BRUCIA (rosso antico) */
        div.stButton > button[key="btn_cancella"] {
            border-color: #9e2a2b !important;
            color: #9e2a2b !important;
        }
        
        div.stButton > button[key="btn_cancella"]:hover {
            background-color: #9e2a2b !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Connessione Supabase ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home per accedere allo Scrittoio.")
        return

    nome_poeta = st.session_state.utente
    st.markdown(f"<div class='titolo-scrittoio'>Lo Scrittoio di {nome_poeta}</div>", unsafe_allow_html=True)

    # --- Recupero opere ---
    try:
        res = supabase.table("Opere").select("*").filter("autore", "eq", nome_poeta).order("created_at", desc=True).execute()
        opere = res.data if res.data else []
    except:
        opere = []

    # Sidebar per caricamento
    scelta = st.sidebar.selectbox("📖 Carica un'opera:", ["✨ Nuova Opera"] + [o['titolo'] for o in opere])
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)

    v_titolo = opera_corrente['titolo'] if opera_corrente else ""
    v_testo = opera_corrente['versi'] if opera_corrente else ""
    v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

    # --- Interfaccia di Scrittura ---
    col_t, col_c = st.columns([2, 1])
    with col_t:
        titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
    with col_c:
        cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
        idx = cats.index(v_cat) if v_cat in cats else 0
        categoria = st.selectbox("Categoria", cats, index=idx)

    contenuto = st.text_area("✍️ Versi e Pensieri", value=v_testo, height=450)
    pubblica = st.toggle("📢 Affiggi in Bacheca", value=opera_corrente.get('pubblica', False) if opera_corrente else False)

    st.markdown("---")

    # --- Bottoni Azione ---
    b1, b2, b3 = st.columns(3)
    
    with b1:
        if st.button("💾 Custodisci", use_container_width=True):
            if titolo and contenuto:
                dati = {"titolo": titolo, "versi": contenuto, "categoria": categoria, "autore": nome_poeta, "pubblica": pubblica}
                if opera_corrente:
                    supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    st.success("Opera aggiornata.")
                else:
                    supabase.table("Opere").insert(dati).execute()
                    st.success("Opera custodita.")
                st.rerun()
            else:
                st.warning("Titolo e testo necessari.")

    with b2:
        if titolo and contenuto:
            pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
            st.download_button(label="🖨️ Scarica PDF", data=pdf_data, file_name=f"{titolo}.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.button("🖨️ Scarica PDF", disabled=True, use_container_width=True)

    with b3:
        if opera_corrente:
            if st.button("🗑️ Brucia", key="btn_cancella", use_container_width=True):
                supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                st.toast("🔥 Opera bruciata.")
                st.rerun()
        else:
            st.button("🗑️ Brucia", disabled=True, use_container_width=True)

if __name__ == "__main__":
    show()
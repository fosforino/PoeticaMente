import streamlit as st
from supabase import create_client
from fpdf import FPDF
from pydantic import BaseModel, Field # Per la validazione dati

# Modello dati con Pydantic
class Opera(BaseModel):
    titolo: str = Field(..., min_length=1)
    contenuto: str = Field(..., min_length=1)
    autore_email: str

def show():
    st.markdown("""
    <style>
        .stApp { background-image: url("https://www.transparenttextures.com/patterns/parchment.png") !important; }
        .stTextArea textarea { background-color: #fffaf0 !important; border: 1px solid #c19a6b !important; color: #3e2723 !important; font-family: 'EB Garamond', serif !important; font-size: 1.2rem !important; }
        div.stButton > button { border-radius: 8px !important; color: white !important; font-weight: bold !important; border: none !important; }
        div.stButton > button[key="btn_salva"] { background-color: #3e2723 !important; box-shadow: 0 5px 0 #1b100d !important; }
        div.stButton > button[key="btn_stampa"] { background-color: #1a237e !important; box-shadow: 0 5px 0 #0d1245 !important; }
        div.stButton > button[key="btn_cancella"] { background-color: #880e4f !important; box-shadow: 0 5px 0 #4a001f !important; }
        div.stButton > button:active { transform: translateY(3px) !important; box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    nome = st.session_state.get("utente")

    if not nome:
        st.warning("⚠️ Identificati nella Home.")
        return

    st.markdown(f"<h1>✒️ Lo Scrittoio di {nome}</h1>", unsafe_allow_html=True)

    res = supabase.table("Opere").select("*").eq("autore_email", nome).execute()
    opere = res.data or []

    scelta = st.sidebar.selectbox("📖 Manoscritti:", ["Nuova Opera"] + [o['titolo'] for o in opere])
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
    
    titolo = st.text_input("Titolo", value=opera_corrente['titolo'] if opera_corrente else "")
    testo = st.text_area("Versi", value=opera_corrente['contenuto'] if opera_corrente else "", height=350)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("💾 Salva", key="btn_salva"):
            try:
                # Validazione con Pydantic
                nuova_opera = Opera(titolo=titolo, contenuto=testo, autore_email=nome)
                dati = nuova_opera.model_dump()
                if opera_corrente:
                    supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                else:
                    supabase.table("Opere").insert(dati).execute()
                st.success("Versi salvati.")
                st.rerun()
            except Exception as e:
                st.error("Inserisci titolo e testo.")

    with b2:
        if st.button("🖨️ PDF", key="btn_stampa"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=f"{titolo}\n\n{testo}")
            st.download_button("Scarica PDF", data=pdf.output(dest='S').encode('latin-1'), file_name=f"{titolo}.pdf")

    with b3:
        if opera_corrente and st.button("🗑️ Brucia", key="btn_cancella"):
            supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
            st.rerun()
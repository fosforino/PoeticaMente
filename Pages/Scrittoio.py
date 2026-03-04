import streamlit as st
import time
from supabase import create_client, Client
from fpdf import FPDF
import io

# --- Config Supabase ---
URL = "https://eeavavlfgeeusijiljfw.supabase.co"
KEY = "sb_publishable_PP-gOScRnNcN9JiD4uN4lQ_hCN0xL7j"
supabase: Client = create_client(URL, KEY)

# --- Stile pergamena ---
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(to bottom, #fdf5e6, #f5e1b8) !important;
    color: #2b1d0e !important; 
    font-family: 'EB Garamond', serif !important; 
    padding: 20px !important;
}
.stTextArea textarea, .stTextInput input { 
    background-color: #fff8dc !important; 
    border: 1px solid #d4af37 !important; 
    font-size: 1.2rem !important;
    padding: 10px !important;
    border-radius: 5px !important;
}
.stButton button { 
    background-color: #2b1d0e !important; 
    color: #fdf5e6 !important; 
    border: 1px solid #d4af37 !important; 
    font-family: 'Playfair Display', serif !important; 
    border-radius: 5px !important;
}
</style>
""", unsafe_allow_html=True)

# --- Lista parole vietate ---
parole_vietate = [
    "odio", "razzismo", "violenza", "anarchia", "terrorismo",
    "discriminazione", "uccidi", "bomb", "assassino"
]

# --- Funzioni ---
def verifica_parole_verse(versi):
    versi_lower = versi.lower()
    for parola in parole_vietate:
        if parola in versi_lower:
            return parola
    return None

def pubblica_opera(titolo, versi):
    data = {
        "titolo": titolo,
        "versi": versi,
        "tipo_account": "demo",
        "autore": "Poeta_Anonimo",
        "likes": 0,
        "approvata": True  # approvata automaticamente se passa filtro
    }
    try:
        supabase.table("Poesie").insert(data).execute()
        return True
    except:
        return False

def genera_pdf(titolo, versi):
    pdf = FPDF()
    pdf.add_page()
    # Bordo dorato
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.5)
    pdf.rect(5, 5, 200, 287)
    # Titolo
    pdf.set_font("Times", 'B', 24)
    pdf.set_text_color(26, 26, 26)
    pdf.cell(0, 20, titolo, ln=True, align='C')
    pdf.ln(10)
    # Testo
    pdf.set_font("Times", '', 14)
    pdf.multi_cell(0, 10, versi, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- Interfaccia ---
st.title("🖋️ Scrittoio")
tit_inp = st.text_input("Titolo dell'Opera")
ver_inp = st.text_area("I tuoi versi", height=450)

if st.button("🚀 PUBBLICA NELL'ALBO"):
    parola_vietata = verifica_parole_verse(ver_inp)
    if parola_vietata:
        st.error(f"❌ La parola '{parola_vietata}' è vietata. Modifica i versi per pubblicare.")
    elif tit_inp.strip() == "" or ver_inp.strip() == "":
        st.error("Compila titolo e versi prima di pubblicare.")
    else:
        if pubblica_opera(tit_inp, ver_inp):
            st.success("Opera salvata nell'Albo Poetico!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("Errore durante il salvataggio.")

st.markdown("---")
if tit_inp and ver_inp:
    pdf_data = genera_pdf(tit_inp, ver_inp)
    st.download_button(
        label="📥 SCARICA PERGAMENA PDF",
        data=pdf_data,
        file_name=f"{tit_inp}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.write("Scrivi qualcosa per generare il PDF.")
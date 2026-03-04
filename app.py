import streamlit as st
import time
from supabase import create_client, Client
from fpdf import FPDF
import io

# --- 1. CONFIGURAZIONE SUPABASE ---
URL = "https://eeavavlfgeeusijiljfw.supabase.co"
KEY = "sb_publishable_PP-gOScRnNcN9JiD4uN4lQ_hCN0xL7j"
supabase: Client = create_client(URL, KEY)

# --- 2. CONFIGURAZIONE ESTETICA ---
st.set_page_config(page_title="Poeticamente", page_icon="🖋️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    .stApp { background-color: #fdf5e6 !important; color: #2b1d0e !important; font-family: 'EB Garamond', serif !important; }
    .poetic-title { font-family: 'Playfair Display', serif; font-size: 4rem; text-align: center; color: #1a1a1a; margin-top: -40px; }
    .stButton button { background-color: #2b1d0e !important; color: #fdf5e6 !important; border: 1px solid #d4af37 !important; font-family: 'Playfair Display', serif !important; border-radius: 0px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    .stTextArea textarea { background-color: rgba(255,255,255,0.2) !important; border: 1px solid #d4af37 !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA FUNZIONALE ---
def conta_opere_demo():
    try:
        res = supabase.table("Poesie").select("id", count="exact").eq("tipo_account", "demo").execute()
        return res.count if res.count is not None else 0
    except: return 0

def pubblica_opera(titolo, versi):
    data = {"titolo": titolo, "versi": versi, "tipo_account": "demo", "autore": "Poeta_Anonimo", "likes": 0}
    try:
        supabase.table("Poesie").insert(data).execute()
        return True
    except: return False

def genera_pdf(titolo, versi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", '', 14)
    pdf.multi_cell(0, 10, versi, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFACCIA ---
st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)

conteggio_reale = conta_opere_demo()

col_scrit, col_stat = st.columns([2, 1], gap="large")

with col_scrit:
    tit_inp = st.text_input("Titolo dell'Opera", placeholder="Il nome della tua creazione...")
    ver_inp = st.text_area("I tuoi versi", height=450, placeholder="Lascia che l'ispirazione fluisca...")

with col_stat:
    st.markdown("### 📜 Il tuo Registro")
    st.write(f"Opere pubblicate: **{conteggio_reale}**")
    st.success("Atelier aperto a tutti. Pubblicazione libera e gratuita.")

    if st.button("🚀 PUBBLICA NELL'ALBO", use_container_width=True):
        if tit_inp and ver_inp:
            if pubblica_opera(tit_inp, ver_inp):
                st.success("Opera salvata nell'Albo Poetico!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Errore durante il salvataggio.")
        else:
            st.error("L'opera è incompleta.")

    st.markdown("---")
    st.markdown("### 💾 Esportazione")
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
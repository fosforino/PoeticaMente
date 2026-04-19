import streamlit as st
from supabase import create_client
import os
import json
from fpdf import FPDF
import io

def genera_pdf(opere, autore):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 20)
    pdf.cell(0, 10, f"Archivio di {autore}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Times", size=12)
    
    for o in opere:
        titolo = o['titolo']
        categoria = o.get('categoria','Poesia')
        versi = o['versi']
        
        pdf.set_font("Times", 'B', 14)
        pdf.cell(0, 8, f"{titolo} ({categoria})", ln=True)
        pdf.set_font("Times", size=12)
        pdf.multi_cell(0, 8, versi)
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

def show():
    st.markdown("<h1 style='text-align:center;'>Archivio Opere</h1>", unsafe_allow_html=True)
    
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    if "utente" in st.session_state:
        utente = st.session_state.utente
        try:
            res = supabase.table("Opere").select("*").filter("autore", "eq", utente).order("created_at", desc=True).execute()
            opere = res.data if res.data else []
        except Exception as e:
            st.error(f"Errore recupero opere: {e}")
            opere = []
        
        if opere:
            for o in opere:
                st.markdown(f"### {o['titolo']} ({o.get('categoria','Poesia')})")
                st.markdown(f"{o['versi']}")
                st.markdown("---")
            
            # Download PDF di tutto l'archivio
            pdf_data = genera_pdf(opere, utente)
            st.download_button(
                label="📥 Scarica PDF dell'Archivio",
                data=pdf_data,
                file_name=f"archivio_{utente}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("Non ci sono opere salvate per questo utente.")
    else:
        st.warning("Identificati nella Home per vedere le tue opere.")
    
if __name__ == "__main__":
    show()
import streamlit as st
from supabase import create_client
import os
from fpdf import FPDF

def genera_pdf_singola(opera):
    def pulisci_testo(testo):
        sostituzioni = {
            '\u2014': '--',
            '\u2013': '-',
            '\u2018': "'",
            '\u2019': "'",
            '\u201c': '"',
            '\u201d': '"',
            '\u2026': '...',
            '\u00ab': '<<',
            '\u00bb': '>>',
        }
        for carattere, sostituto in sostituzioni.items():
            testo = testo.replace(carattere, sostituto)
        return testo.encode('latin-1', errors='replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()

    titolo = pulisci_testo(opera.get('titolo', ''))
    categoria = pulisci_testo(opera.get('categoria', 'Poesia'))
    versi = pulisci_testo(opera.get('versi', ''))
    autore = pulisci_testo(opera.get('autore', ''))

    pdf.set_font("Times", 'B', 18)
    pdf.cell(0, 10, titolo, ln=True, align='C')
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 8, f"({categoria})", ln=True, align='C')
    pdf.ln(8)
    pdf.set_font("Times", size=13)
    pdf.multi_cell(0, 8, versi)
    pdf.ln(5)
    pdf.set_font("Times", 'I', 11)
    pdf.cell(0, 8, f"-- {autore}", ln=True, align='R')

    return bytes(pdf.output(dest='S'))

def show():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');
        .stApp { background-color: #fdf5e6; color: #3e2723; }
        .opera-titolo {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            color: #3e2723;
            text-align: center;
        }
        .opera-testo {
            font-family: 'EB Garamond', serif;
            font-size: 1.15rem;
            line-height: 1.7;
            color: #2c2c2c;
            white-space: pre-wrap;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; font-family:\"Playfair Display\",serif;'>Archivio Opere</h1>", unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("Identificati nella Home per vedere le tue opere.")
        return

    utente = st.session_state.utente
    try:
        res = supabase.table("Opere").select("*").filter("autore", "eq", utente).order("created_at", desc=True).execute()
        opere = res.data if res.data else []
    except Exception as e:
        st.error(f"Errore recupero opere: {e}")
        return

    if not opere:
        st.info("Non ci sono opere salvate.")
        return

    for o in opere:
        id_opera = o.get('id')
        titolo = o.get('titolo', 'Senza Titolo')
        categoria = o.get('categoria', 'Poesia')
        versi = o.get('versi', '')
        autore = o.get('autore', '')

        st.markdown(f"<div class='opera-titolo'>{titolo} · <span style='font-size:1rem; color:#c19a6b;'>{categoria}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='opera-testo'>{versi}</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            pdf_data = genera_pdf_singola(o)
            st.download_button(
                label="📥 Scarica PDF",
                data=pdf_data,
                file_name=f"{titolo}.pdf",
                mime="application/pdf",
                key=f"pdf_{id_opera}"
            )

        with col3:
            with st.popover("🔥 Brucia"):
                st.warning(f"Vuoi eliminare **{titolo}** per sempre?")
                if st.button("Sì, elimina", key=f"del_{id_opera}", type="primary"):
                    try:
                        supabase.table("Opere").delete().eq("id", id_opera).execute()
                        st.success("Opera eliminata.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore: {e}")

        st.markdown("<hr style='border-color: rgba(193,154,107,0.3); margin: 30px 0;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
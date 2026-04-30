import streamlit as st
from supabase import create_client
import os
import urllib.parse
import base64
from fpdf import FPDF
from utils import nav_bar, carica_css 

# =========================
# FUNZIONI AUSILIARIE
# =========================

def genera_pdf_singola(opera):
    def pulisci_testo(testo):
        if not testo: return ""
        sostituzioni = {
            '\u2014': '--', '\u2013': '-', '\u2018': "'",
            '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2026': '...', '\u00ab': '<<', '\u00bb': '>>',
        }
        for carattere, sostituto in sostituzioni.items():
            testo = testo.replace(carattere, sostituto)
        return testo.encode('latin-1', errors='replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    
    titolo = pulisci_testo(opera.get('titolo', 'Senza Titolo'))
    categoria = pulisci_testo(opera.get('categoria', 'Poesia'))
    versi = pulisci_testo(opera.get('versi', ''))
    autore = pulisci_testo(opera.get('autore', 'Anonimo'))

    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo, align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"({categoria})", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, versi)
    
    pdf.ln(20)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Affissa da: {autore}", align='R', new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():
    carica_css()
    nav_bar()
    
    st.markdown("""
        <style>
        .titolo-bacheca {
            font-family: 'Cinzel', serif !important;
            text-align: center;
            color: #432818;
            font-size: 2.8rem;
            margin-bottom: 30px;
        }
        .poesia-card {
            background-color: rgba(255, 250, 240, 0.95);
            border-radius: 12px;
            border: 1px solid rgba(193, 154, 107, 0.4);
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            margin-bottom: 10px;
            padding: 40px;
            position: relative;
        }
        .card-categoria {
            color: #c19a6b;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-family: 'Cinzel', serif;
            margin-bottom: 10px;
        }
        .titolo-opera-card {
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            color: #2c1a0e;
            margin-bottom: 20px;
        }
        .versi-testo {
            font-family: 'EB Garamond', serif;
            font-size: 1.4rem;
            line-height: 1.7;
            white-space: pre-wrap;
            color: #432818;
            margin: 30px 0;
        }
        .firma-autore {
            text-align: right;
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 1.2rem;
            color: #5d4037;
        }
        .social-link {
            text-decoration: none;
            font-size: 0.8rem;
            color: #bb9457;
            border: 1px solid #bb9457;
            padding: 6px 12px;
            border-radius: 4px;
            margin-right: 8px;
            display: inline-block;
            font-family: 'Cinzel', serif;
            transition: 0.3s;
        }
        .social-link:hover {
            background-color: #bb9457;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='titolo-bacheca'>🏛️ La Grande Bacheca</div>", unsafe_allow_html=True)

    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home per vedere le opere affisse.")
        return

    try:
        # Recuperiamo solo le opere pubbliche
        res = supabase.table("Opere").select("*").eq("pubblica", True).order("created_at", desc=True).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("""
                🕯️ **La Bacheca è in attesa di ispirazione.**
                
                Al momento non ci sono opere affisse. Se hai scritto qualcosa nello **Scrittoio**, 
                ricordati di attivare l'interruttore **'Affiggi in Bacheca'** e cliccare su **'Custodisci'** 
                per mostrare i tuoi versi alla comunità.
            """)
            return

        _, col_centrale, _ = st.columns([0.1, 0.8, 0.1])

        with col_centrale:
            for p in poemi:
                id_opera = p.get('id')
                titolo = p.get('titolo', 'Senza Titolo')
                testo = p.get('versi', '')
                autore = p.get('autore', 'Anonimo')
                categoria = p.get('categoria', 'Poesia')

                # Card visiva
                st.markdown(f"""
                    <div class="poesia-card">
                        <div class="card-categoria">{categoria}</div>
                        <div class="titolo-opera-card">{titolo}</div>
                        <div class="versi-testo">{testo}</div>
                        <div class="firma-autore">— {autore}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Social & Action Bar
                c_social, c_pdf, c_action = st.columns([2.5, 0.8, 0.8])
                
                testo_share = f"*{titolo}*\n\n{testo}\n\n— {autore}"
                testo_url = urllib.parse.quote(testo_share)

                with c_social:
                    st.markdown(f"""
                        <div style="margin-bottom: 40px;">
                            <a href="https://wa.me/?text={testo_url}" target="_blank" class="social-link">WhatsApp</a>
                            <a href="mailto:?body={testo_url}" class="social-link">Email</a>
                        </div>
                    """, unsafe_allow_html=True)

                with c_pdf:
                    pdf_bytes = genera_pdf_singola(p)
                    st.download_button("📥 PDF", data=pdf_bytes, file_name=f"{titolo}.pdf", mime="application/pdf", key=f"pdf_{id_opera}", use_container_width=True)

                with c_action:
                    if autore == st.session_state.utente:
                        with st.popover("🔥 Brucia"):
                            st.write("Eliminare definitivamente?")
                            if st.button("Sì, distruggi", key=f"del_{id_opera}", type="primary", use_container_width=True):
                                supabase.table("Opere").delete().eq("id", id_opera).execute()
                                st.rerun()
                    else:
                        with st.popover("🚩 Segnala"):
                            st.write("Contenuto inappropriato?")
                            motivo = st.selectbox("Motivo", ["Plagio", "Offensivo", "Spam"], key=f"mot_{id_opera}")
                            if st.button("Invia", key=f"btn_{id_opera}", use_container_width=True):
                                st.success("Inviata.")

                st.markdown("<hr style='border:0; border-top:1px solid rgba(193,154,107,0.2); margin-bottom:40px;'>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Errore tecnico: {e}")

if __name__ == "__main__":
    show()

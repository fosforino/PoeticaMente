import streamlit as st
from supabase import create_client
import os
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
        # Codifica pulita per evitare crash binari
        return testo.encode('latin-1', errors='replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()

    titolo = pulisci_testo(opera.get('titolo', 'Senza Titolo'))
    categoria = pulisci_testo(opera.get('categoria', 'Poesia'))
    versi = pulisci_testo(opera.get('versi', ''))
    autore = pulisci_testo(opera.get('autore', ''))

    # Intestazione PDF con standard FPDF2
    pdf.set_font("Times", 'B', 18)
    pdf.cell(0, 10, titolo, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 8, f"({categoria})", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    # Corpo del testo
    pdf.set_font("Times", size=13)
    pdf.multi_cell(0, 8, versi)
    pdf.ln(10)
    
    # Firma
    pdf.set_font("Times", 'I', 11)
    pdf.cell(0, 8, f"-- {autore}", align='R', new_x="LMARGIN", new_y="NEXT")

    # RITORNO IN BYTES (Risolve errore bytearray terminale)
    return bytes(pdf.output())

# =========================
# MAIN SHOW()
# =========================

def show():
    carica_css()
    nav_bar()
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');
        
        .titolo-pagina-archivio {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #2c1a0e;
            font-size: 2.8rem;
            margin-bottom: 40px;
            text-transform: uppercase;
            letter-spacing: 4px;
        }

        .opera-titolo {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #3e2723;
            text-align: center;
            margin-top: 20px;
        }

        .opera-testo {
            font-family: 'EB Garamond', serif;
            font-size: 1.25rem;
            line-height: 1.7;
            color: #2c2c2c;
            white-space: pre-wrap;
            background: rgba(255, 255, 255, 0.4);
            padding: 30px;
            border-radius: 8px;
            border: 1px solid rgba(193, 154, 107, 0.3);
            margin: 20px 0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.03);
        }
        
        .status-badge {
            font-size: 0.8rem;
            padding: 3px 8px;
            border-radius: 10px;
            font-family: 'Cinzel';
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='titolo-pagina-archivio'>📚 Il Tuo Archivio</div>", unsafe_allow_html=True)

    # Connessione Supabase
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home per accedere al tuo archivio personale.")
        return

    utente = st.session_state.utente
    
    try:
        # Recupero opere dell'utente
        res = supabase.table("Opere").select("*").eq("autore", utente).order("created_at", desc=True).execute()
        opere = res.data if res.data else []
    except Exception as e:
        st.error(f"Errore nel recupero dell'archivio: {e}")
        return

    if not opere:
        st.info("📜 Il tuo calamaio è ancora pieno. Le opere che custodirai nello Scrittoio appariranno qui.")
        return

    # Visualizzazione centralizzata
    _, col_centrale, _ = st.columns([0.05, 0.9, 0.05])

    with col_centrale:
        for o in opere:
            id_opera = o.get('id')
            titolo = o.get('titolo', 'Senza Titolo')
            categoria = o.get('categoria', 'Poesia')
            versi = o.get('versi', '')
            is_pubblico = o.get('pubblica', False)

            # Header Opera con indicazione di stato (Pubblico/Privato)
            stato_label = "🌐 PUBBLICA" if is_pubblico else "🔒 PRIVATA"
            stato_color = "#2e7d32" if is_pubblico else "#757575"
            
            st.markdown(f"""
                <div class='opera-titolo'>
                    {titolo} <br>
                    <span style='font-size:0.9rem; color:#c19a6b; font-family:Cinzel;'>{categoria}</span> 
                    <span class='status-badge' style='background:{stato_color}22; color:{stato_color}; border:1px solid {stato_color}'> {stato_label} </span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='opera-testo'>{versi}</div>", unsafe_allow_html=True)

            # Azioni
            c_null, c_pdf, c_del = st.columns([2, 1, 1])

            with c_pdf:
                pdf_data = genera_pdf_singola(o)
                st.download_button(
                    label="📥 PDF",
                    data=pdf_data,
                    file_name=f"{titolo}.pdf",
                    mime="application/pdf",
                    key=f"pdf_arch_{id_opera}",
                    use_container_width=True
                )

            with c_del:
                with st.popover("🔥 Brucia", use_container_width=True):
                    st.write(f"Confermi di voler distruggere definitivamente questo manoscritto?")
                    if st.button("Sì, nell'oblio", key=f"del_arch_{id_opera}", type="primary", use_container_width=True):
                        supabase.table("Opere").delete().eq("id", id_opera).execute()
                        st.toast(f"'{titolo}' è cenere.")
                        st.rerun()

            st.markdown("<hr style='border-color: rgba(193,154,107,0.15); margin: 30px 0;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()

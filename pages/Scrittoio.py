import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import urllib.parse
import urllib.request
import json
from utils import nav_bar, carica_css 

# =========================
# FUNZIONI AUSILIARI
# =========================

def genera_pdf(titolo, categoria, contenuto, autore):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    t_enc = titolo.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 20, t_enc, align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    txt_enc = contenuto.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt_enc)
    
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Opera di: {autore}", align='R', new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())

def cerca_wikipedia(termine):
    try:
        termine_enc = urllib.parse.quote(termine)
        url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{termine_enc}"
        req = urllib.request.Request(url, headers={"User-Agent": "PoeticaMente/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("extract", "Nessun risultato trovato.")
    except Exception:
        return "Errore di connessione o termine non trovato."

# =========================
# FUNZIONE PRINCIPALE
# =========================

def show():
    carica_css()
    nav_bar()
    
    st.markdown("""
        <style>
        .titolo-scrittoio {
            font-family: 'Cinzel', serif !important;
            text-align: center;
            color: #432818;
            font-size: 2.2rem;
            margin-bottom: 25px;
        }
        .stTextArea textarea {
            background-color: rgba(255,255,255,0.6) !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
        }
        .guida-bacheca {
            font-family: 'EB Garamond', serif;
            font-size: 0.95rem;
            color: #5d4037;
            background: rgba(187, 148, 87, 0.1);
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #bb9457;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home per accedere allo Scrittoio.")
        return

    nome_poeta = st.session_state.utente
    st.markdown(f"<div class='titolo-scrittoio'>Lo Scrittoio di {nome_poeta}</div>", unsafe_allow_html=True)

    try:
        res = supabase.table("Opere").select("*").eq("autore", nome_poeta).execute()
        opere = res.data if res.data else []
    except:
        opere = []

    # SELETTORE ACCORCIATO
    col_sel, _ = st.columns([1, 1])
    with col_sel:
        opere_nomi = ["✨ Nuova Opera"] + [o['titolo'] for o in opere]
        scelta = st.selectbox("📖 I tuoi manoscritti", opere_nomi, key="selettore_opere_scrittoio")

    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)

    v_titolo = opera_corrente['titolo'] if opera_corrente else ""
    v_testo  = opera_corrente['versi']  if opera_corrente else ""
    v_cat    = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"
    v_pub    = opera_corrente.get('pubblica', False) if opera_corrente else False

    st.markdown("---")

    col_left, col_right = st.columns([1.7, 1], gap="medium")

    with col_left:
        c1, c2 = st.columns([2, 1])
        with c1:
            titolo = st.text_input("Titolo", value=v_titolo, key=f"t_{scelta}")
        with c2:
            cat_list = ["Poesia", "Romanzo", "Saggio", "Racconto", "Riflessione"]
            idx_cat = cat_list.index(v_cat) if v_cat in cat_list else 0
            categoria = st.selectbox("Categoria", cat_list, index=idx_cat, key=f"c_{scelta}")

        testo = st.text_area("✍️ Componi i tuoi versi", value=v_testo, height=450, key=f"v_{scelta}")

        # --- SEZIONE AFFISSIONE INTUITIVA ---
        st.markdown("""
            <div class='guida-bacheca'>
                💡 <b>Nota del Poeta:</b> I tuoi versi sono privati. 
                Per condividerli in <b>Bacheca</b>, attiva l'interruttore qui sotto e clicca su <b>Custodisci</b>.
            </div>
        """, unsafe_allow_html=True)
        
        pubblica = st.toggle("📢 Affiggi in Bacheca", value=v_pub, key=f"p_{scelta}")
        
        if pubblica:
            st.caption("✨ *Questa opera sarà visibile a tutti nella pagina Bacheca.*")
        else:
            st.caption("🔒 *Questa opera resterà privata nel tuo Scrittoio.*")

        # Bottoni Azione
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("💾 Custodisci", use_container_width=True):
                if titolo and testo:
                    dati = {
                        "titolo": titolo, "versi": testo, "categoria": categoria,
                        "autore": nome_poeta, "pubblica": pubblica
                    }
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati).execute()
                    st.rerun()

        with b2:
            if titolo and testo:
                pdf_bytes = genera_pdf(titolo, categoria, testo, nome_poeta)
                st.download_button("🖨️ Scarica PDF", data=pdf_bytes, file_name=f"{titolo}.pdf", use_container_width=True)

        with b3:
            if opera_corrente:
                if st.button("🔥 Brucia", use_container_width=True):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()

    with col_right:
        with st.expander("📖 Ispirazione (Wikipedia)", expanded=False):
            termine = st.text_input("Cerca termine", key="wiki_in")
            if st.button("🔍 Consulta"):
                if termine:
                    st.markdown(f"<div style='font-size:0.9rem;'>{cerca_wikipedia(termine)}</div>", unsafe_allow_html=True)

        with st.expander("📊 Metrica", expanded=True):
            st.metric("Parole", len(testo.split()))
            st.metric("Caratteri", len(testo))

if __name__ == "__main__":
    show()
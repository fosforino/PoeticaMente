import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import base64
import urllib.parse
import urllib.request
import json
from utils import nav_bar, carica_css 

# =========================
# FUNZIONI AUSILIARIE
# =========================

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def genera_pdf(titolo, autore, testo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 24)
    t_enc = titolo.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 20, t_enc, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    a_enc = f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 10, a_enc, align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    txt_enc = testo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt_enc)
    
    # SOLUZIONE ERRORE BYTEARRAY: Forziamo il ritorno in bytes puri
    return bytes(pdf.output())

def cerca_wikipedia(termine):
    try:
        termine_enc = urllib.parse.quote(termine)
        url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{termine_enc}"
        req = urllib.request.Request(url, headers={"User-Agent": "PoeticaMente/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            estratto = data.get("extract", "Nessun risultato trovato.")
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            return estratto, page_url
    except Exception:
        return "Nessun risultato trovato o errore di connessione.", ""

# =========================
# DATABASE ANTROPOLOGI
# =========================

ANTROPOLOGI = {
    "Claude Lévi-Strauss": {
        "opera": "Tristi Tropici",
        "testo": "Il mondo è cominciato senza l'uomo e finirà senza di lui. Le istituzioni, i costumi, gli usi che avrò passato la mia vita a catalogare non sono che un'effimera fioritura.",
        "anni": "1908-2009"
    },
    "Margaret Mead": {
        "opera": "Coming of Age in Samoa",
        "testo": "Mai dubitare che un piccolo gruppo di cittadini pensanti e impegnati possa cambiare il mondo. In realtà, è l'unica cosa che lo abbia mai fatto.",
        "anni": "1901-1978"
    },
    "Bronisław Malinowski": {
        "opera": "Argonauti del Pacifico Occidentale",
        "testo": "L'antropologia è lo studio dell'uomo che abbraccia la donna.",
        "anni": "1884-1942"
    },
    "Franz Boas": {
        "opera": "La mente dell'uomo primitivo",
        "testo": "La civiltà non è qualcosa di assoluto, ma è relativa, e le nostre idee e concezioni sono vere solo nella misura in cui la nostra civiltà è valida.",
        "anni": "1858-1942"
    },
    "Clifford Geertz": {
        "opera": "Interpretazione di Culture",
        "testo": "L'uomo è un animale sospeso nelle reti di significato che lui stesso ha tessuto. La cultura è quella rete.",
        "anni": "1926-2006"
    },
    "Ernesto De Martino": {
        "opera": "Sud e Magia",
        "testo": "Il folklore non è un museo di curiosità arcaiche, ma una civiltà dello spirito che risponde a bisogni profondi dell'esistenza umana.",
        "anni": "1908-1965"
    },
    "Vincenzo Esposito": {
        "opera": "Comunità e Identità",
        "testo": "L'identità di un popolo non si conserva nei libri, ma nelle mani di chi lavora, nella voce di chi canta, nel silenzio di chi ricorda.",
        "anni": "XX sec."
    },
}

SITI_ANTROPOLOGIA = [
    {"nome": "🌍 Wenner-Gren Foundation", "url": "https://www.wennergren.org"},
    {"nome": "🏛️ American Anthropological Assoc.", "url": "https://www.americananthro.org"},
    {"nome": "📚 SIAM - Società Italiana Antropologia", "url": "https://www.antropologiaetnologia.it/"},
]

# =========================
# MAIN SHOW()
# =========================

def show():
    carica_css()
    nav_bar()
    
    st.markdown("""
        <style>
        .titolo-antropologaMente {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #2c1a0e;
            font-size: 2.6rem;
            letter-spacing: 6px;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .riquadro-antropologo {
            background: rgba(255,248,235,0.75);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(180,120,50,0.25);
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 25px;
        }
        .nome-antropologo {
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            color: #5d3a1a;
        }
        .testo-antropologo {
            font-family: 'EB Garamond', serif;
            font-size: 1.6rem;
            line-height: 1.5;
            font-style: italic;
            color: #2c1a0e;
            margin-top: 15px;
        }
        .wiki-estratto {
            font-family: 'EB Garamond', serif;
            font-size: 0.95rem;
            background: #fffdfa;
            padding: 10px;
            border-left: 3px solid #bb9457;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='titolo-antropologaMente'>AntropologaMente</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-family:EB Garamond; font-style:italic;'>L'uomo che studia l'uomo</p>", unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home.")
        return

    nome_poeta = st.session_state.utente

    col_main, col_res = st.columns([1.7, 1], gap="large")

    with col_main:
        # 1. Selettore Maestri
        nomi = ["Scegli un Maestro..."] + list(ANTROPOLOGI.keys())
        selezione = st.selectbox("🏺 Quale voce vuoi evocare?", options=nomi, key="sel_maestro_antro")

        if selezione != "Scegli un Maestro...":
            dati = ANTROPOLOGI[selezione]
            st.markdown(f"""
                <div class="riquadro-antropologo">
                    <div class="nome-antropologo">{selezione}</div>
                    <div style="font-family: 'Cinzel'; font-size: 0.8rem; color: #8d6e63;">{dati['opera']} · {dati['anni']}</div>
                    <div class="testo-antropologo">"{dati['testo']}"</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("##### ✍️ Il tuo pensiero antropologico")
        
        # 2. Recupero opere e Selettore (Risolve Widget Lungo e Sincronizzazione)
        try:
            res = supabase.table("Opere").select("*").eq("autore", nome_poeta).eq("categoria", "Antropologia").execute()
            opere = res.data if res.data else []
        except:
            opere = []

        col_w1, col_w2 = st.columns([1, 1])
        with col_w1:
            opere_lista = ["✨ Nuova Opera"] + [o['titolo'] for o in opere]
            opera_scelta = st.selectbox("📖 Carica un manoscritto:", opere_lista, key="sel_opera_antro_sync")
            opera_corrente = next((o for o in opere if o['titolo'] == opera_scelta), None)

        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo  = opera_corrente['versi']  if opera_corrente else ""

        # 3. Input con Chiavi Dinamiche (Obbliga il reset al cambio opera)
        titolo = st.text_input("Titolo dell'Opera", value=v_titolo, key=f"t_{opera_scelta}")
        testo = st.text_area("Riflessioni e Studi", value=v_testo, height=350, key=f"v_{opera_scelta}")

        # 4. Bottoni Azione
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("💾 Custodisci", use_container_width=True, key="save_antro"):
                if titolo and testo:
                    dati_op = {"titolo": titolo, "versi": testo, "categoria": "Antropologia", "autore": nome_poeta, "pubblica": True}
                    if opera_corrente:
                        supabase.table("Opere").update(dati_op).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati_op).execute()
                    st.rerun()

        with b2:
            if titolo and testo:
                pdf_bytes = genera_pdf(titolo, nome_poeta, testo)
                st.download_button(
                    label="🖨️ Scarica PDF", 
                    data=pdf_bytes, 
                    file_name=f"{titolo}.pdf", 
                    mime="application/pdf",
                    use_container_width=True,
                    key="dl_antro"
                )
            else:
                st.button("🖨️ PDF", disabled=True, use_container_width=True, key="dl_antro_off")

        with b3:
            if opera_corrente:
                if st.button("🔥 Brucia", use_container_width=True, key="del_antro"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()

    with col_res:
        with st.expander("📖 Ispirazione (Wikipedia)", expanded=True):
            termine = st.text_input("Cerca termine", placeholder="es. Etnografia...", key="wiki_in")
            if st.button("🔍 Cerca", key="wiki_btn"):
                if termine:
                    estr, url_w = cerca_wikipedia(termine)
                    st.markdown(f"<div class='wiki-estratto'>{estr}</div>", unsafe_allow_html=True)
                    if url_w:
                        st.markdown(f"[Apri Wikipedia]({url_w})")

        with st.expander("🌍 Istituzioni", expanded=False):
            for s in SITI_ANTROPOLOGIA:
                st.markdown(f"• [{s['nome']}]({s['url']})")

if __name__ == "__main__":
    show()
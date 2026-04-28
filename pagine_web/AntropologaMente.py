import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import base64
import urllib.parse
import urllib.request
import json


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

    t_enc   = titolo.encode('latin-1', 'replace').decode('latin-1')
    a_enc   = f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1')
    txt_enc = testo.encode('latin-1', 'replace').decode('latin-1')

    pdf.cell(0, 20, t_enc, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, a_enc, ln=True, align='R')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, txt_enc)

    output = pdf.output(dest='S')
    if isinstance(output, (bytes, bytearray)):
        return bytes(output)
    return output.encode('latin-1')


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


def cerca_immagini_unsplash(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://unsplash.com/s/photos/{termine_enc}"


def cerca_immagini_pixabay(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://pixabay.com/it/images/search/{termine_enc}/"


def apply_style():
    img_base64 = get_base64_image("assets/Fronte_3d.png")
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark">' if img_base64 else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

        .bg-watermark {{
            position: fixed; top:50%; left:50%;
            transform: translate(-50%, -50%);
            width: 70vw; opacity:0.05; filter: grayscale(100%);
            z-index:-1; pointer-events:none;
        }}
        .titolo-antropologaMente {{
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #2c1a0e;
            font-size: 2.8rem;
            letter-spacing: 8px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        .sottotitolo-antropologaMente {{
            font-family: 'EB Garamond', serif;
            text-align: center;
            color: #6d4c2a;
            font-size: 1.1rem;
            font-style: italic;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }}
        .riquadro-antropologo {{
            background: rgba(255,248,235,0.7);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(180,120,50,0.3);
            padding: 30px 36px;
            border-radius: 4px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.07);
            text-align: center;
            margin-bottom: 20px;
            position: relative; z-index:1;
        }}
        .nome-antropologo {{
            font-family: 'Cinzel', serif;
            font-size: 1.9rem;
            color: #5d3a1a;
            margin-bottom: 4px;
        }}
        .opera-antropologo {{
            font-family: 'Cinzel', serif;
            font-size: 0.82rem;
            color: #8d6e63;
            margin-bottom: 18px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .testo-antropologo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.75rem;
            line-height: 1.65;
            font-style: italic;
            color: #2c1a0e;
        }}
        .wiki-estratto {{
            font-family: 'EB Garamond', serif;
            font-size: 1.05rem;
            color: #2a1200;
            line-height: 1.7;
            background: rgba(255,251,240,0.9);
            border-left: 3px solid #c9a227;
            padding: 10px 14px;
            border-radius: 3px;
            max-height: 280px;
            overflow-y: auto;
        }}
        .link-risorsa {{
            display: inline-block;
            margin: 5px 4px 4px 0;
            padding: 5px 12px;
            background: #1a1008;
            color: #c9a227 !important;
            border: 1px solid #c9a227;
            border-radius: 4px;
            font-family: 'Cinzel', serif;
            font-size: 0.78rem;
            text-decoration: none;
            letter-spacing: 0.08em;
        }}
        .link-risorsa:hover {{
            background: #c9a227;
            color: #1a1008 !important;
        }}
        .etichetta-sezione {{
            font-family: 'Cinzel', serif;
            font-size: 0.82rem;
            color: #5d4037;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-weight: 700;
        }}
        .pannello-risorse {{
            background: rgba(255,251,240,0.85);
            border: 1px solid #d2b48c;
            border-radius: 6px;
            padding: 14px;
            margin-bottom: 12px;
        }}
        .stTextArea textarea {{
            background-color: rgba(255,255,255,0.5) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
            line-height: 1.8 !important;
        }}
        .stTextInput input {{
            background: rgba(255,251,240,0.9) !important;
            border: 1.5px solid #bb9457 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1rem !important;
        }}
        </style>
        {img_html}
    """, unsafe_allow_html=True)


# =========================
# ANTROPOLOGI
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
    "Edward Tylor": {
        "opera": "Cultura Primitiva",
        "testo": "La cultura è quell'insieme complesso che include conoscenza, credenza, arte, morale, legge, costume e ogni altra capacità acquisita dall'uomo come membro della società.",
        "anni": "1832-1917"
    },
    "Ruth Benedict": {
        "opera": "Modelli di Cultura",
        "testo": "Il compito dell'antropologia è quello di rendere il mondo sicuro per le differenze umane.",
        "anni": "1887-1948"
    },
    "Clifford Geertz": {
        "opera": "Interpretazione di Culture",
        "testo": "L'uomo è un animale sospeso nelle reti di significato che lui stesso ha tessuto. La cultura è quella rete.",
        "anni": "1926-2006"
    },
    "Marcel Mauss": {
        "opera": "Saggio sul Dono",
        "testo": "Il dono non è mai gratuito. I presenti creano aspettative di reciprocità.",
        "anni": "1872-1950"
    },
    "Ernesto De Martino": {
        "opera": "Sud e Magia",
        "testo": "Il folklore non è un museo di curiosità arcaiche, ma una civiltà dello spirito che risponde a bisogni profondi dell'esistenza umana.",
        "anni": "1908-1965"
    },
    "Mary Douglas": {
        "opera": "Purezza e Pericolo",
        "testo": "Lo sporco è materia fuori posto. Dove c'è sporco c'è sistema.",
        "anni": "1921-2007"
    },
    "Victor Turner": {
        "opera": "Il Processo Rituale",
        "testo": "Nei riti di passaggio, l'uomo si spoglia della sua identità per rinascere trasformato.",
        "anni": "1920-1983"
    },
    "Vincenzo Esposito": {
        "opera": "Comunità e Identità",
        "testo": "L'identità di un popolo non si conserva nei libri, ma nelle mani di chi lavora, nella voce di chi canta, nel silenzio di chi ricorda.",
        "anni": "XX sec."
    },
}

SITI_ANTROPOLOGIA = [
    {"nome": "🌍 Wenner-Gren Foundation",          "url": "https://www.wennergren.org"},
    {"nome": "🏛️ American Anthropological Assoc.", "url": "https://www.americananthro.org"},
    {"nome": "📚 SIAM - Società Italiana Antropologia", "url": "https://www.antropologiaetnologia.it/"},
    {"nome": "🔬 Royal Anthropological Institute", "url": "https://www.therai.org.uk"},
    {"nome": "📖 AnthroSource (riviste)",           "url": "https://anthrosource.onlinelibrary.wiley.com"},
]


# =========================
# MAIN SHOW()
# =========================

def show():
    apply_style()

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" not in st.session_state:
        st.warning("⚠️ Identificati nella Home.")
        return

    nome_poeta = st.session_state.utente

    st.markdown("<div class='titolo-antropologaMente'>AntropologaMente</div>", unsafe_allow_html=True)
    st.markdown("<div class='sottotitolo-antropologaMente'>L'uomo che studia l'uomo</div>", unsafe_allow_html=True)
    st.markdown("---")

    col_main, col_res = st.columns([1.7, 1])

    with col_main:
        nomi = ["Scegli un Maestro..."] + list(ANTROPOLOGI.keys())
        selezione = st.selectbox("🏺 Quale voce vuoi evocare?", options=nomi)

        if selezione != "Scegli un Maestro...":
            dati = ANTROPOLOGI[selezione]
            st.markdown(f"""
                <div class="riquadro-antropologo">
                    <div class="nome-antropologo">{selezione}</div>
                    <div class="opera-antropologo">{dati['opera']} &nbsp;·&nbsp; {dati['anni']}</div>
                    <div class="testo-antropologo">"{dati['testo']}"</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='text-align:center; margin-top:40px; font-family: EB Garamond, serif;
                            font-size:1.3rem; color:#8d6e63; font-style:italic;'>
                    Scegli un maestro dell'antropologia per iniziare...<br><br>
                    <span style='font-size:2.5rem;'>🏺</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### ✍️ Il tuo pensiero")

        try:
            res = supabase.table("Opere").select("*").eq("autore", nome_poeta).eq("categoria", "Antropologia").execute()
            opere = res.data if res.data else []
        except Exception:
            opere = []

        opere_lista = ["✨ Nuova Opera"] + [o['titolo'] for o in opere]
        opera_scelta = st.selectbox("📖 Carica un'opera:", opere_lista, key="antro_opera_sel")
        opera_corrente = next((o for o in opere if o['titolo'] == opera_scelta), None)

        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo  = opera_corrente['versi']  if opera_corrente else ""
        v_bg     = opera_corrente.get('sfondo', "") if opera_corrente else ""

        # Sincronizza il session_state dello sfondo con il valore dell'opera caricata
        if st.session_state.get("_ultima_opera_caricata") != opera_scelta:
            st.session_state["_ultima_opera_caricata"] = opera_scelta
            st.session_state["antro_sfondo_url"] = v_bg

        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo, key="antro_titolo")
        with col_c:
            cat_list = ["Antropologia", "Saggio", "Riflessione", "Racconto", "Poesia"]
            categoria = st.selectbox("Categoria", cat_list, key="antro_cat")

        testo = st.text_area(
            "Versi e Pensieri",
            value=v_testo,
            height=300,
            placeholder="Lascia che l'umanità parli attraverso di te...",
            key="antro_testo",
            label_visibility="collapsed"
        )

        pubblica = st.toggle(
            "📢 Affiggi in Bacheca",
            value=opera_corrente.get('pubblica', False) if opera_corrente else False,
            key="antro_pubblica"
        )

        st.markdown("---")

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("💾 Custodisci", use_container_width=True, key="antro_save"):
                if titolo and testo:
                    dati_opera = {
                        "titolo": titolo,
                        "versi": testo,
                        "categoria": categoria,
                        "autore": nome_poeta,
                        "pubblica": pubblica,
                        "sfondo": st.session_state.get("antro_sfondo_url") or v_bg
                    }
                    if opera_corrente:
                        supabase.table("Opere").update(dati_opera).eq("id", opera_corrente['id']).execute()
                        st.success("✅ Opera aggiornata.")
                    else:
                        supabase.table("Opere").insert(dati_opera).execute()
                        st.success("✅ Opera custodita.")
                    st.rerun()
                else:
                    st.warning("✍️ Compila titolo e testo prima di custodire.")

        with b2:
            if titolo and testo:
                pdf_output = genera_pdf(titolo, nome_poeta, testo)
                st.download_button(
                    label="🖨️ Scarica PDF",
                    data=bytes(pdf_output),
                    file_name=f"{titolo}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="antro_pdf"
                )
            else:
                st.button("🖨️ Scarica PDF", disabled=True, use_container_width=True, key="antro_pdf_dis")

        with b3:
            if opera_corrente:
                if st.button("🔥 Brucia", use_container_width=True, key="antro_del"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.success("🔥 Opera eliminata.")
                    st.rerun()
            else:
                st.button("🔥 Brucia", disabled=True, use_container_width=True, key="antro_del_dis")

    with col_res:
        with st.expander("📖 Cerca su Wikipedia", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca un termine</div>", unsafe_allow_html=True)
            default_wiki = selezione if selezione != "Scegli un Maestro..." else ""
            termine_wiki = st.text_input(
                "Termine Wikipedia",
                value=default_wiki,
                placeholder="es. Malinowski, totem, rituale...",
                key="antro_wiki_cerca",
                label_visibility="collapsed"
            )
            if st.button("🔍 Cerca", key="antro_btn_wiki"):
                if termine_wiki.strip():
                    with st.spinner("Consultando Wikipedia..."):
                        estratto, wiki_url = cerca_wikipedia(termine_wiki.strip())
                    st.session_state["antro_wiki_risultato"] = estratto
                    st.session_state["antro_wiki_url"] = wiki_url
                else:
                    st.warning("Inserisci un termine.")

            if st.session_state.get("antro_wiki_risultato"):
                st.markdown(
                    f"<div class='wiki-estratto'>{st.session_state['antro_wiki_risultato']}</div>",
                    unsafe_allow_html=True
                )
                if st.session_state.get("antro_wiki_url"):
                    st.markdown(
                        f"<a class='link-risorsa' href='{st.session_state['antro_wiki_url']}' target='_blank'>🔗 Pagina completa</a>",
                        unsafe_allow_html=True
                    )
                if st.button("✖ Chiudi", key="antro_wiki_close"):
                    st.session_state["antro_wiki_risultato"] = ""
                    st.session_state["antro_wiki_url"] = ""
                    st.rerun()

        with st.expander("🌍 Risorse di Antropologia", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Siti e Istituzioni</div>", unsafe_allow_html=True)
            for sito in SITI_ANTROPOLOGIA:
                st.markdown(
                    f"<a class='link-risorsa' href='{sito['url']}' target='_blank'>{sito['nome']}</a>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='etichetta-sezione'>Antropologi su Wikipedia</div>", unsafe_allow_html=True)
            for nome in list(ANTROPOLOGI.keys())[:5]:
                wiki_url = f"https://it.wikipedia.org/wiki/{urllib.parse.quote(nome)}"
                st.markdown(
                    f"<a class='link-risorsa' href='{wiki_url}' target='_blank'>📜 {nome}</a>",
                    unsafe_allow_html=True
                )

        with st.expander("🖼️ Sfondo dell'Opera", expanded=False):
            st.markdown("<div class='etichetta-sezione'>Cerca ispirazione visiva</div>", unsafe_allow_html=True)
            termine_img = st.text_input(
                "Cerca immagini",
                placeholder="es. tribù, foresta, archeologia...",
                key="antro_img_cerca",
                label_visibility="collapsed"
            )
            if termine_img.strip():
                u_link = cerca_immagini_unsplash(termine_img.strip())
                p_link = cerca_immagini_pixabay(termine_img.strip())
                st.markdown(
                    f"<a class='link-risorsa' href='{u_link}' target='_blank'>🌅 Unsplash</a>"
                    f"<a class='link-risorsa' href='{p_link}' target='_blank'>🖼 Pixabay</a>",
                    unsafe_allow_html=True
                )
            st.markdown("<div class='etichetta-sezione' style='margin-top:12px'>Incolla URL immagine</div>", unsafe_allow_html=True)
            bg_url = st.text_input(
                "URL sfondo",
                value=v_bg,
                placeholder="https://...",
                key="antro_sfondo_url",
                label_visibility="collapsed"
            )
            if bg_url and bg_url.startswith("http"):
                estensioni_valide = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
                url_pulito = bg_url.split('?')[0].lower()
                if any(url_pulito.endswith(ext) for ext in estensioni_valide):
                    st.image(bg_url, caption="Anteprima sfondo", use_container_width=True)
                else:
                    st.warning(
                        "⚠️ Usa il link diretto all'immagine (deve finire con .jpg, .png ecc.).\n\n"
                        "Su **Pixabay/Unsplash**: clicca sull'immagine → tasto destro → *Copia indirizzo immagine*."
                    )

        with st.expander("📊 Conteggio Opera", expanded=False):
            if testo:
                parole    = len(testo.split())
                caratteri = len(testo)
                righe     = testo.count('\n') + 1
                st.markdown(f"""
                    <div class='pannello-risorse'>
                        <div class='etichetta-sezione'>Statistiche</div>
                        📝 <b>Parole:</b> {parole}<br>
                        🔤 <b>Caratteri:</b> {caratteri}<br>
                        📜 <b>Righe:</b> {righe}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Inizia a scrivere per vedere le statistiche.")


if __name__ == "__main__":
    show()
import streamlit as st
from fpdf import FPDF
import os
import base64
import urllib.parse
import urllib.request
import json
from utils import nav_bar, carica_css  # Fondamentale per la coerenza del menu

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
    # Encoding per gestire caratteri speciali latini
    t_enc   = titolo.encode('latin-1', 'replace').decode('latin-1')
    a_enc   = f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1')
    txt_enc = testo.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.cell(0, 20, t_enc, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, a_enc, align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, txt_enc)
    return bytes(pdf.output()) # Formato corretto per download_button

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

# --- NUOVE FUNZIONI PER IMMAGINI DINAMICHE ---
def cerca_immagini_unsplash(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://unsplash.com/s/photos/{termine_enc}"

def cerca_immagini_pixabay(termine):
    termine_enc = urllib.parse.quote(termine)
    return f"https://pixabay.com/it/images/search/{termine_enc}/"

# =========================
# DATABASE FILOSOFI
# =========================
FILOSOFI = {
    "Socrate": {
        "opera": "Apologia",
        "testo": "L'unica vera sapienza è sapere di non sapere. Una vita senza ricerca non è degna di essere vissuta.",
        "anni": "470-399 a.C."
    },
    "Platone": {
        "opera": "Simposio",
        "testo": "Al tocco dell'amore, ognuno diventa poeta.",
        "anni": "428-348 a.C."
    },
    "Aristotele": {
        "opera": "Poetica",
        "testo": "La poesia è più filosofica e più seria della storia: la poesia tende a rappresentare l'universale, la storia il particolare.",
        "anni": "384-322 a.C."
    },
    "Kant": {
        "opera": "Critica della ragion pura",
        "testo": "Il cielo stellato sopra di me, la legge morale dentro di me.",
        "anni": "1724-1804"
    },
    "Nietzsche": {
        "opera": "Così parlò Zarathustra",
        "testo": "Bisogna avere ancora un caos dentro di sé per partorire una stella danzante.",
        "anni": "1844-1900"
    },
    "Leopardi": {
        "opera": "Zibaldone",
        "testo": "Il più solido piacere di questa vita è il piacer vano delle illusioni.",
        "anni": "1798-1837"
    },
    "Dante": {
        "opera": "Divina Commedia",
        "testo": "Considerate la vostra semenza: fatti non foste a viver come bruti, ma per seguir virtute e canoscenza.",
        "anni": "1265-1321"
    },
}

# =========================
# MAIN SHOW()
# =========================
def show():
    carica_css()
    nav_bar()
    
    path_watermark = "assets/Fronte.png"
    img_b64 = get_base64_image(path_watermark)
    
    watermark_style = f"""
        <style>
        .bg-watermark {{
            position: fixed; top:50%; left:50%;
            transform: translate(-50%, -50%);
            width: 70vw; opacity:0.04; filter: grayscale(100%);
            z-index:-1; pointer-events:none;
        }}
        .titolo-filosofaMente {{
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #1a1a1a;
            font-size: 2.8rem;
            letter-spacing: 8px;
            margin-bottom: 20px;
            text-transform: uppercase;
        }}
        .marmo-focus {{
            background: rgba(255,255,255,0.65);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(180,140,80,0.2);
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 30px;
        }}
        .nome-autore {{
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            color: #5d4037;
        }}
        .testo-stimolo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.8rem;
            line-height: 1.6;
            font-style: italic;
            color: #1a1a1a;
            margin-top: 20px;
        }}
        .wiki-estratto {{
            font-family: 'EB Garamond', serif;
            background: rgba(255,251,240,0.9);
            border-left: 4px solid #c9a227;
            padding: 15px;
            border-radius: 4px;
            font-size: 1rem;
        }}
        </style>
    """
    
    if img_b64:
        st.markdown(watermark_style + f'<img src="data:image/png;base64,{img_b64}" class="bg-watermark">', unsafe_allow_html=True)
    else:
        st.markdown(watermark_style, unsafe_allow_html=True)

    st.markdown("<div class='titolo-filosofaMente'>FilosofaMente</div>", unsafe_allow_html=True)

    col_main, col_res = st.columns([1.7, 1], gap="large")

    with col_main:
        nomi = ["Scegli una Scintilla..."] + list(FILOSOFI.keys())
        selezione = st.selectbox("✨ Quale anima vuoi consultare?", options=nomi, key="sel_filosofo")

        if selezione != "Scegli una Scintilla...":
            dati = FILOSOFI[selezione]

            st.markdown(f"""
                <div class="marmo-focus">
                    <div class="nome-autore">{selezione}</div>
                    <div style="font-family: 'Cinzel', serif; font-size: 0.9rem; color: #8d6e63; letter-spacing: 2px;">
                        {dati['opera']} &nbsp;·&nbsp; {dati['anni']}
                    </div>
                    <div class="testo-stimolo">"{dati['testo']}"</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### ✍️ Le tue riflessioni")
            testo_key = f"filo_text_{selezione}"
            testo = st.text_area(
                "Riflessioni",
                value=st.session_state.get(testo_key, ""),
                height=300,
                placeholder="Lascia che il pensiero del maestro illumini la tua penna...",
                key=f"area_{selezione}",
                label_visibility="collapsed"
            )
            st.session_state[testo_key] = testo

            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("💾 Salva", use_container_width=True):
                    st.success("Riflessione custodita.")
            with c2:
                if st.button("🗑️ Svuota", use_container_width=True):
                    st.session_state[testo_key] = ""
                    st.rerun()
            with c3:
                if testo:
                    pdf_bytes = genera_pdf(f"Riflessione su {selezione}", st.session_state.get('utente', 'Autore'), testo)
                    st.download_button("🖨️ PDF", data=pdf_bytes, file_name=f"Riflessione_{selezione}.pdf", use_container_width=True, key="dl_pdf")
                else:
                    st.button("🖨️ PDF", disabled=True, use_container_width=True)
        else:
            st.markdown("<div style='text-align:center; margin-top:80px; font-family: EB Garamond, serif; font-size:1.4rem; color:#8d6e63; font-style:italic;'>🕯️ Accendi una scintilla scegliendo un maestro dal menu...</div>", unsafe_allow_html=True)

    with col_res:
        with st.expander("📖 Ispirazione (Wikipedia)", expanded=True):
            default_wiki = selezione if selezione != "Scegli una Scintilla..." else ""
            termine_wiki = st.text_input("Cerca termine", value=default_wiki, placeholder="es. Socrate, Estetica...", key="w_in")
            if st.button("🔍 Consulta", key="w_btn"):
                if termine_wiki:
                    estratto, url_w = cerca_wikipedia(termine_wiki)
                    st.markdown(f"<div class='wiki-estratto'>{estratto}</div>", unsafe_allow_html=True)
                    if url_w:
                        st.markdown(f"<a class='link-risorsa' href='{url_w}' target='_blank'>Vai a Wikipedia</a>", unsafe_allow_html=True)

        # --- SEZIONE AGGIORNATA: ATMOSFERA VISIVA DINAMICA ---
        with st.expander("🎨 Atmosfera Visiva", expanded=False):
            st.write("Trova ispirazione per la tua riflessione:")
            termine_img = st.text_input("Cerca immagini", value=default_wiki, placeholder="es. Grecia, Marmo...", key="img_in")
            
            if termine_img:
                u_url = cerca_immagini_unsplash(termine_img)
                p_url = cerca_immagini_pixabay(termine_img)
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-around; margin-top: 10px;">
                        <a href="{u_url}" target="_blank" style="text-decoration:none; color:#bb9457; font-weight:bold;">📸 UNSPLASH</a>
                        <a href="{p_url}" target="_blank" style="text-decoration:none; color:#bb9457; font-weight:bold;">🖼️ PIXABAY</a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            link_img = st.text_input("Incolla URL immagine per visualizzarla", placeholder="https://...", key="img_url_in")
            if link_img:
                st.image(link_img, use_container_width=True)

if __name__ == "__main__":
    show()
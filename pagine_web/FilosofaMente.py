import streamlit as st
from fpdf import FPDF
import os
import base64
import io

# =========================
# Funzioni ausiliarie
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
    # Gestione codifica per evitare errori con caratteri speciali
    t_enc = titolo.encode('latin-1', 'replace').decode('latin-1')
    a_enc = f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1')
    txt_enc = testo.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.cell(0, 20, t_enc, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, a_enc, ln=True, align='R')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, txt_enc)
    return pdf.output(dest='S').encode('latin-1')

# =========================
# Stile e sfondo
# =========================
def apply_sacred_style(bg_image=None):
    if bg_image is None:
        bg_image = "assets/Fronte_3d.png"

    img_base64 = get_base64_image(bg_image)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark">' if img_base64 else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital,wght@0,400;1,400&display=swap');
        .stApp {{ background-color: #fdf5e6; }}
        .bg-watermark {{
            position: fixed; top:50%; left:50%;
            transform: translate(-50%, -50%);
            width: 80vw; opacity:0.06; filter: grayscale(100%);
            z-index:-1; pointer-events:none;
        }}
        .titolo-filosofaMente {{
            font-family: 'Cinzel', serif; text-align:center; color:#1a1a1a; font-size:3.5rem;
            letter-spacing:8px; margin-top:20px; text-transform:uppercase;
        }}
        .marmo-focus {{
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(5px);
            border:1px solid rgba(0,0,0,0.1);
            padding:50px; border-radius:4px;
            box-shadow:0 20px 40px rgba(0,0,0,0.05);
            text-align:center; margin-top:30px;
            min-height:350px; display:flex; flex-direction:column; justify-content:center;
            position:relative; z-index:1;
        }}
        .nome-autore {{ font-family:'Cinzel', serif; font-size:2.2rem; color:#5d4037; margin-bottom:5px; }}
        .opera-unica {{ font-family:'Cinzel', serif; font-size:0.9rem; color:#8d6e63; margin-bottom:25px; text-transform:uppercase; letter-spacing:2px; }}
        .testo-stimolo {{ font-family:'EB Garamond', serif; font-size:2rem; line-height:1.6; font-style:italic; color:#1a1a1a; }}
        </style>
        {img_html}
    """, unsafe_allow_html=True)

# =========================
# Main show()
# =========================
def show():
    st.markdown("<div class='titolo-filosofaMente'>FilosofaMente</div>", unsafe_allow_html=True)

    # Configurazione Sfondo
    with st.expander("🎨 Personalizza Atmosfera"):
        uploaded_file = st.file_uploader("Carica un'immagine", type=['png','jpg','jpeg'])
        link_image = st.text_input("Oppure inserisci un link diretto")
    
    bg_image = None
    if uploaded_file:
        bg_image = "temp_bg.png"
        with open(bg_image, "wb") as f:
            f.write(uploaded_file.getbuffer())
    elif link_image:
        bg_image = link_image

    apply_sacred_style(bg_image)

    filosofi = {
        "Socrate": {"opera": "Apologia", "testo": "L'unica vera sapienza è sapere di non sapere. Una vita senza ricerca non è degna di essere vissuta."},
        "Marx": {"opera": "Il Capitale", "testo": "La filosofia non ha mai fatto altro che interpretare il mondo; si tratta di trasformarlo."},
        "Kant": {"opera": "Critica della ragion pura", "testo": "Il cielo stellato sopra di me, la legge morale dentro di me."},
        "Hegel": {"opera": "Fenomenologia dello Spirito", "testo": "Ciò che è razionale è reale, e ciò che è reale è razionale."},
        "Schopenhauer": {"opera": "Il mondo come volontà e rappresentazione", "testo": "La vita è un pendolo che oscilla tra dolore e noia."},
        "Nietzsche": {"opera": "Così parlò Zarathustra", "testo": "Bisogna avere ancora un caos dentro di sé per partorire una stella danzante."},
        "Platone": {"opera": "Simposio", "testo": "Al tocco dell'amore, ognuno diventa poeta."}
    }

    col_l, col_c, col_r = st.columns([0.1,1,0.1])
    with col_c:
        nomi = ["Scegli una Scintilla..."] + list(filosofi.keys())
        selezione = st.selectbox("Quale anima vuoi consultare?", options=nomi)

        if selezione != "Scegli una Scintilla...":
            dati = filosofi[selezione]
            st.markdown(f"""
                <div class="marmo-focus">
                    <div class="nome-autore">{selezione}</div>
                    <div class="opera-unica">{dati['opera']}</div>
                    <div class="testo-stimolo">"{dati['testo']}"</div>
                </div>
            """, unsafe_allow_html=True)

            st.subheader("Scrivi qui le tue riflessioni")
            testo_iniziale = st.session_state.get('filosofaMente_text', '')
            testo = st.text_area("", value=testo_iniziale, height=250, key="area_filo")
            st.session_state['filosofaMente_text'] = testo

            # --- SERRANDA OPERATIVA ---
            with st.expander("🛠️ GESTISCI LA TUA OPERA"):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("💾 SALVA", key="btn_save"):
                        st.success("Testo salvato!")
                with c2:
                    if st.button("📝 MODIFICA", key="btn_edit"):
                        st.info("Area pronta.")
                with c3:
                    if st.button("🗑️ ELIMINA", key="btn_del"):
                        st.session_state['filosofaMente_text'] = ""
                        st.rerun()
                with c4:
                    pdf_data = genera_pdf(f"Riflessione: {selezione}", st.session_state.get('utente', 'Autore'), testo)
                    st.download_button("🖨️ PDF", data=pdf_data, file_name="Riflessione.pdf", key="btn_pdf")
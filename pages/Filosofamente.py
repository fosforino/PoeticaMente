import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import base64
import json

# Funzioni ausiliarie
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def genera_pdf(titolo, autore, testo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='R')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, testo.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

def apply_sacred_style():
    path_icona_filo = "Icona_Filosofamente_Test.png"
    if not os.path.exists(path_icona_filo):
        path_icona_filo = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona_filo)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-filosofia">' if img_base64 else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital,wght@0,400;1,400&display=swap');
        .stApp {{
            background-color: #fdf5e6;
            background-image: 
                url("https://www.transparenttextures.com/patterns/marble-similar.png"),
                url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        }}
        .bg-watermark-filosofia {{
            position: fixed; top:50%; left:50%;
            transform: translate(-50%, -50%);
            width:45vw; opacity:0.06; filter: grayscale(100%);
            z-index:-1; pointer-events:none;
        }}
        .titolo-filosofamente {{
            font-family: 'Cinzel', serif; text-align:center; color:#1a1a1a; font-size:3.5rem; letter-spacing:8px; margin-top:20px; text-transform:uppercase;
        }}
        .marmo-focus {{
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(5px);
            border:1px solid rgba(0,0,0,0.1);
            padding:50px;
            border-radius:4px;
            box-shadow:0 20px 40px rgba(0,0,0,0.05);
            text-align:center; margin-top:30px; min-height:350px;
            display:flex; flex-direction:column; justify-content:center; position:relative; z-index:1;
        }}
        .nome-autore {{ font-family:'Cinzel', serif; font-size:2.2rem; color:#5d4037; margin-bottom:5px; }}
        .opera-unica {{ font-family:'Cinzel', serif; font-size:0.9rem; color:#8d6e63; margin-bottom:25px; text-transform:uppercase; letter-spacing:2px; }}
        .testo-stimolo {{ font-family:'EB Garamond', serif; font-size:2rem; line-height:1.6; font-style:italic; color:#1a1a1a; }}
        </style>
        {img_html}
    """, unsafe_allow_html=True)

def show():
    apply_sacred_style()
    st.markdown("<div class='titolo-filosofamente'>Filosofamente</div>", unsafe_allow_html=True)

    # Dizionario filosofico
    filosofi = {
        "Socrate": {"opera": "Apologia", "testo": "L'unica vera sapienza è sapere di non sapere. Una vita senza ricerca non è degna di essere vissuta."},
        "Marx": {"opera": "Il Capitale", "testo": "La filosofia non ha mai fatto altro che interpretare il mondo; si tratta di trasformarlo."},
        "Kant": {"opera": "Critica della ragion pura", "testo": "Il cielo stellato sopra di me, la legge morale dentro di me."},
        "Hegel": {"opera": "Fenomenologia dello Spirito", "testo": "Ciò che è razionale è reale, e ciò che è reale è razionale."},
        "Schopenhauer": {"opera": "Il mondo come volontà e rappresentazione", "testo": "La vita è un pendolo che oscilla tra dolore e noia."},
        "Nietzsche": {"opera": "Così parlò Zarathustra", "testo": "Bisogna avere ancora un caos dentro di sé per partorire una stella danzante."},
        "Platone": {"opera": "Simposio", "testo": "Al tocco dell'amore, ognuno diventa poeta."}}
    
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

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
            
            st.write("")
            if st.button("🖋️ Corri allo Scrittoio"):
                st.session_state.selezione_filo = dati['testo']
                st.switch_page("pages/Scrittoio.py")
            
            if st.button("💾 Salva questa citazione"):
                if "utente" in st.session_state:
                    try:
                        record = {
                            "titolo": f"Citazione: {selezione}",
                            "versi": dati['testo'],
                            "categoria": "Citazione",
                            "autore": st.session_state.utente,
                            "pubblica": False,
                            "immagine_url": "",
                            "stile_layout": {}
                        }
                        supabase.table("Opere").insert(record).execute()
                        st.success("Citazione salvata nello Scrittoio!")
                    except Exception as e:
                        st.error(f"Errore salvataggio: {e}")
            if st.button("🖨️ Scarica PDF"):
                pdf_data = genera_pdf(f"Citazione: {selezione}", st.session_state.utente if "utente" in st.session_state else "Anonimo", dati['testo'])
                st.download_button("Download PDF", data=pdf_data, file_name=f"Citazione_{selezione}.pdf", mime="application/pdf")
        else:
            st.markdown("<div style='text-align:center; margin-top:80px; opacity:0.4; font-family:\"EB Garamond\"; font-size:1.5rem;'>Il silenzio è l'inizio di ogni grande opera.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
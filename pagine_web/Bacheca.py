import streamlit as st
from supabase import create_client
import os
import base64
import urllib.parse
from fpdf import FPDF

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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

def apply_aesthetic_style():
    path_icona = "PoeticaMente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-bacheca">' if img_base64 else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

        .stApp {{
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
            color: #3e2723;
        }}

        .bg-watermark-bacheca {{
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 60vw; opacity: 0.05; filter: blur(10px);
            z-index: -1; pointer-events: none;
        }}

        .poesia-card {{
            background-color: rgba(255, 250, 240, 0.9);
            border-radius: 8px;
            border: 1px solid rgba(193, 154, 107, 0.4);
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            overflow: hidden;
        }}

        .anteprima-img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
        }}

        .card-content {{
            padding: 30px;
        }}

        .titolo-poesia {{
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
        }}

        .versi-testo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.35rem;
            line-height: 1.6;
            white-space: pre-wrap;
            margin: 25px 0;
        }}

        .firma-autore {{
            text-align: right;
            font-style: italic;
        }}

        .social-link {{
            text-decoration: none;
            font-size: 0.85rem;
            color: #795548;
            border: 1px solid #c19a6b;
            padding: 8px 14px;
            border-radius: 20px;
            margin-right: 10px;
            display: inline-block;
        }}

        /* 🔥 BOTTONI SISTEMATI */
        .stDownloadButton button,
        .stButton button {{
            width: 100%;
            min-width: 130px;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        /* Hover elegante */
        .stButton button:hover,
        .stDownloadButton button:hover {{
            background-color: #c19a6b;
            color: white;
            transition: 0.3s;
        }}

        </style>
        {img_html}
        """, unsafe_allow_html=True)

def show():
    apply_aesthetic_style()

    st.markdown("<h1 style='text-align: center; font-family: \"Playfair Display\", serif; font-size: 3rem; margin-bottom: 50px;'>🏛️ La Grande Bacheca</h1>", unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    try:
        res = supabase.table("Opere").select("*").filter("autore", "eq", f"{st.session_state.utente}").order("created_at", desc=True).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("La bacheca è ancora bianca. Inizia a scrivere nel tuo Scrittoio!")

        col_m_1, col_m_2, col_m_3 = st.columns([0.1, 1, 0.1])

        with col_m_2:
            for p in poemi:
                id_opera = p.get('id')
                titolo = p.get('titolo', 'Senza Titolo')
                testo = p.get('versi', '')
                autore = p.get('autore', 'Anonimo')
                categoria = p.get('categoria', 'Poesia')
                img_url = p.get('immagine_url', "")

                st.markdown('<div class="poesia-card">', unsafe_allow_html=True)

                if img_url and img_url != "PC":
                    st.markdown(f'<img src="{img_url}" class="anteprima-img">', unsafe_allow_html=True)
                elif img_url == "PC":
                    st.markdown('<div style="background: #e9e0d1; height: 10px;"></div>', unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="card-content">
                        <div style='color: #c19a6b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px;'>{categoria}</div>
                        <div class="titolo-poesia">{titolo}</div>
                        <div class="versi-testo">{testo}</div>
                        <div class="firma-autore">— {autore}</div>
                    </div>
                    """, unsafe_allow_html=True)

                testo_share = f"*{titolo}*\n\n{testo}\n\n— {autore}"
                testo_url = urllib.parse.quote(testo_share)

                # --- Riga bottoni: Social | PDF | Brucia | Segnala ---
                c_social, c_pdf, c_brucia, c_report = st.columns([2, 1.5, 1.5, 1.5])

                with c_social:
                    st.markdown(f"""
                        <div style="padding: 0 0 30px 30px;">
                            <a href="https://wa.me/?text={testo_url}" target="_blank" class="social-link">WhatsApp</a>
                            <a href="mailto:?body={testo_url}" class="social-link">Email</a>
                        </div>
                        """, unsafe_allow_html=True)

                with c_pdf:
                    pdf_data = genera_pdf_singola(p)
                    st.download_button(
                        label="📥 PDF",
                        data=pdf_data,
                        file_name=f"{titolo}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{id_opera}"
                    )

                with c_brucia:
                    with st.popover("🔥 Brucia"):
                        st.warning(f"Vuoi eliminare **{titolo}** per sempre?")
                        if st.button("Sì, elimina", key=f"del_{id_opera}", type="primary"):
                            try:
                                supabase.table("Opere").delete().eq("id", id_opera).execute()
                                st.success("Opera eliminata.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Errore eliminazione: {e}")

                with c_report:
                    with st.popover("🚩 Segnala"):
                        st.write("Segnala contenuto inappropriato")
                        motivo = st.selectbox("Motivo:", ["Inappropriato", "Plagio", "Spam"], key=f"mot_{id_opera}")
                        if st.button("Invia", key=f"btn_{id_opera}"):
                            report_data = {
                                "opera_id": id_opera,
                                "titolo_opera": titolo,
                                "segnalatore": st.session_state.get("utente", "Anonimo"),
                                "motivo": motivo
                            }
                            supabase.table("Segnalazioni").insert(report_data).execute()
                            st.success("Segnalato.")

                st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Errore bacheca: {e}")

if __name__ == "__main__":
    show()
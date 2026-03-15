import streamlit as st
from supabase import create_client
import os
import base64
import urllib.parse

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    path_icona = "Poeticamente.png"
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
            transition: transform 0.3s ease;
        }}
        .poesia-card:hover {{
            transform: translateY(-5px);
        }}
        .anteprima-img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-bottom: 1px solid rgba(193, 154, 107, 0.2);
        }}
        .card-content {{
            padding: 30px;
        }}
        .titolo-poesia {{
            font-family: 'Playfair Display', serif;
            color: #3e2723;
            font-size: 2.2rem;
            margin-bottom: 5px;
            line-height: 1.2;
        }}
        .versi-testo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.35rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #2c2c2c;
            margin: 25px 0;
        }}
        .firma-autore {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            text-align: right;
            color: #795548;
            border-top: 1px solid rgba(193, 154, 107, 0.2);
            padding-top: 15px;
            font-size: 1.1rem;
        }}
        .social-link {{
            text-decoration: none;
            font-size: 0.85rem;
            color: #795548;
            border: 1px solid #c19a6b;
            padding: 6px 12px;
            border-radius: 20px;
            margin-right: 10px;
            display: inline-block;
            transition: 0.3s;
        }}
        .social-link:hover {{
            background: #c19a6b;
            color: white;
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
        # Recuperiamo tutte le info incluse le immagini e lo stile
        res = supabase.table("Opere").select("*").eq("pubblica", True).order("created_at", desc=True).execute()
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
                
                # Gestione Immagine
                img_url = p.get('immagine_url', "")
                stile = p.get('stile_layout', {}) # Se abbiamo salvato stili particolari
                
                # Logica visualizzazione immagine
                # Se è un link esterno o una base64 salvata come "PC" (che però richiede gestione media se complessa)
                # Per ora mostriamo l'immagine se il link è valido
                
                st.markdown('<div class="poesia-card">', unsafe_allow_html=True)
                
                # Anteprima Immagine (se presente)
                if img_url and img_url != "PC":
                    st.markdown(f'<img src="{img_url}" class="anteprima-img">', unsafe_allow_html=True)
                elif img_url == "PC":
                    # Nota: Se è salvata in locale sul PC dell'utente, qui non la vedremo 
                    # a meno di non caricarla su un cloud storage. Per ora mettiamo un placeholder elegante.
                    st.markdown(f'<div style="background: #e9e0d1; height: 10px;"></div>', unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="card-content">
                        <div style='color: #c19a6b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px;'>{categoria}</div>
                        <div class="titolo-poesia">{titolo}</div>
                        <div class="versi-testo">{testo}</div>
                        <div class="firma-autore">— {autore}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Footer Interattivo
                testo_share = f"*{titolo}*\n\n{testo}\n\n— {autore}"
                testo_url = urllib.parse.quote(testo_share)
                
                c_social, c_report = st.columns([3, 1])
                
                with c_social:
                    st.markdown(f"""
                        <div style="padding: 0 0 30px 30px;">
                            <a href="https://wa.me/?text={testo_url}" target="_blank" class="social-link">WhatsApp</a>
                            <a href="mailto:?body={testo_url}" class="social-link">Email</a>
                        </div>
                        """, unsafe_allow_html=True)
                
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
import streamlit as st
import os
import base64
from utils import nav_bar, carica_css  # Importazione fondamentale per la navigazione

# =========================
# FUNZIONI AUSILIARIE
# =========================

def get_base64_image(image_path):
    """Legge l'immagine e la converte in base64 per l'integrazione HTML."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# =========================
# MAIN SHOW()
# =========================

def show():
    # 1. Carica stile globale e barra di navigazione superiore
    carica_css()
    nav_bar()
    # Stile CSS specifico per rendere il video e la pagina più "materici"
    st.markdown("""
        <style>
        .video-wrapper {
            border: 4px solid #c9a227; /* Oro bronzato */
            border-radius: 15px;
            box-shadow: 0 0 50px rgba(201, 162, 39, 0.3), inset 0 0 20px rgba(0,0,0,0.5);
            padding: 10px;
            background: #1a1008; /* Sfondo scuro per far risaltare il bronzo */
            margin: 20px auto;
            max-width: 800px;
        }
        .titolo-premio {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #1a1a1a;
            font-size: 2.8rem;
            letter-spacing: 6px;
            text-transform: uppercase;
            margin-bottom: 20px;
            margin-top: 10px;
        }
        .citazione-premio {
            font-family: 'EB Garamond', serif;
            text-align: center;
            color: #5d4037;
            font-style: italic;
            font-size: 1.8rem;
            margin-top: 25px;
            line-height: 1.4;
        }
        /* Rende il video responsive */
        video {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='titolo-premio'>Il Tuo Riconoscimento</div>", unsafe_allow_html=True)
    
    # Percorsi file
    video_path = "assets/Medaglia_v2.mp4"
    img_icon_path = "assets/Icona.png"
    
    # Verifica presenza video
    if os.path.exists(video_path):
        # Effetto celebrazione all'apertura
        st.balloons()
        
        # Contenitore video centrato
        _, col_video, _ = st.columns([0.1, 0.8, 0.1])
        with col_video:
            st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
            st.video(video_path)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("🏮 L'effigie del premio è in fase di forgiatura (file video non trovato).")
    
    # Spazio e Icona finale decorativa
    st.markdown("<br>", unsafe_allow_html=True)
    img_base64 = get_base64_image(img_icon_path)
    
    if img_base64:
        st.markdown(f"""
            <div style="text-align:center; margin-top: 20px;">
                <img src="data:image/png;base64,{img_base64}" style="width:70px; opacity:0.5; filter: sepia(100%);">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='citazione-premio'>L'Alchimia tra il Pensiero e il Verso.</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-family:Cinzel; font-size:0.8rem; color:#bb9457; margin-top:10px;'>POETICAMENTE · MMXXVI</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
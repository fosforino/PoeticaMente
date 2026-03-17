import streamlit as st
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente
import os
import base64

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(
    page_title="Poeticamente", 
    page_icon="🖋️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_global_style(image_path):
    img_base64 = get_base64_image(image_path)
    if img_base64:
        st.markdown(f"""
            <img src="data:image/png;base64,{img_base64}" class="bg-watermark">
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        .stApp { 
            background-color: #fdf5e6 !important;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
        }

        .bg-watermark {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 70vw; opacity: 0.07; filter: blur(8px);
            z-index: -1; pointer-events: none;
        }

        [data-testid="stSidebarNav"] { display: none; }

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            margin: auto;
        }

        /* Box di Login Elegante */
        .login-box {
            background: rgba(255, 255, 255, 0.4);
            padding: 40px;
            border-radius: 15px;
            border: 1px solid rgba(193, 154, 107, 0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            backdrop-filter: blur(5px);
            margin-top: 20px;
        }

        div.stButton > button { 
            background-color: #3e2723 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #c19a6b !important; 
            border-radius: 8px !important;
            width: 100%;
        }
        
        .poetic-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 5rem; text-align: center; 
            color: #3e2723; margin-top: -10px;
            letter-spacing: -2px;
        }
    </style>
    """, unsafe_allow_html=True)

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Percorso immagine aggiornato al nuovo marchio trasparente
path_icona_standard = "Poeticamente.png"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LOGICA DI ACCESSO ---
if not st.session_state.authenticated:
    st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
    apply_global_style(path_icona_standard)
    
    _, col_centrale, _ = st.columns([0.5, 1, 0.5])
    
    with col_centrale:
        # Icona centrata con ombra esterna
        if os.path.exists(path_icona_standard):
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src='data:image/png;base64,{get_base64_image(path_icona_standard)}' 
                         width='180' style='filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)); margin-bottom: 20px;'>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.2rem; color: #795548; margin-top: -20px;'>Dove il pensiero si fa inchiostro</p>", unsafe_allow_html=True)
        
        # Box Contenitore della Login
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: #3e2723; font-family: \"Playfair Display\";'>Identificazione del Poeta</h3>", unsafe_allow_html=True)
        
        nuovo_pseudo = st.text_input("Pseudonimo")
        password_segreta = st.text_input("Chiave d'Accesso", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        accetto_codice = st.checkbox("Giuro solennemente di rispettare il Codice d'Onore")
        captcha_input = st.text_input("Completa: 'Nel mezzo del cammin di nostra...'")

        if st.button("🔓 Entra nello Scrittoio"):
            if (nuovo_pseudo.strip() and password_segreta == "Ermetico_2026" and 
                accetto_codice and captcha_input.strip().lower() == "vita"):
                st.session_state.authenticated = True
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("Accesso negato. Riprova, Poeta.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- GESTIONE SIDEBAR E NAVIGAZIONE ---
page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca", "Archivio", "Filosofamente"])

apply_global_style(path_icona_standard)

with st.sidebar:
    if os.path.exists(path_icona_standard):
        st.image(path_icona_standard, width=150)
    
    st.markdown(f"<h2 style='text-align: center; color: #3e2723; font-family: \"Playfair Display\";'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Congeda il Profilo"):
        esegui_logout()

# --- NAVIGAZIONE ---
if page == "Home": Home.show()
elif page == "Scrittoio": Scrittoio.show()
elif page == "Bacheca": Bacheca.show()
elif page == "Archivio": Archivio.show()
elif page == "Filosofamente": Filosofamente.show()
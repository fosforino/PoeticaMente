import streamlit as st
from Pages import Home, Scrittoio, Bacheca
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

def apply_global_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        /* SFONDO PERGAMENA INCRESPATA */
        .stApp { 
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png"); /* Trama carta fatta a mano */
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
        }

        /* MENU A SCOMPARSA (Selectbox) - Diventa Marrone Antico */
        div[data-baseweb="select"] > div {
            background-color: #fdf5e6 !important;
            border: 1px solid #3e2723 !important;
            border-radius: 8px;
        }
        
        /* Colore del testo dentro il menu */
        div[data-baseweb="select"] span {
            color: #3e2723 !important;
            font-weight: 500;
        }

        /* Bottoni Uniformati */
        div.stButton > button { 
            background-color: #3e2723 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #c19a6b !important; 
            font-family: 'Playfair Display', serif !important; 
            border-radius: 8px !important;
            transition: 0.3s all ease;
        }
        
        div.stButton > button:hover {
            background-color: #5d4037 !important;
            transform: scale(1.02);
        }

        .poetic-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 3.5rem; 
            text-align: center; 
            color: #3e2723; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def apply_login_background(image_path):
    img_base64 = get_base64_image(image_path)
    if img_base64:
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(253, 245, 230, 0.85), rgba(253, 245, 230, 0.85)), 
                url("data:image/png;base64,{img_base64}");
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

apply_global_style()
path_icona = "Poeticamente.png" 

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    apply_login_background(path_icona)
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 0.8, 1])
    with col_logo_2:
        if os.path.exists(path_icona):
            st.image(path_icona)
    
    st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)
    
    col_mid_1, col_mid_2, col_mid_3 = st.columns([1, 1.5, 1])
    with col_mid_2:
        st.markdown("<h3 style='text-align: center;'>Identificazione del Poeta</h3>", unsafe_allow_html=True)
        nuovo_pseudo = st.text_input("Scegli il tuo Pseudonimo:")
        password_segreta = st.text_input("Chiave d'Accesso:", type="password")
        accetto_codice = st.checkbox("Giuro solennemente di rispettare il Codice d'Onore")
        captcha_input = st.text_input("Completa: 'Nel mezzo del cammin di nostra...'")

        if st.button("Entra nello Scrittoio"):
            if (nuovo_pseudo.strip() and password_segreta == "Ermetico_2026" and 
                accetto_codice and captcha_input.strip().lower() == "vita"):
                st.session_state.authenticated = True
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("Accesso negato.")
    st.stop()

# --- SIDEBAR E NAVIGAZIONE ---
with st.sidebar:
    if os.path.exists(path_icona):
        st.image(path_icona, width=150)
    st.markdown(f"<h2 style='text-align: center;'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    page = st.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca"])
    if st.button("Congeda il Profilo"):
        esegui_logout()

if page == "Home": Home.show()
elif page == "Scrittoio": Scrittoio.show()
elif page == "Bacheca": Bacheca.show()
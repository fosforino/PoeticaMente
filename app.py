import streamlit as st
import os
import pandas as pd
from fpdf import FPDF
from supabase import create_client, Client
from pydantic import BaseModel
# --- AGGIUNTO PREMIO NEGLI IMPORT ---
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente, Premio

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(
    page_title="Poeticamente", 
    page_icon="🖋️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Link al logo su GitHub
LOGO_URL = "https://raw.githubusercontent.com/fosforino/Poeticamente/main/Poeticamente.png"

def apply_global_style():
    """Carica lo stile dal file esterno e lo inietta nell'app"""
    css_path = "style.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning("File style.css non trovato. Assicurati che sia nella stessa cartella.")

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- INIZIALIZZAZIONE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- APPLICAZIONE STILE GLOBALE ---
apply_global_style()

# --- GESTIONE LOGIN ---
if not st.session_state.authenticated:
    # Nasconde la sidebar in fase di login
    st.markdown('<style>[data-testid="stSidebar"] {display: none;}</style>', unsafe_allow_html=True)
    
    # Spostiamo tutto a sinistra: colonna sx stretta per il testo, dx larga per il logo
    col_sinistra, col_vuota_destra = st.columns([1, 1.8])
    
    with col_sinistra:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #3e2723; font-family: \"Playfair Display\";'>Poeticamente</h1>", unsafe_allow_html=True)
        st.markdown('<h2 class="titolo-id">ID</h2>', unsafe_allow_html=True)
        
        # Inserimento dati SENZA st.form per reattività immediata
        nuovo_pseudo = st.text_input("Identità", placeholder="Chi bussa?", key="live_user")
        password_segreta = st.text_input("Chiave d'Accesso", type="password", placeholder="••••••••", key="live_pass")
        accetto_codice = st.checkbox("Accetto il Codice d'Onore", key="live_check")
        
        # Il captcha può apparire o reagire istantaneamente qui
        captcha_input = st.text_input("Dante: 'Nel mezzo del cammin di nostra...'", placeholder="Completa la riga", key="live_captcha")

        # Bottone d'ingresso classico (senza submit_button del form)
        # ... fine del codice di login (dentro l'if not st.session_state.authenticated) ...
        if st.button("🔓 Entra nello Scrittoio"):
            if (nuovo_pseudo.strip() and password_segreta == "Ermetico_2026" and 
                accetto_codice and captcha_input.strip().lower() == "vita"):
                st.session_state.authenticated = True
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("Accesso negato.")
    
    st.stop() # <--- IL MURO: Se non è loggato, il codice si ferma qui.

# --- APP DOPO IL LOGIN (Questo viene letto solo se sei loggato) ---
page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca", "Archivio", "Filosofamente", "Premio"])

with st.sidebar:
    # Qui usiamo il nuovo file nitido che hai caricato
    st.image("Icona.png", width=120) 
    st.markdown(f"<h2 style='text-align: center; color: #3e2723; font-family: \"Playfair Display\";'>Profilo:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Congeda il Profilo"):
        esegui_logout()

# --- NAVIGAZIONE ---
if page == "Home": Home.show()
elif page == "Scrittoio": Scrittoio.show()
elif page == "Bacheca": Bacheca.show()
elif page == "Archivio": Archivio.show()
elif page == "Filosofamente": Filosofamente.show()
elif page == "Premio": Premio.show()
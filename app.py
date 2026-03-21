import streamlit as st
import os
import pandas as pd
from fpdf import FPDF
from supabase import create_client, Client
from pydantic import BaseModel
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(
    page_title="Poeticamente", 
    page_icon="🖋️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Link al logo su GitHub (Punta al file che hai rinominato)
LOGO_URL = "https://raw.githubusercontent.com/fosforino/Poeticamente/main/Poeticamente.png"

def apply_global_style():
    """Carica lo stile dal file esterno e lo inietta nell'app"""
    css_path = "style.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        # Iniezione del CSS pulita senza stringhe HTML orfane
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
# Chiamata fuori dagli IF per coprire sia Login che App
apply_global_style()

# --- GESTIONE LOGIN ---
if not st.session_state.authenticated:
    # Nasconde la sidebar in fase di login
    st.markdown('<style>[data-testid="stSidebar"] {display: none;}</style>', unsafe_allow_html=True)
    
    _, col_centrale, _ = st.columns([0.5, 1, 0.5])
    with col_centrale:
        st.markdown("<h1 style='text-align: center; color: #3e2723; font-family: \"Playfair Display\";'>Poeticamente</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.2rem; color: #795548; margin-top: -20px;'>Dove il pensiero si fa inchiostro</p>", unsafe_allow_html=True)
        
        st.markdown("### Identificazione del Poeta")
        nuovo_pseudo = st.text_input("Pseudonimo")
        password_segreta = st.text_input("Chiave d'Accesso", type="password")
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
    st.stop()

# --- APP DOPO IL LOGIN ---
page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca", "Archivio", "Filosofamente"])

with st.sidebar:
    st.image(LOGO_URL, width=120)
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
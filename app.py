import streamlit as st
import os
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente, Premio

# 1. Configurazione Pagina (Layout Wide e Titolo)
st.set_page_config(page_title="Poeticamente", layout="wide", initial_sidebar_state="collapsed")

# 2. Blindaggio Estetico: Uccidiamo i menu di sistema e i testi fantasma
st.markdown("""
    <style>
        /* Nasconde il menu in alto a destra (Deploy, Rerun, etc.) */
        #MainMenu, header, footer {visibility: hidden; display: none !important;}
        
        /* Nasconde il selettore di contrasto e scritte tecniche residue */
        .stAppDeployButton, .stAppToolbar, [data-testid="stStatusWidget"] {display: none !important;}
        
        /* Forza il colore nero per i testi per contrastare col medaglione */
        .stMarkdown, p, label, h1, h2, h3 {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        /* Pulizia dei box di input per il login */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Caricamento del tuo style.css (quello che abbiamo pulito prima)
def load_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

load_css()

# --- LOGICA DI ACCESSO ---
if not st.session_state.authenticated:
    # Nasconde la sidebar se non sei loggato
    st.markdown('<style>[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)
    
    _, col, _ = st.columns([0.5, 1, 0.5])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True) # Spazio per non coprire il centro del medaglione
        st.title("Poeticamente")
        u = st.text_input("Identità", placeholder="Inserisci il tuo nome...")
        p = st.text_input("Chiave", type="password", placeholder="La tua parola ermetica...")
        
        if st.button("Entra"):
            if p == "Ermetico_2026":
                st.session_state.authenticated = True
                st.session_state.utente = u
                st.rerun()
            else:
                st.error("Chiave errata.")
    st.stop()

# --- INTERFACCIA POST-LOGIN ---
with st.sidebar:
    st.title(f"✒️ {st.session_state.utente}")
    st.markdown("---")
    page = st.radio("Naviga tra le stanze:", ["Home", "Scrittoio", "Bacheca", "Archivio", "Filosofamente", "Premio"])
    st.markdown("---")
    if st.button("Chiudi Portale"):
        st.session_state.authenticated = False
        st.rerun()

# Mapping delle pagine
pagine = {
    "Home": Home.show, 
    "Scrittoio": Scrittoio.show, 
    "Bacheca": Bacheca.show, 
    "Archivio": Archivio.show, 
    "Filosofamente": Filosofamente.show, 
    "Premio": Premio.show
}

# Esecuzione della pagina selezionata
pagine[page]()
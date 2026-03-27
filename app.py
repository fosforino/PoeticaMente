import streamlit as st
import os
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente, Premio

st.set_page_config(page_title="Poeticamente", layout="wide")

# Funzione per forzare il caricamento del CSS
def load_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

load_css()

if not st.session_state.authenticated:
    st.markdown('<style>[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)
    _, col, _ = st.columns([0.5, 1, 0.5])
    with col:
        st.title("Poeticamente")
        u = st.text_input("Identità")
        p = st.text_input("Chiave", type="password")
        if st.button("Entra"):
            if p == "Ermetico_2026":
                st.session_state.authenticated = True
                st.session_state.utente = u
                st.rerun()
    st.stop()

with st.sidebar:
    st.title(f"Poeta: {st.session_state.utente}")
    page = st.radio("Naviga:", ["Home", "Scrittoio", "Bacheca", "Archivio", "Filosofamente", "Premio"])
    if st.button("Esci"):
        st.session_state.authenticated = False
        st.rerun()

# Mapping diretto
pagine = {"Home": Home.show, "Scrittoio": Scrittoio.show, "Bacheca": Bacheca.show, "Archivio": Archivio.show, "Filosofamente": Filosofamente.show, "Premio": Premio.show}
pagine[page]()
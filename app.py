import streamlit as st
import os
from supabase import create_client
import importlib

# =========================
# CONFIGURAZIONE PAGINA
# =========================
st.set_page_config(
    page_title="Poeticamente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# IMPORT PAGINE
# =========================
try:
    from pages import Home, Scrittoio, Bacheca, Filosofamente, Archivio, Premio
except ImportError as e:
    st.error(f"Errore di importazione: {e}")

# =========================
# CONNESSIONE SUPABASE
# =========================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# =========================
# SESSIONE
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "utente" not in st.session_state:
    st.session_state.utente = ""

# =========================
# LOGIN / SOGLIA
# =========================
if not st.session_state.authenticated:

    # Carica CSS esterno se presente
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Schermata poetica iniziale
    st.markdown("""
        <div class="medaglione-container">
            <img src="https://raw.githubusercontent.com/fosforino/Poeticamente/main/assets/Fronte_3d.png" 
                 class="medaglione-immagine">
        </div>
        <h1 class="titolo-soglia">SOGLIA</h1>
        <div class="sottotitolo-opera">PENSIERO ED OPERA</div>
        <div class="citazione-solenne">
            "La vera vita è molto breve.<br>
            L'esistere è un'altra cosa."
        </div>
    """, unsafe_allow_html=True)

    # Input utente
    u = st.text_input("L'Identità", placeholder="Chi bussa?", key="input_u")
    p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="input_p")

    if st.button("VARCA IL PORTALE", use_container_width=True):
        if u and p:
            try:
                user_val = str(u).strip()
                pass_val = str(p).strip()
                # Controllo credenziali
                res = supabase.table("Opere").select("autore") \
                    .eq("autore", user_val) \
                    .eq("codice_firma", pass_val) \
                    .execute()

                if res.data and len(res.data) > 0:
                    st.session_state.authenticated = True
                    st.session_state.utente = user_val
                    st.rerun()
                else:
                    st.error("Il silenzio non risponde. Chiavi errate.")
            except Exception as e:
                st.error(f"Errore tecnico di connessione: {e}")
        else:
            st.warning("La Soglia richiede che ogni campo sia colmato.")

# =========================
# APP AUTENTICATA
# =========================
else:
    # Mostra il benvenuto solo una volta
    if "welcome_shown" not in st.session_state:
        st.toast(f"Benvenuto, {st.session_state.utente}", icon="✨")
        st.session_state.welcome_shown = True

    # Menu laterale
    menu = st.sidebar.selectbox(
        "📂 Navigazione",
        ["Home", "Scrittoio", "Bacheca", "Filosofamente", "Archivio", "Premio"]
    )

    # =========================
    # RICARICA PAGINA DINAMICAMENTE
    # =========================
    if menu == "Home":
        importlib.reload(Home)
        Home.show()
    elif menu == "Scrittoio":
        importlib.reload(Scrittoio)
        Scrittoio.show()
    elif menu == "Bacheca":
        importlib.reload(Bacheca)
        Bacheca.show()
    elif menu == "Filosofamente":
        importlib.reload(Filosofamente)
        Filosofamente.show()
    elif menu == "Archivio":
        importlib.reload(Archivio)
        Archivio.show()
    elif menu == "Premio":
        importlib.reload(Premio)
        Premio.show()
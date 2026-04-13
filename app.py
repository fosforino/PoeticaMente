import streamlit as st
import os
import base64
from supabase import create_client
import importlib

# =========================
# CONFIGURAZIONE PAGINA
# =========================
st.set_page_config(
    page_title="PoeticaMente",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# IMPORT PAGINE
# =========================
try:
    from pages import Home, Scrittoio, Bacheca, FilosofaMente, Archivio, Premio
except ImportError as e:
    st.error(f"Errore di importazione pagine: {e}")
    st.stop()

# =========================
# CONNESSIONE SUPABASE
# =========================
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Errore di connessione al database: {e}")
    st.stop()

# =========================
# INIZIALIZZAZIONE SESSIONE
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "utente" not in st.session_state:
    st.session_state.utente = ""
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# =========================
# FUNZIONE: carica immagine locale
# =========================
def carica_medaglione():
    path = "assets/Fronte.png"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# =========================
# SCHERMATA LOGIN / SOGLIA
# =========================
if not st.session_state.authenticated:

    # Carica CSS esterno
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # CSS della Soglia
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

        .stApp {
            background-color: #fdf5e6 !important;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
        }

        /* Medaglione fisso a destra */
        .medaglione-wrapper {
            position: fixed;
            top: 0; right: 0;
            width: 52%;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;
            z-index: 0;
        }

        /* Cerchio che ritaglia l'immagine */
        .medaglione-cerchio {
            position: relative;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            overflow: hidden;
            box-shadow:
                0 0 60px 30px rgba(212, 175, 55, 0.40),
                0 0 120px 60px rgba(184, 142, 35, 0.20),
                0 0 0 3px rgba(212, 175, 55, 0.30),
                0 0 0 10px rgba(212, 175, 55, 0.10);
            background: radial-gradient(
                circle at center,
                rgba(255, 240, 180, 0.60) 0%,
                rgba(230, 190, 80, 0.30) 40%,
                transparent 70%
            );
        }

        .medaglione-cerchio img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }

        /* Anello dorato esterno */
        .medaglione-anello {
            position: absolute;
            top: -8px; left: -8px;
            right: -8px; bottom: -8px;
            border-radius: 50%;
            border: 2px solid rgba(212, 175, 55, 0.30);
            box-shadow: 0 0 0 8px rgba(212, 175, 55, 0.08);
            pointer-events: none;
        }

        /* Testi poetici */
        .titolo-soglia {
            font-family: 'EB Garamond', serif !important;
            font-size: 4rem !important;
            font-weight: 700 !important;
            color: #1a1008 !important;
            letter-spacing: 0.3em !important;
            margin-bottom: 0 !important;
            position: relative; z-index: 10;
        }
        .sottotitolo-opera {
            font-family: 'EB Garamond', serif !important;
            font-style: italic !important;
            font-size: 1.1rem !important;
            color: #8b6508 !important;
            letter-spacing: 0.2em !important;
            margin-bottom: 1.5rem !important;
            position: relative; z-index: 10;
        }
        .citazione-solenne {
            font-family: 'EB Garamond', serif !important;
            font-style: italic !important;
            font-size: 1.15rem !important;
            color: #3e2723 !important;
            border-left: 3px solid #c9a227 !important;
            padding-left: 1rem !important;
            margin-bottom: 2rem !important;
            line-height: 1.8 !important;
            position: relative; z-index: 10;
        }

        /* Bottone portale */
        div.stButton > button {
            background: #1a1008 !important;
            color: #c9a227 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            letter-spacing: 0.25em !important;
            border: 1px solid #c9a227 !important;
            border-radius: 4px !important;
            padding: 0.7em 2em !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background: #c9a227 !important;
            color: #1a1008 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Carica e mostra il medaglione da file locale
    medaglione = carica_medaglione()
    if medaglione:
        st.markdown(f"""
            <div class="medaglione-wrapper">
                <div style="position: relative;">
                    <div class="medaglione-cerchio">
                        <img src="data:image/png;base64,{medaglione}">
                    </div>
                    <div class="medaglione-anello"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Testi poetici
    st.markdown("""
        <h1 class="titolo-soglia">SOGLIA</h1>
        <div class="sottotitolo-opera">PENSIERO ED OPERA</div>
        <div class="citazione-solenne">
            "La vera vita è molto breve.<br>
            L'esistere è un'altra cosa."
        </div>
    """, unsafe_allow_html=True)

    # Campi login
    u = st.text_input("L'Identità", placeholder="Chi bussa?", key="input_u")
    p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="input_p")

    if st.button("VARCA IL PORTALE", use_container_width=True):
        if u and p:
            try:
                user_val = str(u).strip()
                pass_val = str(p).strip()
                res = supabase.table("Opere").select("autore") \
                    .eq("autore", user_val) \
                    .eq("codice_firma", pass_val) \
                    .execute()
                if res.data and len(res.data) > 0:
                    st.session_state.authenticated = True
                    st.session_state.utente = user_val
                    st.session_state.welcome_shown = False
                    st.rerun()
                else:
                    st.error("🔒 Il silenzio non risponde. Chiavi errate.")
            except Exception as e:
                st.error(f"Errore tecnico di connessione: {e}")
        else:
            st.warning("✍️ La Soglia richiede che ogni campo sia colmato.")

# =========================
# APP AUTENTICATA
# =========================
else:

    # Benvenuto (solo una volta)
    if not st.session_state.welcome_shown:
        st.toast(f"Benvenuto, {st.session_state.utente} ✨")
        st.session_state.welcome_shown = True

    # Menu laterale
    with st.sidebar:
        st.markdown(
            f"<div style='font-family: EB Garamond, serif; font-size:1.1rem; color:#3e2723; "
            f"font-weight:bold; padding: 0.5rem 0 1rem 0;'>✒️ {st.session_state.utente}</div>",
            unsafe_allow_html=True
        )
        menu = st.selectbox(
            "📂 Navigazione",
            ["Home", "Scrittoio", "Bacheca", "FilosofaMente", "Archivio", "Premio"],
            index=["Home", "Scrittoio", "Bacheca", "FilosofaMente", "Archivio", "Premio"].index(
                st.session_state.pagina
            )
        )
        st.session_state.pagina = menu
        st.markdown("---")
        if st.button("🚪 Esci", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Routing pagine
    if menu == "Home":
        importlib.reload(Home)
        Home.show()
    elif menu == "Scrittoio":
        importlib.reload(Scrittoio)
        Scrittoio.show()
    elif menu == "Bacheca":
        importlib.reload(Bacheca)
        Bacheca.show()
    elif menu == "FilosofaMente":
        importlib.reload(FilosofaMente)
        FilosofaMente.show()
    elif menu == "Archivio":
        importlib.reload(Archivio)
        Archivio.show()
    elif menu == "Premio":
        importlib.reload(Premio)
        Premio.show()
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
    initial_sidebar_state="expanded"
)

# =========================
# IMPORT PAGINE
# =========================
from pagine_web import Home, Scrittoio, Bacheca, FilosofaMente, Archivio, Premio

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
# FUNZIONE: carica CSS globale
# =========================
def carica_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

    # Carica CSS globale
    carica_css()

    # Nasconde Sidebar e Header SOLO nella schermata login
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            header { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    # Medaglione centrato
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

    # --- CAMPI LOGIN ---
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        u = st.text_input("L'Identità", placeholder="Chi bussa?", key="input_u")
        p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="input_p")

        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

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
    # Carica CSS globale
    carica_css()

    # Forza sidebar visibile dopo il login
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: block !important; }
            section[data-testid="stSidebar"] { display: block !important; }
            [data-testid="stSidebarNav"] { display: block !important; }
        </style>
    """, unsafe_allow_html=True)

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
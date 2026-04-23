import streamlit as st
import os
import base64
from supabase import create_client
import importlib

st.set_page_config(
    page_title="PoeticaMente",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from pagine_web import Home, Scrittoio, Bacheca, FilosofaMente, Archivio, Premio

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Errore di connessione al database: {e}")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "utente" not in st.session_state:
    st.session_state.utente = ""
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"
if "opera_selezionata" not in st.session_state:
    st.session_state.opera_selezionata = "✨ Nuova Opera"
if "opere_lista" not in st.session_state:
    st.session_state.opere_lista = ["✨ Nuova Opera"]

def carica_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carica_medaglione():
    path = "assets/Fronte.png"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ─────────────────────────────────────────
# PAGINA DI LOGIN
# ─────────────────────────────────────────
if not st.session_state.authenticated:

    carica_css()

    medaglione = carica_medaglione()
    img_src = f"data:image/png;base64,{medaglione}" if medaglione else ""

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&display=swap');

        [data-testid="stSidebar"] {{ display: none !important; }}
        header {{ display: none !important; }}
        [data-testid="stHeader"] {{ display: none !important; }}
        footer {{ display: none !important; }}

        * {{
            box-sizing: border-box !important;
        }}

        html, body {{
            margin: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: #c8a96e !important;
        }}

        #root,
        .stApp > div,
        [data-testid="stAppViewContainer"] > div,
        [data-testid="stAppViewContainer"] > section,
        body > div:first-child {{
            background-color: transparent !important;
        }}

        .stApp {{
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            min-height: 100vh !important;
            overflow: hidden !important;
            background-color: #c8a96e !important;
        }}

        .block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main > div,
        .main .block-container {{
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
            width: 100vw !important;
            min-height: 100vh !important;
            background-color: transparent !important;
        }}

        .medaglione-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            object-position: center;
            opacity: 1;
            z-index: 0;
            pointer-events: none;
        }}

        .soglia-testi {{
            position: fixed;
            top: 6vh;
            left: 8vw;
            z-index: 2;
            pointer-events: none;
            max-width: 28vw;
        }}

        .soglia-titolo {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: #2a1200;
            letter-spacing: 0.2em;
            margin: 0 0 0.2rem 0;
            text-shadow: 2px 2px 8px rgba(255,220,120,0.8);
        }}

        .soglia-sottotitolo {{
            font-family: 'Cinzel', serif;
            font-size: 0.85rem;
            color: #3d1f00;
            letter-spacing: 0.3em;
            font-style: italic;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 4px rgba(255,220,120,0.8);
        }}

        .soglia-citazione {{
            font-family: 'EB Garamond', serif;
            font-size: 1.1rem;
            color: #2a1200;
            font-style: italic;
            border-left: 3px solid #c9a227;
            padding-left: 0.8rem;
            line-height: 1.7;
            text-shadow: 1px 1px 4px rgba(255,220,120,0.6);
        }}

        [data-testid="stVerticalBlock"] {{
            position: relative;
            z-index: 10;
        }}

        div[data-testid="column"]:nth-of-type(1) {{
            padding-left: 8vw !important;
        }}

        div[data-testid="column"]:nth-of-type(1) input {{
            width: 200px !important;
            max-width: 200px !important;
            transition: width 0.3s ease !important;
        }}
        div[data-testid="column"]:nth-of-type(1) input:focus {{
            width: 280px !important;
            max-width: 280px !important;
        }}

        div.stButton > button {{
            background: #1a1008 !important;
            color: #c9a227 !important;
            border: 1px solid #c9a227 !important;
            font-family: 'Cinzel', serif !important;
            font-weight: bold !important;
            letter-spacing: 0.1em !important;
            width: 200px !important;
            transition: all 0.3s ease !important;
        }}
        div.stButton > button:hover {{
            background: #c9a227 !important;
            color: #1a1008 !important;
            width: 280px !important;
        }}
        </style>

        <img class="medaglione-bg" src="{img_src}">

        <div class="soglia-testi">
            <div class="soglia-titolo">SOGLIA</div>
            <div class="soglia-sottotitolo">PENSIERO ED OPERA</div>
            <div class="soglia-citazione">
                "La vera vita è molto breve.<br>
                L'esistere è un'altra cosa."
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 62vh'></div>", unsafe_allow_html=True)

    col_login, col_vuota = st.columns([0.25, 0.75])
    with col_login:
        u = st.text_input("L'Identità", placeholder="Chi bussa?", key="input_u")
        p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="input_p")
        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)
        if st.button("VARCA IL PORTALE", use_container_width=False):
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

# ─────────────────────────────────────────
# APP PRINCIPALE (dopo login)
# ─────────────────────────────────────────
else:
    carica_css()

    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: flex !important;
                visibility: visible !important;
                opacity: 1 !important;
            }
            section[data-testid="stSidebar"] {
                display: flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                min-width: 240px !important;
            }
            [data-testid="stMain"] {
                background-color: #fdf5e6 !important;
                background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
            }
            .block-container {
                padding: 2rem 3rem !important;
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.welcome_shown:
        st.toast(f"Benvenuto, {st.session_state.utente} ✨")
        st.session_state.welcome_shown = True

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

        if menu == "Scrittoio":
            st.markdown("---")
            opere_lista = st.session_state.get("opere_lista", ["✨ Nuova Opera"])
            opera_scelta = st.selectbox("📖 Carica un'opera:", opere_lista)
            st.session_state.opera_selezionata = opera_scelta

        st.markdown("---")
        if st.button("🚪 Esci", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

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
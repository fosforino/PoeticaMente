import streamlit as st
import os
import base64
from supabase import create_client
import importlib
from pagine_web import Home, Scrittoio, Bacheca, FilosofaMente, AntropologaMente, Archivio, Premio

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="PoeticaMente",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONNESSIONE DATABASE ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Errore di connessione al database: {e}")
    st.stop()

# --- INIZIALIZZAZIONE SESSION STATE ---
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

# --- FUNZIONI DI SUPPORTO ---
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

            * {{ box-sizing: border-box !important; }}

            html, body {{
                margin: 0 !important;
                padding: 0 !important;
                overflow-x: hidden !important;
                width: 100vw !important;
                height: 100vh !important;
                background-color: #f5c37a !important;
            }}

            .stApp {{
                margin: 0 !important;
                padding: 0 !important;
                width: 100vw !important;
                min-height: 100vh !important;
                background-color: #f5c37a !important;
            }}

            .block-container {{
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100vw !important;
            }}

            .medaglione-bg {{
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                object-fit: cover;
                z-index: 0;
                pointer-events: none;
            }}

            .soglia-testi {{
                position: fixed;
                top: 6vh; left: 8vw;
                z-index: 2;
                max-width: 28vw;
            }}

            .soglia-titolo {{
                font-family: 'Cinzel', serif;
                font-size: 3.5rem;
                font-weight: 700;
                color: #2a1200;
                letter-spacing: 0.2em;
                text-shadow: 2px 2px 8px rgba(255,220,120,0.8);
            }}

            .soglia-sottotitolo {{
                font-family: 'Cinzel', serif;
                font-size: 0.85rem;
                color: #3d1f00;
                letter-spacing: 0.3em;
                font-style: italic;
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
            }}

            div[data-testid="column"]:nth-of-type(2) input {{
                width: 200px !important;
                transition: width 0.4s ease !important;
            }}
            
            div[data-testid="column"]:nth-of-type(2) input:focus {{
                width: 300px !important;
            }}

            div.stButton > button {{
                background: #1a1008 !important;
                color: #c9a227 !important;
                border: 1px solid #c9a227 !important;
                font-family: 'Cinzel', serif !important;
                width: 200px !important;
                transition: all 0.4s ease !important;
            }}
            
            div.stButton > button:hover {{
                background: #c9a227 !important;
                color: #1a1008 !important;
                width: 300px !important;
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

    col_vuota_sx, col_login, col_vuota_dx = st.columns([0.03, 0.22, 0.75])
    
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

    # ── BOTTONE HAMBURGER FISSO ──
    st.markdown("""
        <style>
            .hamburger-btn {
                position: fixed;
                top: 14px;
                left: 14px;
                z-index: 999999;
                background: #f5e6cc;
                border: 1.5px solid #bb9457;
                border-radius: 8px;
                width: 42px;
                height: 42px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 5px;
                cursor: pointer;
                box-shadow: 0 2px 8px rgba(0,0,0,0.18);
            }
            .hamburger-btn span {
                display: block;
                width: 22px;
                height: 2.5px;
                background: #5d4037;
                border-radius: 2px;
            }
        </style>

        <div class="hamburger-btn" onclick="toggleSidebar()" title="Apri/Chiudi menu">
            <span></span><span></span><span></span>
        </div>

        <script>
            function toggleSidebar() {
                const doc = window.parent.document;
                const buttons = doc.querySelectorAll('button');
                for (const btn of buttons) {
                    const label = (btn.getAttribute('aria-label') || '').toLowerCase();
                    if (label.includes('sidebar') || label.includes('collapse') || label.includes('expand')) {
                        btn.click();
                        return;
                    }
                }
                const ctrl = doc.querySelector('[data-testid="stSidebarCollapsedControl"] button');
                if (ctrl) { ctrl.click(); return; }
                const close = doc.querySelector('[data-testid="stSidebar"] button');
                if (close) { close.click(); }
            }
        </script>
    """, unsafe_allow_html=True)

    if not st.session_state.welcome_shown:
        st.toast(f"Benvenuto, {st.session_state.utente} ✨")
        st.session_state.welcome_shown = True

    PAGINE = ["Home", "Scrittoio", "Bacheca", "FilosofaMente", "AntropologaMente", "Archivio", "Premio"]

    with st.sidebar:
        st.markdown(
            f"<div style='font-family: EB Garamond, serif; font-size:1.1rem; color:#3e2723; "
            f"font-weight:bold; padding: 0.5rem 0 1rem 0;'>✒️ {st.session_state.utente}</div>",
            unsafe_allow_html=True
        )

        menu = st.selectbox(
            "📂 Navigazione",
            PAGINE,
            key="pagina"
        )

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

    # --- ROUTER DELLE PAGINE ---
    if menu == "Home":
        Home.show()
    elif menu == "Scrittoio":
        Scrittoio.show()
    elif menu == "Bacheca":
        Bacheca.show()
    elif menu == "FilosofaMente":
        FilosofaMente.show()
    elif menu == "AntropologaMente":
        AntropologaMente.show()
    elif menu == "Archivio":
        Archivio.show()
    elif menu == "Premio":
        Premio.show()
import streamlit as st
import os
import base64
from supabase import create_client
# Importiamo i mattoni fondamentali da utils.py
from utils import nav_bar, carica_css, carica_medaglione

# 1. CONFIGURAZIONE PAGINA (Deve essere la primissima istruzione)
st.set_page_config(
    page_title="PoeticaMente",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CONNESSIONE DATABASE (Con gestione errori robusta)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Errore critico di connessione al database: {e}")
    st.stop()

# 3. INIZIALIZZAZIONE SESSION STATE
# authenticated: serve per la Soglia di accesso
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# utente: memorizza chi è loggato per filtrare Archivio e Scrittoio
if "utente" not in st.session_state:
    st.session_state.utente = ""

# ────────────────────────────────────────────────────────
# LOGICA DI ACCESSO (SOGLIA)
# ────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    # Carichiamo lo stile e il medaglione solo per la login
    carica_css()
    medaglione_b64 = carica_medaglione() # Punta a assets/Fronte.png
    img_src = f"data:image/png;base64,{medaglione_b64}" if medaglione_b64 else ""

    # Interfaccia grafica della Soglia
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&display=swap');
            
            /* Nascondiamo header e menu nativi per immersione totale */
            header, [data-testid="stHeader"], footer {{ display: none !important; }}
            
            html, body, .stApp {{ background-color: #f5c37a !important; }}
            
            .medaglione-bg {{ 
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                object-fit: cover; z-index: 0; pointer-events: none; 
            }}
            .soglia-testi {{ 
                position: fixed; top: 6vh; left: 8vw; z-index: 2; max-width: 28vw; 
            }}
            .soglia-titolo {{ 
                font-family: 'Cinzel', serif; font-size: 3.5rem; font-weight: 700; color: #2a1200; 
            }}
            .soglia-citazione {{ 
                font-family: 'EB Garamond', serif; font-size: 1.1rem; color: #2a1200; 
                font-style: italic; border-left: 3px solid #c9a227; padding-left: 0.8rem; line-height: 1.7; 
            }}
        </style>
        <img class="medaglione-bg" src="{img_src}">
        <div class="soglia-testi">
            <div class="soglia-titolo">SOGLIA</div>
            <div style="font-family: 'Cinzel', serif; color: #3d1f00; letter-spacing: 0.3em; margin-bottom: 10px;">
                PENSIERO ED OPERA
            </div>
            <div class="soglia-citazione">"La vera vita è molto breve.<br>L'esistere è un'altra cosa."</div>
        </div>
    """, unsafe_allow_html=True)

    # Spazio verticale per allineare il box di login
    st.markdown("<div style='height: 62vh'></div>", unsafe_allow_html=True)
    
    col_v, col_login, col_v2 = st.columns([0.03, 0.22, 0.75])
    
    with col_login:
        u = st.text_input("L'Identità", placeholder="Chi bussa?", key="input_u")
        p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="input_p")
        
        if st.button("VARCA IL PORTALE", use_container_width=True):
            if u and p:
                try:
                    user_val = str(u).strip()
                    pass_val = str(p).strip()
                    
                    # Verifica credenziali su Supabase
                    res = supabase.table("Opere").select("autore").eq("autore", user_val).eq("codice_firma", pass_val).execute()
                    
                    if res.data:
                        st.session_state.authenticated = True
                        st.session_state.utente = user_val
                        st.rerun() # Ricarica per passare al blocco else
                    else:
                        st.error("🔒 Le chiavi non corrispondono o l'identità è ignota.")
                except Exception as e:
                    st.error(f"Errore tecnico durante l'accesso: {e}")
            else:
                st.warning("È necessario fornire sia Identità che Chiave.")

# ────────────────────────────────────────────────────────
# SEZIONE POST-AUTENTICAZIONE: IL REDIRECT
# ────────────────────────────────────────────────────────
else:
    # Una volta loggati, app.py non deve mostrare nulla.
    # Deve solo lanciare l'utente nella Home delle pagine multi-page.
    # Questo risolve il problema dei conflitti di navigazione.
    st.switch_page("pages/Home.py")
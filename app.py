import streamlit as st
import os
from supabase import create_client

# =========================
# IMPORT PAGINE
# =========================
from pages import Home, Scrittoio, Bacheca, Archivio, Filosofamente, Premio

# =========================
# CONFIG PAGINA
# =========================
st.set_page_config(
    page_title="Poeticamente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# =========================
# LOGICA DI NAVIGAZIONE
# =========================

# 1. SE NON AUTENTICATO: MOSTRA LA SOGLIA
if not st.session_state.authenticated:

    # Caricamento CSS per l'estetica del medaglione
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Medaglione + Testi
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

    # Input Utente
    u = st.text_input("L'Identità", placeholder="Chi bussa?", key="u")
    p = st.text_input("La Chiave", type="password", placeholder="La firma...", key="p")
    w = st.text_input("La Parola d'Ordine", type="password", placeholder="Sussurra...", key="w")

    # Bottone Login - QUERY BLINDATA ANTI-PGRST100
    if st.button("VARCA IL PORTALE", width="stretch"):
        if u and p and w:
            try:
                # Esecuzione query senza filtri "Filters.EQ" per evitare crash
                res = supabase.table("Opere").select("autore") \
                    .eq("autore", str(u).strip()) \
                    .eq("codice_firma", str(p).strip()) \
                    .eq("parola_ordine", str(w).strip()) \
                    .execute()
                
                if res.data and len(res.data) > 0:
                    st.session_state.authenticated = True
                    st.session_state.utente = u
                    st.rerun()
                else:
                    st.error("Il silenzio non risponde. Chiavi errate.")
            except Exception as e:
                st.error(f"Errore tecnico: {e}")
        else:
            st.warning("La Soglia richiede che ogni campo sia colmato.")

# 2. SE AUTENTICATO: MOSTRA L'APP REALE
else:
    # Qui il modulo di login sparisce e parte la tua Home
    Home.show() 
    # Se la tua Home usa .run() invece di .show(), usa Home.run()
    
    # Opzionale: un messaggio di successo temporaneo
    # st.toast(f"Benvenuto, {st.session_state.utente}")
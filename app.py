import streamlit as st
from Pages import Home, Scrittoio, Bacheca

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="Poeticamente", page_icon="🖋️", layout="wide")

# --- STILE CSS GLOBALE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
.stApp { background-color: #fdf5e6 !important; color: #2b1d0e !important; font-family: 'EB Garamond', serif !important; }
.poetic-title { font-family: 'Playfair Display', serif; font-size: 4rem; text-align: center; color: #1a1a1a; margin-top: -40px; }
.stButton button { background-color: #2b1d0e !important; color: #fdf5e6 !important; border: 1px solid #d4af37 !important; font-family: 'Playfair Display', serif !important; border-radius: 0px !important; }
#MainMenu, footer, header {visibility: hidden;}
.codice-onore { background-color: #f4ece0; padding: 15px; border-left: 5px solid #d4af37; font-style: italic; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- GESTIONE ACCESSO ---
if "utente" not in st.session_state:
    st.session_state.utente = None

if st.session_state.utente is None:
    st.markdown("<h1 class='poetic-title'>Benvenuto su Poeticamente 🖋️</h1>", unsafe_allow_html=True)
    
    st.write("### Identificazione del Poeta")
    col1, col2 = st.columns(2)
    with col1:
        nuovo_pseudo = st.text_input("Pseudonimo:")
    with col2:
        email_utente = st.text_input("Email:")
    
    st.markdown("<div class='codice-onore'><strong>Codice d'Onore:</strong><br>Prometto di onorare l'arte della parola e di non usare automazioni.</div>", unsafe_allow_html=True)
    accetto_codice = st.checkbox("Accetto il Codice d'Onore")
    
    st.write("---")
    st.write("#### Sfida di Verità")
    captcha_input = st.text_input("Completa il verso: 'Nel mezzo del cammin di nostra...'")

    if st.button("Entra nello Scrittoio"):
        if nuovo_pseudo.strip() and email_utente.strip() and accetto_codice and captcha_input.strip().lower() == "vita":
            st.session_state.utente = nuovo_pseudo.strip()
            st.rerun()
        else:
            st.error("Verifica i dati, accetta il codice o risolvi correttamente la sfida poetica.")
else:
    # --- NAVIGAZIONE ---
    st.sidebar.title(f"Poeta: {st.session_state.utente}")
    if st.sidebar.button("Logout"):
        st.session_state.utente = None
        st.rerun()
        
    page = st.sidebar.radio("Vai a:", ["Home", "Scrittoio", "Bacheca"])

    if page == "Home": Home.show()
    elif page == "Scrittoio": Scrittoio.show()
    elif page == "Bacheca": Bacheca.show()
import streamlit as st
import os
import base64

# --- FUNZIONI DI SUPPORTO GRAFICO ---

def carica_css():
    """Carica lo stile dal file style.css esterno"""
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(image_path):
    """Utility per convertire immagini in base64 (usata per watermark e loghi)"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None
def carica_medaglione():
    """Carica l'immagine per la schermata di apertura"""
    path = "assets/Fronte.png"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None
# --- MENU DI NAVIGAZIONE ---

def nav_bar():
    # Usiamo un expander per non rubare spazio ai contenuti
    with st.expander("📖 MENU DI NAVIGAZIONE", expanded=False):
        # Definiamo le 7 pagine (Aggiunto Premio come da image_1b6606.png)
        pagine = [
            ("🏠 HOME", "pages/Home.py"),
            ("📝 SCRITTOIO", "pages/Scrittoio.py"),
            ("📌 BACHECA", "pages/Bacheca.py"),
            ("🧠 FILOSOFAMENTE", "pages/FilosofaMente.py"),
            ("🌍 ANTROPOLOGAMENTE", "pages/AntropologaMente.py"),
            ("📚 ARCHIVIO", "pages/Archivio.py"),
            ("🏆 PREMIO", "pages/Premio.py")
        ]
        
        # Sette colonne per sette tasti
        # Ho bilanciato i pesi per i titoli più lunghi (AntropologaMente e FilosofaMente)
        cols = st.columns([1, 1.2, 1.2, 1.8, 1.8, 1.2, 1.2])
        
        for i, (label, path) in enumerate(pagine):
            with cols[i]:
                # Key univoca basata sul label per evitare "Duplicate Widget ID"
                # use_container_width=True rende i tasti uniformi
                if st.button(label, key=f"nav_{i}", use_container_width=True):
                    # Nota: assicurati che il file pages/Premio.py esista fisicamente!
                    st.switch_page(path)
                    
    st.markdown("---")
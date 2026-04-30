import streamlit as st
import os
import base64
from utils import nav_bar, carica_css  # Importazione fondamentale

def get_base64_image(path):
    """Legge l'immagine e la converte in base64 per l'integrazione HTML."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def show():
    # 1. Carica lo stile globale e il menu superiore
    carica_css()
    nav_bar()
    
    # CSS specifico per la Home (sfondo e rifiniture)
    st.markdown("""
        <style>
        .medaglione-wrapper-home {
            position: fixed;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: -1;
            opacity: 0.08;
            pointer-events: none;
        }

        .medaglione-img-home {
            width: 55vw;
            filter: sepia(0.5) contrast(1.1);
        }

        h1 {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #2c1a0e;
            font-size: 3.5rem !important;
            margin-top: 10px !important;
        }
        
        .rules-card {
            background-color: rgba(255, 255, 255, 0.2);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(187, 148, 87, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Caricamento Medaglione (Sfondo invisibile)
    img_b64 = get_base64_image("assets/Fronte.png")
    if img_b64:
        st.markdown(f"""
            <div class="medaglione-wrapper-home">
                <img src="data:image/png;base64,{img_b64}" class="medaglione-img-home">
            </div>
        """, unsafe_allow_html=True)

    # 3. Intestazione
    st.markdown("<h1>PoeticaMente</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family: \"EB Garamond\", serif; font-style: italic; font-size: 1.4rem; color: #8d6e63; margin-bottom: 45px;'>Dimora sacra per l'arte del verso</p>", unsafe_allow_html=True)

    # 4. Colonne Contenuto
    col1, col2 = st.columns([1.8, 1], gap="large")

    with col1:
        st.markdown("""
            <div style='font-family: "EB Garamond", serif; font-size: 1.4rem; line-height: 1.6; text-align: justify; margin-bottom: 35px; color: #432818;'>
                PoeticaMente è uno spazio dedicato a chi trasforma il silenzio in rime. 
                Qui, ogni parola ha un peso e ogni autore un volto. Ogni verso affidato a queste pagine 
                diventa parte di un'antologia senza tempo, custodita nel cuore della bellezza.
            </div>
        """, unsafe_allow_html=True)

        # Sezione descrizioni (Con istruzioni per l'affissione)
        st.markdown(
            "<div style='font-family: \"EB Garamond\", serif; font-size: 1.25rem; color: #432818; line-height: 1.8;'>"
            "<p>🖋️ <b>Lo Scrittoio</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Il tuo spazio privato. Componi in tranquillità e, quando sei pronto, attiva <b>'Affiggi in Bacheca'</b> per condividere i tuoi versi.</span></p>"
            "<p>📖 <b>La Bacheca</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Il cuore pubblico di PoeticaMente. Qui appaiono solo le opere che gli autori hanno deciso di mostrare al mondo.</span></p>"
            "<p>🏛️ <b>FilosofaMente</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Evoca i maestri. Lascia che una scintilla di pensiero illumini la tua penna.</span></p>"
            "<p>🌍 <b>AntropologaMente</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Esplora le radici dell'umano e le culture che hanno dato voce al mondo.</span></p>"
            "<p>📚 <b>L'Archivio</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Ripercorri i passi del passato e ritrova i versi che hanno fatto la storia.</span></p>"
            "<p>🏆 <b>Il Premio</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>L'eccellenza del verso viene celebrata qui. Partecipa alla selezione mensile.</span></p>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("""
            <div class="rules-card">
                <h3 style="font-size: 1.7rem; margin-top: 0; color: #432818; font-family: 'Cinzel', serif;">IL CODICE DEL POETA</h3>
                <hr style="border: 0; border-top: 1px solid #d2b48c; margin: 20px 0;">
                <ul style="list-style-type: none; padding-left: 0; font-family: 'EB Garamond', serif; font-size: 1.15rem; line-height: 1.8;">
                    <li style="margin-bottom: 18px;">📜 <b>Identità:</b> Lo pseudonimo è il tuo vessillo, onoralo con sincerità.</li>
                    <li style="margin-bottom: 18px;">✒️ <b>Decoro:</b> La poesia eleva l'animo, scrivi per costruire bellezza.</li>
                    <li style="margin-bottom: 18px;">🔒 <b>Legame:</b> Ogni verso è sacro e appartiene indissolubilmente al suo autore.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # Saluto personalizzato
        utente = st.session_state.get('utente', 'Poeta')
        if utente:
            st.markdown(f"""
                <div style="margin-top: 30px; padding: 15px; border-left: 3px solid #bb9457; font-style: italic; color: #5d4037; background-color: rgba(187, 148, 87, 0.1);">
                    Il calamaio di <b>{utente}</b> è pronto per nuova linfa.
                </div>
            """, unsafe_allow_html=True)
            
        # Pulsante rapido per il Premio (come suggerito dai tuoi appunti)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏆 VAI AL PREMIO", use_container_width=True):
            st.session_state.pagina = "Premio"
            st.rerun()

if __name__ == "__main__":
    show()

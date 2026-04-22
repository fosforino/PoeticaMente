import streamlit as st
import os
import base64

def get_base64_image(path):
    """Legge l'immagine e la converte in base64 per l'integrazione HTML."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def show():
    # 1. Caricamento Medaglione come Filigrana (Background)
    img_b64 = get_base64_image("Fronte.png")
    if img_b64:
        st.markdown(f"""
            <div class="medaglione-wrapper-home">
                <img src="data:image/png;base64,{img_b64}" class="medaglione-img-home">
            </div>
        """, unsafe_allow_html=True)

    # 2. Intestazione Principale
    st.markdown("<h1>PoeticaMente</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family: \"EB Garamond\", serif; font-style: italic; font-size: 1.4rem; color: #8d6e63; margin-bottom: 45px;'>Dimora sacra per l'arte del verso</p>", unsafe_allow_html=True)

    # 3. Layout a due colonne
    col1, col2 = st.columns([1.8, 1], gap="large")

    with col1:
        # Testo introduttivo
        st.markdown("""
            <div style='font-family: "EB Garamond", serif; font-size: 1.4rem; line-height: 1.6; text-align: justify; margin-bottom: 35px; color: #432818;'>
                PoeticaMente è uno spazio dedicato a chi trasforma il silenzio in rime. 
                Qui, ogni parola ha un peso e ogni autore un volto. Ogni verso affidato a queste pagine 
                diventa parte di un'antologia senza tempo, custodita nel cuore della bellezza.
            </div>
        """, unsafe_allow_html=True)

        # Voci non cliccabili (solo testo descrittivo)
        st.markdown(
            "<div style='font-family: \"EB Garamond\", serif; font-size: 1.25rem; color: #432818; line-height: 2;'>"
            "<p>&#128393; <b>Lo Scrittoio</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Il tuo spazio privato. Componi in tranquillità il tuo manoscritto.</span></p>"
            "<p>&#128214; <b>La Bacheca</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Affiggi i tuoi versi al cuore del mondo. Leggi e lasciati ispirare.</span></p>"
            "<p>&#127963; <b>FilosofaMente</b><br>"
            "<span style='font-style: italic; color: #6d4c41;'>Evoca i maestri. Lascia che una scintilla di pensiero illumini la tua penna.</span></p>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        # Card laterale del Codice
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

        # Messaggio di benvenuto utente
        if st.session_state.get('utente'):
            st.markdown(f"""
                <div style="margin-top: 30px; padding: 15px; border-left: 3px solid #bb9457; font-style: italic; color: #5d4037;">
                    Il calamaio di <b>{st.session_state.utente}</b> è pronto per nuova linfa.
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
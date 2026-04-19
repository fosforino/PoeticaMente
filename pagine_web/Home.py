import streamlit as st
import os
import base64

def get_base64_image(image_path):
    """Restituisce il contenuto base64 di un'immagine se esiste."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    """Applica lo stile con il medaglione Fronte.png ben visibile."""
    # Cerchiamo il file con il nuovo nome
    path_icona = "Fronte.png"  
    img_base64 = get_base64_image(path_icona)
    
    # Se non lo trova nella root, prova nella cartella assets (giusto per sicurezza)
    if not img_base64:
        img_base64 = get_base64_image("assets/Fronte.png")

    img_html = f"""
        <div class="medaglione-wrapper-home">
            <img src="data:image/png;base64,{img_base64}" class="medaglione-img-home">
        </div>
    """ if img_base64 else ""

    st.markdown(
        f"""
        <style>
        /* Contenitore Medaglione - Centrato e Nitido */
        .medaglione-wrapper-home {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 550px; /* Un po' più grande per dare impatto */
            z-index: -1;
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: none;
        }}

        .medaglione-img-home {{
            width: 100%;
            opacity: 0.20 !important; /* Alzato per essere sicuri di vederlo */
            filter: sepia(0.4) brightness(1.1); /* Tocco vintage */
        }}

        /* Stile App */
        .stApp {{
            background-color: #fdf5e6 !important;
        }}

        .poetic-title-home {{ 
            font-family: 'Cinzel', serif; 
            font-size: 4.5rem; 
            color: #3e2723; 
            text-align: center; 
            margin-bottom: 0px;
        }}
        </style>
        {img_html}
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()

    st.markdown("<h1 class='poetic-title-home'>PoeticaMente ✒️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='home-subtitle'>Dimora sacra per l'arte del verso</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.8, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style='font-family: "EB Garamond", serif; font-size: 1.45rem; line-height: 1.9; text-align: justify; margin-bottom: 30px;'>
        Poeticamente è uno spazio dedicato a chi trasforma il silenzio in rime. 
        Qui, ogni parola ha un peso e ogni autore un volto. Ogni verso affidato a queste pagine diventa parte di un'antologia senza tempo.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-box'>
            <strong>🖋️ Lo Scrittoio</strong>
            <p>Il tuo spazio privato. Componi in tranquillità, con la cura di chi stila un manoscritto prezioso.</p>
        </div>
        <div class='feature-box'>
            <strong>📖 La Bacheca</strong>
            <p>Affiggi i tuoi versi al cuore del mondo. Leggi e lasciati ispirare dalla comunità.</p>
        </div>
        <div class='feature-box'>
            <strong>🏛️ FilosofaMente</strong>
            <p>Evoca i grandi maestri del passato. Lascia che una scintilla di pensiero illumini la tua penna.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='rules-card'>
            <h3 style='text-align: center; margin-top: 0; color: #3e2723; font-family: "Playfair Display";'>Il Codice del Poeta</h3>
            <hr style='border: 0.5px solid #d2b48c; margin: 15px 0;'>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 15px;'>📜 <b>Identità:</b> Lo pseudonimo è il tuo vessillo.</li>
                <li style='margin-bottom: 15px;'>✒️ <b>Decoro:</b> La poesia eleva l'animo.</li>
                <li style='margin-bottom: 15px;'>🔒 <b>Legame:</b> Ogni verso appartiene al suo autore.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.get('utente'):
        st.markdown(
            f"""
            <div class='status-msg'>
                Bentornato, <strong>{st.session_state.utente}</strong>. Il tuo calamaio ti attende.
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    show()
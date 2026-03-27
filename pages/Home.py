import streamlit as st
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    """Applica l'estetica 'Parchment & Ink' ottimizzata per la leggibilità."""
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = ""
    
    if img_base64:
        img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-home">'

    st.markdown(
        f"""
        <style>
        /* Testo base più grande e arioso */
        .stApp {{
            color: #3e2723;
            line-height: 1.8;
        }}

        .bg-watermark-home {{
            position: fixed;
            top: 55%; left: 50%;
            transform: translate(-50%, -50%);
            width: 65vw; opacity: 0.06;
            filter: blur(10px);
            z-index: -1; pointer-events: none;
        }}

        .poetic-title-home {{ 
            font-family: 'Playfair Display', serif; 
            font-size: 4rem; color: #3e2723; 
            text-align: center; margin-top: -20px;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        
        .home-subtitle {{
            font-family: 'EB Garamond', serif;
            font-style: italic; font-size: 1.8rem;
            text-align: center; color: #5d4037;
            margin-bottom: 50px;
        }}

        /* Box trasparenti ma leggibili per non coprire lo sfondo */
        .feature-box {{
            background-color: rgba(255, 250, 240, 0.4);
            padding: 25px; border-radius: 8px;
            border-left: 4px solid #c19a6b;
            margin-bottom: 25px; /* Più spazio tra i box */
            color: #3e2723;
            font-size: 1.25rem;
            line-height: 1.6;
        }}
        
        .feature-box strong {{
            color: #3e2723;
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            display: block;
            margin-bottom: 8px;
        }}

        .rules-card {{
            background-color: rgba(244, 236, 224, 0.7);
            padding: 25px; border-radius: 4px;
            border: 1px solid #d2b48c;
            font-family: 'EB Garamond', serif;
            font-size: 1.2rem;
        }}

        .status-msg {{
            text-align: center; padding: 20px; 
            border-radius: 6px; 
            background-color: rgba(193, 154, 107, 0.2); 
            border: 1px solid #c19a6b;
            color: #3e2723; font-style: italic;
            font-size: 1.3rem;
            margin-top: 30px;
        }}
        </style>
        {img_html}
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()

    st.markdown("<h1 class='poetic-title-home'>Poeticamente ✒️</h1>", unsafe_allow_html=True)
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
            <strong>🏛️ Filosofamente</strong>
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
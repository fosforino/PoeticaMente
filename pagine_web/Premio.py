import streamlit as st
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def show():
    # Stile CSS per rendere il video più "tridimensionale" e materico
    st.markdown("""
        <style>
        .video-wrapper {
            border: 4px solid #c9a227; /* Oro bronzato */
            border-radius: 15px;
            box-shadow: 0 0 50px rgba(201, 162, 39, 0.2), inset 0 0 20px rgba(0,0,0,0.5);
            padding: 10px;
            background: #1a1008; /* Sfondo scuro per far risaltare il bronzo */
            margin: 20px auto;
            max-width: 850px;
        }
        .titolo-premio {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #1a1a1a;
            font-size: 3rem;
            letter-spacing: 8px;
            text-transform: uppercase;
            margin-bottom: 30px;
        }
        .citazione-premio {
            font-family: 'EB Garamond', serif;
            text-align: center;
            color: #5d4037;
            font-style: italic;
            font-size: 1.8rem;
            margin-top: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='titolo-premio'>Il Tuo Riconoscimento</div>", unsafe_allow_html=True)
    
    video_path = "assets/Medaglia_v2.mp4"
    img_icon_path = "assets/Icona.png"
    
    if os.path.exists(video_path):
        # I palloncini per celebrare il traguardo
        st.balloons()
        
        # Inseriamo il video nel contenitore stilizzato
        st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
        st.video(video_path)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Il video della medaglia non è stato trovato. Assicurati che il render sia completo.")
    
    # Spazio e Icona finale
    st.markdown("<br>", unsafe_allow_html=True)
    img_base64 = get_base64_image(img_icon_path)
    if img_base64:
        st.markdown(f"""
            <div style="text-align:center;">
                <img src="data:image/png;base64,{img_base64}" style="width:80px; opacity:0.6; filter: sepia(100%);">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='citazione-premio'>L'Alchimia tra il Pensiero e il Verso.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
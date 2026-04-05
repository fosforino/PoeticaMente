import streamlit as st
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def show():
    st.markdown("<h1>Il Tuo Riconoscimento</h1>", unsafe_allow_html=True)
    
    video_path = "assets/Medaglia_v2.mp4"
    img_icon_path = "assets/Icona.png"
    
    if os.path.exists(video_path):
        st.balloons()
        st.video(video_path)
    else:
        st.error("Video non trovato in assets/Medaglia_v2.mp4")
    
    # Icona della medaglia
    img_base64 = get_base64_image(img_icon_path)
    if img_base64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{img_base64}" style="width:20%; opacity:0.8;"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center;'>L'Alchimia tra il Pensiero e il Verso.</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
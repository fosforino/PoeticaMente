import streamlit as st
import os

def show():
    st.markdown("<h1>Il Tuo Riconoscimento</h1>", unsafe_allow_html=True)
    
    video_path = "assets/medaglia_v2.mp4"
    
    if os.path.exists(video_path):
        st.balloons()
        st.video(video_path)
        st.markdown("<h2 style='text-align:center;'>L'Alchimia tra il Pensiero e il Verso.</h2>", unsafe_allow_html=True)
    else:
        st.error("Video non trovato in assets/medaglia_v2.mp4")

if __name__ == "__main__":
    show()
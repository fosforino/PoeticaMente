import streamlit as st

st.set_page_config(
    page_title="Poeticamente",
    page_icon="🖋️",
    layout="wide"
)

st.markdown("""
<style>
.stApp { 
    background: linear-gradient(to bottom, #fdf5e6, #f5e1b8) !important;
    color: #2b1d0e !important; 
    font-family: 'EB Garamond', serif !important; 
}
.poetic-title { 
    font-family: 'Playfair Display', serif; 
    font-size: 4rem; 
    text-align: center; 
    color: #1a1a1a; 
    margin-top: -40px; 
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)
st.markdown("Benvenuto nell'atelier poetico! 🌿 Usa il menu a sinistra per scrivere nuove poesie o sfogliare le opere pubblicate.")
import streamlit as st
from supabase import create_client, Client

# --- Config Supabase ---
URL = "https://eeavavlfgeeusijiljfw.supabase.co"
KEY = "sb_publishable_PP-gOScRnNcN9JiD4uN4lQ_hCN0xL7j"
supabase: Client = create_client(URL, KEY)

# --- Stile pergamena ---
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(to bottom, #fdf5e6, #f5e1b8) !important;
    color: #2b1d0e !important; 
    font-family: 'EB Garamond', serif !important; 
    padding: 20px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📜 Bacheca Poetica")

# Mostra solo poesie approvate
res = supabase.table("Poesie").select("*").eq("approvata", True).order("id", desc=True).execute()
poesie = res.data

if poesie:
    for opera in poesie:
        st.markdown(f"### {opera['titolo']}")
        st.markdown(f"_{opera['autore']}_")
        st.markdown(f"{opera['versi']}")
        st.markdown("---")
else:
    st.info("Non ci sono opere pubblicate al momento.")
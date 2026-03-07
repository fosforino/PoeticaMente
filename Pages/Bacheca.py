import streamlit as st
from supabase import create_client

URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

def show():
    st.header("Bacheca Poetica 🖋️") [cite: 22]
    
    try:
        # Recuperiamo le ultime 20 poesie per non appesantire il sistema
        res = supabase.table("Poesie").select("*").order("created_at", desc=True).limit(20).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.write("La bacheca è ancora vuota. Sii il primo a scrivere!")
        
        for p in poemi:
            with st.container():
                st.markdown(f"### {p['titolo']}") [cite: 28]
                st.caption(f"Scritta da: {p['autore']}") [cite: 28]
                st.text(p['versi']) [cite: 28]
                st.markdown("---")
    except Exception as e:
        st.error(f"Errore nel caricamento della bacheca: {e}")
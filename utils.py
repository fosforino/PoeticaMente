import streamlit as st

def nav_bar():
    with st.expander("📖 MENU DI NAVIGAZIONE", expanded=True):
        cols = st.columns(6)

        with cols[0]:
            if st.button("🏠 Home", key="n_h"):
                st.switch_page("Home.py")

        with cols[1]:
            if st.button("📝 Scrivi", key="n_s"):
                st.switch_page("Scrittoio.py")

        with cols[2]:
            if st.button("📌 Bacheca", key="n_b"):
                st.switch_page("Bacheca.py")

        with cols[3]:
            if st.button("🧠 Filosofa", key="n_f"):
                st.switch_page("Filosofamente.py")

        with cols[4]:
            if st.button("📚 Archivio", key="n_a"):
                st.switch_page("Archivio.py")

        with cols[5]:
            if st.button("🏆 Premi", key="n_p"):
                st.switch_page("Premio.py")

    st.markdown("---")
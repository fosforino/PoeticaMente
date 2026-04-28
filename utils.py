import streamlit as st

def nav_bar():
    # Usiamo un contenitore per raggruppare il menu
    with st.expander("📖 MENU DI NAVIGAZIONE", expanded=True):
        # 7 colonne per includere la nuova pagina Antropologa
        cols = st.columns(7)

        with cols[0]:
            if st.button("🏠 Home", key="n_h", use_container_width=True):
                st.switch_page("pagine_web/Home.py")

        with cols[1]:
            if st.button("📝 Scrivi", key="n_s", use_container_width=True):
                st.switch_page("pagine_web/Scrittoio.py")

        with cols[2]:
            if st.button("📌 Bacheca", key="n_b", use_container_width=True):
                st.switch_page("pagine_web/Bacheca.py")

        with cols[3]:
            if st.button("🧠 Filosofa", key="n_f", use_container_width=True):
                st.switch_page("pagine_web/FilosofaMente.py")
        
        with cols[4]:
            if st.button("🌍 Antropologa", key="n_ant", use_container_width=True):
                st.switch_page("pagine_web/AntropologaMente.py") 

        with cols[5]:
            if st.button("📚 Archivio", key="n_a", use_container_width=True):
                st.switch_page("pagine_web/Archivio.py")

        with cols[6]:
            if st.button("🏆 Premi", key="n_p", use_container_width=True):
                st.switch_page("pagine_web/Premio.py")

    st.markdown("---")
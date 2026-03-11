import streamlit as st
from supabase import create_client

def show():
    # 1. Estetica (Sfondo crema e font Serif)
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f5dc;
        }
        h1, h2, h3, p, label {
            font-family: 'Georgia', serif;
            color: #2c3e50;
        }
        .stButton>button {
            border-radius: 20px;
            font-family: 'Georgia', serif;
        }
        </style>
        """, unsafe_allow_html=True)

    # 2. Connessione a Supabase
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # 3. Controllo Utente
    if "user" in st.session_state:
        user_id = st.session_state.user.id
        user_email = st.session_state.user.email

        st.title("✒️ Lo Scrittoio")
        st.write(f"*Benvenuto, {user_email}.*")

        # --- Sidebar: Archivio ---
        st.sidebar.header("Il tuo Archivio")
        res = supabase.table("poesie").select("*").eq("user_id", user_id).order("creato_il", desc=True).execute()
        opere = res.data
        
        opzioni = ["Nuova Opera"] + [o['titolo'] for o in opere]
        scelta = st.sidebar.selectbox("Carica opera:", opzioni)

        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        # Variabili pre-compilate
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['contenuto'] if opera_corrente else ""
        v_cat = opera_corrente['categoria'] if opera_corrente else "Poesia"
        v_link = opera_corrente.get('link_riferimento', "") if opera_corrente else ""
        
        tags_raw = opera_corrente.get('tag', []) if opera_corrente else []
        v_tag = ", ".join(tags_raw) if isinstance(tags_raw, list) else ""

        # --- Interfaccia ---
        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo", value=v_titolo)
        with col_c:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        testo = st.text_area("Scrivi qui", value=v_testo, height=400)
        
        with st.expander("Extra"):
            link_r = st.text_input("Link", value=v_link)
            tag_i = st.text_input("Tag (virgola)", value=v_tag)

        # --- Bottoni ---
        c_salva, c_canc, c_stampa = st.columns(3)

        with c_salva:
            if st.button("💾 Salva"):
                l_tag = [t.strip() for t in tag_i.split(",")] if tag_i else []
                dati = {
                    "user_id": user_id,
                    "titolo": titolo,
                    "contenuto": testo,
                    "categoria": categoria,
                    "link_riferimento": link_r,
                    "tag": l_tag,
                    "autore_email": user_email
                }
                if opera_corrente:
                    supabase.table("poesie").update(dati).eq("id", opera_corrente['id']).execute()
                else:
                    supabase.table("poesie").insert(dati).execute()
                st.success("Salvato!")
                st.rerun()

        with c_canc:
            if opera_corrente and st.button("🗑️ Elimina"):
                supabase.table("poesie").delete().eq("id", opera_corrente['id']).execute()
                st.rerun()

        with c_stampa:
            if titolo and testo:
                output = f"{titolo}\n\n{testo}"
                st.download_button("🖨️ Scarica TXT", data=output, file_name=f"{titolo}.txt")
    else:
        st.warning("Esegui il login nella Home.")

if __name__ == "__main__":
    show()
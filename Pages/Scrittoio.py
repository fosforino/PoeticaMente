import streamlit as st
from supabase import create_client

def show():
    # Stile Old-Fashioned (Sfondo crema e font Serif)
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f5dc; /* Sfondo Crema/Parchment */
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

    # --- Logica di Connessione ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "user" in st.session_state:
        user_id = st.session_state.user.id
        user_email = st.session_state.user.email

        st.title("✒️ Lo Scrittoio")
        st.write(f"*Benvenuto, {user_email}. Lascia che le tue parole trovino dimora.*")

        # --- SIDEBAR: Gestione Opere Esistenti ---
        st.sidebar.header("Il tuo Archivio")
        # Recuperiamo le opere dell'utente
        res = supabase.table("poesie").select("*").eq("user_id", user_id).order("creato_il", desc=True).execute()
        opere = res.data
        
        opzioni_archivio = ["Nuova Opera"] + [o['titolo'] for o in opere]
        scelta = st.sidebar.selectbox("Carica un'opera:", opzioni_archivio)

        # Inizializzazione variabili
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        val_titolo = opera_corrente['titolo'] if opera_corrente else ""
        val_contenuto = opera_corrente['contenuto'] if opera_corrente else ""
        val_cat = opera_corrente['categoria'] if opera_corrente else "Poesia"
        val_link = opera_corrente.get('link_riferimento', "") if opera_corrente else ""
        
        # Gestione sicura dei tag
        tags_raw = opera_corrente.get('tag', []) if opera_corrente else []
        val_tag = ", ".join(tags_raw) if isinstance(tags_raw, list) else ""

        # --- INTERFACCIA PRINCIPALE ---
        col1, col2 = st.columns([2, 1])
        with col1:
            titolo = st.text_input("Titolo dell'Opera", value=val_titolo)
        with col2:
            lista_categories = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx_cat = lista_categories.index(val_cat) if val_cat in lista_categories else 0
            categoria = st.selectbox("Categoria", lista_categories, index=idx_cat)

        contenuto = st.text_area("Versi o Prosa", value=val_contenuto, height=400)
        
        with st.expander("Dettagli aggiuntivi (Link e Tag)"):
            link = st.text_input("Link di riferimento", value=val_link)
            tag_input = st.text_input("Tag (separati da virgola)", value=val_tag)

        # --- TASTI AZIONE ---
        col_salva, col_canc, col_stampa = st.columns(3)

        with col_salva:
            if st.button("💾 Salva nel Registro"):
                lista_tag = [t.strip() for t in tag_input.split(",")] if tag_input else []
                dati = {
                    "user_id": user_id,
                    "titolo": titolo,
                    "contenuto": contenuto,
                    "categoria": categoria,
                    "link_riferimento": link,
                    "tag": lista_tag,
                    "autore_email": user_email
                }
                
                if opera_corrente: # Update
                    supabase.table("poesie").update(dati).eq("id", opera_corrente['id']).execute()
                    st.success("L'opera è stata aggiornata.")
                else: # Insert
                    supabase.table("poesie").insert(dati).execute()
                    st.success("L'opera è stata trascritta con cura.")
                st.rerun()

        with col_canc:
            if opera_corrente:
                if st.button("🗑️ Elimina", type="secondary"):
                    supabase.table("poesie").delete().eq("id", opera_corrente['id']).execute()
                    st.error("Opera rimossa dal registro.")
                    st.rerun()

        with col_stampa:
            if titolo and contenuto:
                testo_stampa = f"{titolo}\n\nCategoria: {categoria}\n\n{contenuto}"
                st.download_button(
                    label="🖨️ Scarica per Stampa",
                    data=testo_stampa,
                    file_name=f"{titolo}.txt",
                    mime="text/plain"
                )
    else:
        st.warning("Accedi dalla pagina principale per iniziare a scrivere.")

# Chiamata alla funzione se il file viene eseguito direttamente
if __name__ == "__main__":
    show()
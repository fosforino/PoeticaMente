import streamlit as st
from supabase import create_client, Client

# --- CONNESSIONE SUPABASE (Utilizza i tuoi secrets) ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def show():
    st.markdown("<h1 style='text-align: center; font-family: \"Playfair Display\", serif;'>Lo Scrittoio di Poeticamente ✒️</h1>", unsafe_allow_html=True)
    
    # --- CREAZIONE OPERA ---
    with st.expander("📝 Componi una nuova Opera", expanded=True):
        titolo = st.text_input("Titolo dell'Opera:", key="new_titolo")
        testo = st.text_area("Versi:", height=200, key="new_testo")
        url_immagine = st.text_input("URL Immagine Ispirazionale (Opzionale):")
        
        if st.button("Pubblica su Poeticamente"):
            if titolo and testo:
                data = {
                    "autore": st.session_state.utente,
                    "titolo": titolo,
                    "testo": testo,
                    "immagine_url": url_immagine if url_immagine else None
                }
                # Inserimento su Supabase
                try:
                    supabase.table("opere").insert(data).execute()
                    st.success("L'opera è stata impressa nel database.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nel salvataggio: {e}")
            else:
                st.warning("Titolo e Testo sono il cuore dell'opera. Non possono mancare.")

    st.write("---")
    st.write("### Le Tue Opere")

    # --- RECUPERO DATI ---
    # Recuperiamo solo le opere dell'utente loggato
    response = supabase.table("opere").select("*").eq("autore", st.session_state.utente).order("created_at", desc=True).execute()
    opere = response.data

    if not opere:
        st.info("Il tuo registro è ancora bianco. Comincia a scrivere!")
    else:
        for opera in opere:
            with st.container():
                col_testo, col_azioni = st.columns([3, 1])
                
                with col_testo:
                    st.markdown(f"#### {opera['titolo']}")
                    st.text(opera['testo'])
                    if opera.get('immagine_url'):
                        st.image(opera['immagine_url'], width=250)
                
                with col_azioni:
                    # Tasto MODIFICA (Attiva lo stato di editing per questa specifica riga)
                    if st.button("Modifica ✏️", key=f"btn_edit_{opera['id']}"):
                        st.session_state[f"editing_{opera['id']}"] = True
                    
                    # Tasto ELIMINA
                    if st.button("Elimina 🗑️", key=f"btn_del_{opera['id']}"):
                        supabase.table("opere").delete().eq("id", opera['id']).execute()
                        st.rerun()

                # --- FORM DI MODIFICA INLINE ---
                if st.session_state.get(f"editing_{opera['id']}", False):
                    with st.form(key=f"edit_form_{opera['id']}"):
                        edit_titolo = st.text_input("Modifica Titolo", value=opera['titolo'])
                        edit_testo = st.text_area("Modifica Versi", value=opera['testo'])
                        edit_img = st.text_input("Modifica URL Immagine", value=opera.get('immagine_url', ''))
                        
                        c1, c2 = st.columns(2)
                        if c1.form_submit_button("Salva"):
                            supabase.table("opere").update({
                                "titolo": edit_titolo,
                                "testo": edit_testo,
                                "immagine_url": edit_img if edit_img else None
                            }).eq("id", opera['id']).execute()
                            st.session_state[f"editing_{opera['id']}"] = False
                            st.rerun()
                        
                        if c2.form_submit_button("Annulla"):
                            st.session_state[f"editing_{opera['id']}"] = False
                            st.rerun()
                st.write("---")
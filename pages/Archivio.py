import streamlit as st
from supabase import create_client
import pandas as pd
import io

def show():
    st.markdown("<h1 style='text-align: center; color: #3e2723;'>📊 Il tuo Archivio Personale</h1>", unsafe_allow_html=True)

    # --- CONNESSIONE ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        
        try:
            # Recuperiamo TUTTE le opere dell'utente
            res = supabase.table("Opere").select("*").eq("autore", nome_poeta).execute()
            opere = res.data if res.data else []

            if opere:
                # Creiamo un DataFrame (una tabella intelligente)
                df = pd.DataFrame(opere)
                
                # --- CALCOLI STATISTICI ---
                tot_opere = len(df)
                # Contiamo le parole in ogni riga della colonna 'versi'
                df['num_parole'] = df['versi'].apply(lambda x: len(str(x).split()))
                tot_parole = df['num_parole'].sum()

                # --- VISUALIZZAZIONE CARD STATISTICHE ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Opere Custodite", tot_opere)
                c2.metric("Inchiostro Versato (Parole)", tot_parole)
                c3.metric("Media parole per opera", int(tot_parole/tot_opere))

                st.markdown("---")

                # --- EXPORT CSV ---
                st.subheader("📥 Esporta i tuoi dati")
                # Prepariamo il CSV in memoria
                csv_buffer = io.StringIO()
                # Esportiamo solo le colonne importanti
                df_export = df[['created_at', 'titolo', 'categoria', 'versi']]
                df_export.to_csv(csv_buffer, index=False, encoding='utf-8')
                
                st.download_button(
                    label="Scarica tutto l'Archivio in CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"archivio_{nome_poeta}.csv",
                    mime="text/csv",
                )

                st.markdown("---")

                # --- TABELLA RIASSUNTIVA ---
                st.subheader("📜 Riepilogo Opere")
                st.dataframe(df_export, use_container_width=True)

            else:
                st.info("Non hai ancora custodito nessuna opera. Inizia dallo Scrittoio!")

        except Exception as e:
            st.error(f"Errore nel recupero dati: {e}")
    else:
        st.warning("Effettua l'accesso dalla Home per vedere il tuo archivio.")

if __name__ == "__main__":
    show()
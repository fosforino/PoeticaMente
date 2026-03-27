import streamlit as st
from supabase import create_client
import pandas as pd
import io
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_archive_style():
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-archive">' if img_base64 else ""

    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        }}
        .bg-watermark-archive {{
            position: fixed; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 55vw; opacity: 0.04; filter: blur(8px);
            z-index: -1; pointer-events: none;
        }}
        /* Styling delle metriche */
        [data-testid="stMetricValue"] {{
            font-family: 'Playfair Display', serif;
            color: #3e2723 !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-family: 'EB Garamond', serif;
            font-size: 1.1rem !important;
            color: #795548 !important;
        }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

def show():
    apply_archive_style()
    
    st.markdown("<h1 style='text-align: center; font-family: \"Playfair Display\", serif; color: #3e2723; font-size: 3rem;'>📊 Il tuo Archivio Personale</h1>", unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        
        try:
            # Nota le doppie virgolette f"..." e le singole '{...}' dentro
            res = supabase.table("Opere").select("*").filter("autore", "eq", f"{st.session_state.utente}").order("created_at", desc=True).execute()
            opere = res.data if res.data else []

            if opere:
                df = pd.DataFrame(opere)
                
                # Calcoli
                tot_opere = len(df)
                df['num_parole'] = df['versi'].apply(lambda x: len(str(x).split()))
                tot_parole = df['num_parole'].sum()

                # Dashboard Statistiche
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("📜 Opere Custodite", tot_opere)
                c2.metric("✒️ Inchiostro (Parole)", tot_parole)
                c3.metric("📏 Media per Opera", int(tot_parole/tot_opere) if tot_opere > 0 else 0)

                st.markdown("---")

                # Esportazione
                st.markdown("### 📥 Estrai il tuo Manoscritto")
                df_export = df[['created_at', 'titolo', 'categoria', 'versi']]
                csv_buffer = io.StringIO()
                df_export.to_csv(csv_buffer, index=False, encoding='utf-8')
                
                st.download_button(
                    label="💾 Scarica Archivio in formato CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"archivio_{nome_poeta}.csv",
                    mime="text/csv",
                )

                st.markdown("---")

                # Tabella Riassuntiva
                st.markdown("### 📜 Registro delle Opere")
                # Rendiamo la tabella più leggibile
                df_show = df_export.copy()
                df_show['created_at'] = pd.to_datetime(df_show['created_at']).dt.date
                st.dataframe(df_show, use_container_width=True)

            else:
                st.info("Il tuo archivio è ancora vuoto. Componi la tua prima opera nello Scrittoio!")

        except Exception as e:
            st.error(f"Errore nel recupero dei dati: {e}")
    else:
        st.warning("Posa il calamaio! Devi prima identificarti nella Home.")

if __name__ == "__main__":
    show()
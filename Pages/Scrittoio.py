import streamlit as st
from supabase import create_client

def show():
    # --- STILE 3D REALE E COERENTE ---
    st.markdown("""
        <style>
        /* Sfondo Pergamena (per coerenza con la Home) */
        .stApp {
            background: #f4ecd8 url("https://www.transparenttextures.com/patterns/parchment.png") !important;
        }

        /* Area di scrittura come carta antica */
        .stTextArea textarea {
            background-color: #fffaf0 !important;
            border: 1px solid #c19a6b !important;
            border-radius: 5px !important;
            box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05) !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
        }

        /* BOTTONI 3D "REALISTICI" */
        div.stButton > button {
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            padding: 0.6em 1.2em !important;
            transition: all 0.1s !important;
            border-radius: 8px !important;
            text-transform: uppercase;
        }

        /* SALVA - Verde Smeraldo Profondo */
        div.stButton > button[key="btn_salva"] {
            background: #2e7d32 !important;
            box-shadow: 0 5px 0 #1b5e20, 0 8px 15px rgba(0,0,0,0.2) !important;
        }
        div.stButton > button[key="btn_salva"]:active {
            box-shadow: 0 2px 0 #1b5e20 !important;
            transform: translateY(3px) !important;
        }

        /* STAMPA - Blu Notte */
        div.stButton > button[key="btn_stampa"] {
            background: #1565c0 !important;
            box-shadow: 0 5px 0 #0d47a1, 0 8px 15px rgba(0,0,0,0.2) !important;
        }
        div.stButton > button[key="btn_stampa"]:active {
            box-shadow: 0 2px 0 #0d47a1 !important;
            transform: translateY(3px) !important;
        }

        /* BRUCIA / ELIMINA - Bordeaux */
        div.stButton > button[key="btn_cancella"] {
            background: #8e0000 !important;
            box-shadow: 0 5px 0 #4a0000, 0 8px 15px rgba(0,0,0,0.2) !important;
        }
        div.stButton > button[key="btn_cancella"]:active {
            box-shadow: 0 2px 0 #4a0000 !important;
            transform: translateY(3px) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- LOGICA DI CONNESSIONE E FUNZIONI ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1 style='text-align: center; color: #3e2723;'>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

        # Recupero opere dal database
        try:
            res = supabase.table("Opere").select("*").eq("autore_email", nome_poeta).order("creato_il", desc=True).execute()
            opere = res.data
        except:
            opere = []

        # Interfaccia di caricamento
        scelta = st.sidebar.selectbox("📖 Carica opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['contenuto'] if opera_corrente else ""
        v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

        # Campi input
        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
        with col_c:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        contenuto = st.text_area("Versi e Pensieri", value=v_testo, height=400)

        st.write("---")
        # Bottoni d'azione
        b1, b2, b3 = st.columns([1, 1, 1])

        with b1:
            if st.button("💾 Salva nel Diario", key="btn_salva"):
                if titolo:
                    dati = {"titolo": titolo, "contenuto": contenuto, "categoria": categoria, "autore_email": nome_poeta}
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati).execute()
                    st.success("Versi custoditi con cura.")
                    st.rerun()
                else:
                    st.warning("Un'opera ha bisogno di un titolo.")

        with b2:
            if st.button("🖨️ Stampa Foglio", key="btn_stampa"):
                st.markdown("<script>window.print();</script>", unsafe_allow_html=True)

        with b3:
            if opera_corrente:
                if st.button("🗑️ Brucia Opera", key="btn_cancella"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()
    else:
        st.warning("Identificati nella Home per accedere allo Scrittoio.")
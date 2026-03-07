import streamlit as st

def show():
    # Titolo principale con stile poetico
    st.markdown("<h1 class='poetic-title'>Benvenuto in Poeticamente 🖋️</h1>", unsafe_allow_html=True)
    
    # Spazio per separare dal titolo
    st.write("")
    
    # Layout a due colonne per rendere la home più elegante
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### La tua dimora per l'arte del verso
        
        Poeticamente è uno spazio dedicato a chi trasforma emozioni in rime. 
        Abbiamo rimosso l'accesso anonimo per creare una comunità di autori autentici e proteggere l'integrità delle opere.
        
        **Cosa puoi fare qui:**
        * **🖋️ Scrittoio Privato:** Componi le tue poesie con la sicurezza di un controllo automatico che garantisce un linguaggio decoroso, evitando sanzioni o contenuti impropri.
        * **📖 Bacheca Pubblica:** Condividi i tuoi versi con il mondo e leggi le opere degli altri poeti registrati.
        * **📜 Archivio Personale:** Gestisci le tue pubblicazioni sotto il tuo pseudonimo univoco.
        """)

    with col2:
        st.info("""
        **Regole della Community**
        
        1. **Registrazione:** È obbligatorio scegliere uno pseudonimo per pubblicare.
        2. **Rispetto:** Il sistema filtra automaticamente termini violenti o inappropriati.
        3. **Proprietà:** Ogni opera pubblicata resta legata al tuo profilo.
        """)

    st.divider()
    
    # Messaggio di stato per l'utente loggato
    if st.session_state.utente:
        st.success(f"Bentornato, **{st.session_state.utente}**. Il tuo calamaio è pronto nello Scrittoio.")
    else:
        st.warning("Per iniziare a scrivere, usa il modulo di accesso nella barra laterale.")

# Se il file viene eseguito da solo per test
if __name__ == "__main__":
    show()
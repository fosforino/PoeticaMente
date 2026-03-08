import streamlit as st

def show():
    # --- STILE LOCALE PER LA HOME ---
    st.markdown("""
    <style>
    .poetic-title-home { 
        font-family: 'Playfair Display', serif; 
        font-size: 3.5rem; 
        color: #4a3721; 
        text-align: center;
        margin-top: -20px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .home-subtitle {
        font-family: 'EB Garamond', serif;
        font-style: italic;
        font-size: 1.4rem;
        text-align: center;
        color: #8c6d46;
        margin-bottom: 30px;
    }
    .feature-box {
        background-color: #f4ece0;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #d4af37;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Titolo e Sottotitolo
    st.markdown("<h1 class='poetic-title-home'>Benvenuto in Poeticamente 🖋️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='home-subtitle'>La tua dimora per l'arte del verso</p>", unsafe_allow_html=True)
    
    # Layout a due colonne
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Poeticamente è uno spazio dedicato a chi trasforma emozioni in rime. 
        Abbiamo rimosso l'accesso anonimo per creare una comunità di autori autentici e proteggere l'integrità delle opere.
        
        **Cosa puoi fare qui:**
        """)
        
        st.markdown("""
        <div class='feature-box'>
        <strong>🖋️ Scrittoio Privato:</strong> Componi le tue poesie con la sicurezza di un controllo automatico che garantisce un linguaggio decoroso.
        </div>
        <div class='feature-box'>
        <strong>📖 Bacheca Pubblica:</strong> Condividi i tuoi versi con il mondo e leggi le opere degli altri poeti registrati.
        </div>
        <div class='feature-box'>
        <strong>📜 Archivio Personale:</strong> Gestisci le tue pubblicazioni sotto il tuo pseudonimo univoco.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.info("""
        **Regole della Community**
        
        1. **Registrazione:** È obbligatorio scegliere uno pseudonimo per pubblicare.
        2. **Rispetto:** Il sistema filtra termini inappropriati.
        3. **Proprietà:** Ogni opera pubblicata resta legata al tuo profilo.
        """)

    st.divider()
    
    # Messaggio di stato
    if st.session_state.get('utente'):
        st.success(f"Bentornato, **{st.session_state.utente}**. Il tuo calamaio è pronto nello Scrittoio.")
    else:
        st.warning("Per iniziare a scrivere, usa il modulo di accesso nella barra laterale.")

if __name__ == "__main__":
    show()
# pages/Premio.py
import streamlit as st
import random

def genera_vortice_lettere(num_lettere=120):
    """Genera l'HTML per il vortice di lettere casuali (Latine, Greche e Simboli)."""
    # Alfabeto misto per l'effetto "Big Bang della mente"
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZΩΨΦΣΠΛΔΓΘΞαβγδεζηθικλμνξοπρστυφχψω!?¿"
    html_lettere = '<div class="vortex-container">'
    
    for _ in range(num_lettere):
        char = random.choice(alfabeto)
        # Posizione casuale nello schermo (0-100% di larghezza e altezza)
        pos_x = random.uniform(0, 100)
        pos_y = random.uniform(0, 100)
        # Scegliamo casualmente se la lettera è piccola, media o grande (classi CSS)
        classe_dim = random.choice(['piccola', 'media', 'grande'])
        # Velocità dell'animazione casuale (tra 15 e 40 secondi per un giro)
        durata_anim = random.uniform(15, 40)

        html_lettere += f"""
            <div class="lettera-vortice {classe_dim}" 
                 style="left: {pos_x}vw; top: {pos_y}vh; animation-duration: {durata_anim}s;">
                {char}
            </div>
        """
    html_lettere += '</div>'
    return html_lettere

def show():
    # 1. INIETTIAMO IL VORTICE (Deve essere il primo per stare sullo sfondo)
    st.markdown(genera_vortice_lettere(), unsafe_allow_html=True)

    # 2. TITOLO (Sopra il vortice)
    st.markdown("<h1 class='titolo-id'>Il Tuo Riconoscimento</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 3. IL MEDAGLIONE 3D (Il centro gravitazionale)
    st.markdown("""
        <div class="medaglione-3d-container">
            <div class="card-3d">
                <div class="faccia fronte">
                    <img src="https://raw.githubusercontent.com/fosforino/Poeticamente/main/Poeticamente.png">
                </div>
                <div class="faccia retro-immagine">
                    <img src="https://raw.githubusercontent.com/fosforino/Poeticamente/main/Poeticamente_retro.png">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4. LA PERGAMENA DELLA DEDICA
    st.markdown("""
        <div class="pergamena-dedica">
            <p style="font-size: 1.3rem; line-height: 1.8; color: #5d4037;">
                <i>"A chi ha saputo trasformare il silenzio in inchiostro,<br>
                e il pensiero in un'opera senza tempo."</i>
            </p>
            <p style="font-size: 1.1rem; color: #795548; margin-top: 25px;">
                Un riconoscimento da parte di chi crede nel valore<br>
                <b>dell'Alchimia tra il Pensiero e il Verso.</b>
            </p>
            <div class="firma-fosforino">
                fosforino
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
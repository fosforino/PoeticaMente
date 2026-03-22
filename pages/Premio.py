# pages/Premio.py
import streamlit as st
import random

def genera_vortice_lettere(num_lettere=120):
    """Genera l'HTML per il vortice di lettere (Inchiostro dinamico)"""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZΩΨΦΣΠΛΔΓΘΞαβγδεζηθικλμνξοπρστυφχψω"
    html_lettere = '<div class="vortex-container">'
    for _ in range(num_lettere):
        char = random.choice(alfabeto)
        pos_x = random.uniform(0, 100)
        pos_y = random.uniform(0, 100)
        classe_dim = random.choice(['piccola', 'media', 'grande'])
        durata_anim = random.uniform(15, 35)

        html_lettere += f"""
            <div class="lettera-vortice {classe_dim}" 
                 style="left: {pos_x}vw; top: {pos_y}vh; animation-duration: {durata_anim}s;">
                {char}
            </div>
        """
    html_lettere += '</div>'
    return html_lettere

def show():
    # 1. INIETTIAMO IL VORTICE (Fluttua sopra il tuo fotomontaggio)
    st.markdown(genera_vortice_lettere(), unsafe_allow_html=True)

    # 2. TITOLO (Ora fluttua direttamente sulla carta del fotomontaggio)
    st.markdown("<h1 style='text-align: center;'>Il Tuo Riconoscimento</h1>", unsafe_allow_html=True)
    
    st.write("---")

    # 3. AREA TESTO (Semplice e pulita, la grafica è già nello sfondo)
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p style="font-size: 1.4rem; font-style: italic;">
                "A chi ha saputo trasformare il silenzio in inchiostro,<br>
                e il pensiero in un'opera senza tempo."
            </p>
            <p style="margin-top: 20px;">
                <b>L'Alchimia tra il Pensiero e il Verso.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
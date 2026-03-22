import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center; color: #3e2723; font-family: \"Playfair Display\";'>Il Tuo Riconoscimento</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- MOTORE 3D CON NOMI FILE ALLINEATI A GITHUB ---
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

    # --- PERGAMENA DEDICA ---
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
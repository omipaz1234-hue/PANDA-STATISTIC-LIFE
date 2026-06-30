import streamlit as st

def mostrar():

    st.container()

    col1, col2, col3 = st.columns([1.2, 3, 1.4])

    with col1:

        st.image("assets/panda.png", width=170)

    with col2:

        st.markdown("""
        # PANDA STATISTIC LIFE

        ### Plataforma Boliviana para el
        ### Análisis Estadístico y Epidemiológico
        """)

    with col3:

        st.image("assets/bolivia.png", width=180)

    st.divider()

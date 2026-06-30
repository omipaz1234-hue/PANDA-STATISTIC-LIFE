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
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.button("📊 Estadística", use_container_width=True)

with c2:
    st.button("🦠 Bioestadística", use_container_width=True)

with c3:
    st.button("👥 Demografía", use_container_width=True)

with c4:
    st.button("🛡 Vigilancia", use_container_width=True)

with c5:
    st.button("🗄 SNIS", use_container_width=True)

with c6:
    st.button("📈 Canal Endémico", use_container_width=True)

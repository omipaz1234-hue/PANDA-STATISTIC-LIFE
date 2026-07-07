import streamlit as st

def mostrar():

    # =====================================
    # CONFIGURACIÓN DE ESTILO
    # =====================================

    st.markdown("""
    <style>

    .titulo{
        text-align:center;
        font-size:55px;
        font-weight:bold;
        color:#1E3A8A;
        margin-bottom:5px;
    }

    .subtitulo{
        text-align:center;
        font-size:24px;
        color:#555555;
        margin-top:0px;
    }

    hr{
        margin-top:15px;
        margin-bottom:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # ENCABEZADO
    # =====================================

    col1, col2, col3 = st.columns([1.2, 4, 1.2])

    with col1:
        st.image("assets/Panda.png", width=170)

    with col2:

        st.markdown("""
        <div class="titulo">
        🐼 PANDA STATISTIC LIFE
        </div>

        <div class="subtitulo">
        Plataforma Boliviana de Estadística
        </div>

        <div class="subtitulo">
        y Vigilancia Epidemiológica
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.image("assets/bolivia.png", width=170)

    st.divider()

    # =====================================
    # MENÚ PRINCIPAL
    # =====================================

    st.subheader("📌 Módulos disponibles")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("📊 Estadística", use_container_width=True)
        st.button("👥 Demografía", use_container_width=True)

    with c2:
        st.button("🦠 Bioestadística", use_container_width=True)
        st.button("🛡 Vigilancia", use_container_width=True)

    with c3:
        st.button("🗄 SNIS", use_container_width=True)
        st.button("📈 Canal Endémico", use_container_width=True)

    st.divider()

    st.info(
        "Bienvenido a Panda Statistic Life. "
        "Seleccione un módulo para comenzar el análisis de datos estadísticos y epidemiológicos."
    )

import streamlit as st

def mostrar():

    # ============================
    # BANNER PRINCIPAL
    # ============================

    st.image("assets/banner.png", use_container_width=True)

    st.divider()

    # ============================
    # BOTONES PRINCIPALES
    # ============================

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

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================
    # MÉTRICAS
    # ============================

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric("Registros", "15,248")

    with m2:
        st.metric("Variables", "34")

    with m3:
        st.metric("Numéricas", "15")

    with m4:
        st.metric("Texto", "19")

    with m5:
        st.metric("Actualización", "2026")

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================
    # INFORMACIÓN
    # ============================

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📄 Información del archivo")

        st.info("""
Archivo cargado

**SNIS_SEMANA24.xlsx**

Estado:

✅ Datos cargados correctamente
        """)

    with c2:
        st.subheader("📊 Vista rápida")

        st.write("Primer registro: 01/01/2026")
        st.write("Último registro: 14/06/2026")
        st.write("Variables faltantes: 5")
        st.write("Duplicados: 0")
        st.write("Observaciones: 15,248")

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================
    # BIENVENIDA
    # ============================

    st.success(
        "🐼 Bienvenido a PANDA STATISTIC LIFE. Plataforma Boliviana para el análisis estadístico, bioestadístico y epidemiológico."
    )

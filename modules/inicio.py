import streamlit as st

def mostrar():

    st.markdown("""
    <div style="
        background: linear-gradient(90deg,#4F46E5,#6366F1,#93C5FD);
        padding:30px;
        border-radius:20px;
        color:white;
        box-shadow:0px 4px 15px rgba(0,0,0,0.15);
    ">
        <h1 style="font-size:48px;margin-bottom:5px;">
        🐼 PANDA STATISTIC LIFE
        </h1>

        <h3 style="margin-top:0;">
        Plataforma Boliviana de Estadística y Vigilancia Epidemiológica
        </h3>

        <p style="font-size:20px;">
        🇧🇴 Sistema Nacional de Información en Salud (SNIS)
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("📁 Registros", "0")

with c2:
    st.metric("📊 Variables", "0")

with c3:
    st.metric("🔢 Numéricas", "0")

with c4:
    st.metric("📝 Texto", "0")

with c5:
    st.metric("📅 Actualización", "--")
    st.divider()

izq, der = st.columns(2)

with izq:

    st.subheader("📄 Información del archivo")

    st.info("""
Archivo cargado:

Ninguno

Tamaño:

0 MB

Estado:

Esperando archivo...
""")

with der:

    st.subheader("📈 Resumen")

    st.success("""
✔ Plataforma lista

✔ Esperando datos

✔ Compatible con Excel

✔ Compatible con CSV
""")
    st.divider()

st.success("""
# 👋 Bienvenido a PANDA STATISTIC LIFE

Esta plataforma fue desarrollada para apoyar el análisis estadístico,
la bioestadística, la demografía y la vigilancia epidemiológica
del Sistema Nacional de Información en Salud (SNIS) de Bolivia.

Seleccione una opción del menú lateral para comenzar.
""")

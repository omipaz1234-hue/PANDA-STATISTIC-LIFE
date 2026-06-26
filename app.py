import streamlit as st

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="🐼 PANDA STATISTIC LIFE",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# ESTILOS CSS
# ==========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #0B5394;
    font-weight: 800;
}

h2 {
    color: #1B5E20;
}

h3 {
    color: #1565C0;
}

section[data-testid="stSidebar"]{
    background-color:#EAF4FF;
}

div.stButton > button{
    background-color:#1565C0;
    color:white;
    border-radius:10px;
    border:none;
    padding:0.5rem 1rem;
    font-weight:bold;
}

div.stButton > button:hover{
    background-color:#0D47A1;
}

div[data-testid="stMetric"]{
    background-color:white;
    border-radius:10px;
    padding:10px;
    border:1px solid #D9D9D9;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.title("🐼 PANDA STATISTIC LIFE")
st.subheader(
    "Plataforma de Estadística, Bioestadística, Epidemiología y Demografía"
)

st.markdown(
"""
Bienvenido a **PANDA STATISTIC LIFE**.

Esta plataforma está diseñada para apoyar el análisis de datos en:

- 📊 Estadística descriptiva
- 📈 Tablas de frecuencia
- 📉 Visualización de datos
- 🦠 Bioestadística
- 🏥 Indicadores de salud
- 👥 Demografía
- 📉 Canal endémico
- 🇧🇴 Importación de reportes SNIS
"""
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png",
    width=150
)

st.sidebar.title("🐼 MENÚ")

pagina = st.sidebar.radio(
    "Seleccione un módulo",
    [
        "🏠 Inicio",
        "📥 Importar datos",
        "📊 Estadística descriptiva",
        "📈 Tablas de frecuencia",
        "📉 Visualización",
        "🦠 Bioestadística",
        "🏥 Indicadores de salud",
        "👥 Demografía",
        "📉 Canal endémico",
        "📄 Exportar resultados",
        "ℹ️ Acerca de"
    ]
)

# ==========================================================
# PÁGINAS
# ==========================================================

if pagina == "🏠 Inicio":

    st.success("Bienvenido a PANDA STATISTIC LIFE")

    st.info(
        """
        Utiliza el menú lateral para acceder a los distintos módulos.

        Próximamente:
        - Importación automática de reportes SNIS.
        - Pirámides poblacionales.
        - Estadística inferencial.
        - Exportación de reportes.
        """
    )

elif pagina == "📥 Importar datos":

    st.header("📥 Importación de datos")

    archivo = st.file_uploader(
        "Seleccione un archivo",
        type=["xls", "xlsx", "csv"]
    )

    st.checkbox(
        "🇧🇴 Detectar automáticamente formato SNIS",
        value=True
    )

    st.checkbox(
        "Eliminar filas vacías",
        value=True
    )

    st.checkbox(
        "Eliminar columnas vacías",
        value=True
    )

    st.checkbox(
        "Conservar variables categóricas",
        value=True
    )

    if archivo is not None:
        st.success("Archivo cargado correctamente.")
        st.write("Nombre:", archivo.name)

elif pagina == "📊 Estadística descriptiva":

    st.header("📊 Estadística descriptiva")

    st.warning(
        "Este módulo se implementará en una siguiente versión."
    )

elif pagina == "📈 Tablas de frecuencia":

    st.header("📈 Tablas de frecuencia")

    st.warning(
        "Este módulo se implementará en una siguiente versión."
    )

elif pagina == "📉 Visualización":

    st.header("📉 Visualización")

    st.warning(
        "Este módulo se implementará en una siguiente versión."
    )

elif pagina == "🦠 Bioestadística":

    st.header("🦠 Bioestadística")

    st.write("Incluye cálculos como RR, OR y tablas 2×2.")

elif pagina == "🏥 Indicadores de salud":

    st.header("🏥 Indicadores de salud")

    st.write(
        "Incidencia, prevalencia, mortalidad y otros indicadores."
    )

elif pagina == "👥 Demografía":

    st.header("👥 Demografía")

    st.markdown("""
### Funcionalidades previstas

- Pirámide poblacional.
- Distribución por edad.
- Distribución por sexo.
- Razón de masculinidad.
- Índice de dependencia.
- Índice de envejecimiento.
- Indicadores demográficos.
""")

elif pagina == "📉 Canal endémico":

    st.header("📉 Canal endémico")

    st.write(
        "Visualización de zonas de seguridad, normalidad, alarma y epidemia."
    )

elif pagina == "📄 Exportar resultados":

    st.header("📄 Exportación")

    st.write(
        "Permite exportar tablas, gráficos e informes."
    )

elif pagina == "ℹ️ Acerca de":

    st.header("ℹ️ Acerca del proyecto")

    st.markdown("""
**PANDA STATISTIC LIFE**

Aplicación desarrollada para apoyar la enseñanza, investigación y análisis de datos en salud pública.

Incluye herramientas de:

- Estadística descriptiva.
- Bioestadística.
- Epidemiología.
- Demografía.
- Vigilancia epidemiológica.
- Procesamiento de datos del SNIS Bolivia.
""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "🐼 PANDA STATISTIC LIFE © 2026 | Desarrollado por Omar Paz"
)

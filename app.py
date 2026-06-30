import streamlit as st

# ============================
# CONFIGURACIÓN
# ============================

st.set_page_config(
    page_title="PANDA STATISTIC LIFE",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# IMPORTAR MÓDULOS
# ============================

from modules import importar
from modules import descriptiva
from modules import frecuencias
from modules import visualizacion
from modules import bioestadistica
from modules import indicadores
from modules import demografia
from modules import canal_endemico
from modules import exportar
# ============================
# CARGAR ESTILOS CSS
# ============================

def load_css():
    with open("styles/style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ============================
# CSS PERSONALIZADO
# ============================

st.markdown("""
<style>

/* Fondo */

.stApp{
    background-color:#F4F7FC;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#4F46E5,#6366F1);
}

/* Títulos Sidebar */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div{
    color:white;
}

/* Botones */

.stButton>button{
    background:#4F46E5;
    color:white;
    border-radius:10px;
    border:none;
}

.stButton>button:hover{

    background:#312E81;

}

/* Métricas */

div[data-testid="metric-container"]{

    background:white;

    border-radius:15px;

    padding:15px;

    box-shadow:0px 2px 10px rgba(0,0,0,0.1);

}

/* Dataframe */

[data-testid="stDataFrame"]{

    border-radius:10px;

}

</style>

""", unsafe_allow_html=True)

# ============================
# SIDEBAR
# ============================

with st.sidebar:

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png",
        width=120
    )

    st.title("🐼 PANDA")

    st.caption("STATISTIC LIFE")

    st.divider()

    menu = st.radio(

        "Menú Principal",

        [

            "🏠 Inicio",

            "📥 Importar Datos",

            "📊 Estadística Descriptiva",

            "📈 Frecuencias",

            "📉 Visualización",

            "🦠 Bioestadística",

            "🏥 Indicadores",

            "👥 Demografía",

            "📉 Canal Endémico",

            "📄 Exportar"

        ]

    )

    st.divider()

    st.success("🇧🇴 Bolivia")

    st.caption("Versión 1.0")

    st.caption("PANDA STATISTIC LIFE")

# ============================
# PÁGINAS
# ============================

if menu=="🏠 Inicio":

    st.title("🐼 PANDA STATISTIC LIFE")

    st.subheader("Plataforma Boliviana de Estadística y Vigilancia Epidemiológica")

    st.markdown("---")

    c1,c2,c3=st.columns(3)

    with c1:

        st.metric("Versión","1.0")

    with c2:

        st.metric("País","Bolivia")

    with c3:

        st.metric("Estado","Activo")

    st.markdown("---")

    st.info("""
Bienvenido a **PANDA STATISTIC LIFE**.

Esta plataforma está orientada al análisis estadístico y epidemiológico
para apoyar la toma de decisiones en Salud Pública de Bolivia.

Seleccione una opción del menú lateral para comenzar.
""")

elif menu=="📥 Importar Datos":

    importar.mostrar()

elif menu=="📊 Estadística Descriptiva":

    descriptiva.mostrar()

elif menu=="📈 Frecuencias":

    frecuencias.mostrar()

elif menu=="📉 Visualización":

    visualizacion.mostrar()

elif menu=="🦠 Bioestadística":

    bioestadistica.mostrar()

elif menu=="🏥 Indicadores":

    indicadores.mostrar()

elif menu=="👥 Demografía":

    demografia.mostrar()

elif menu=="📉 Canal Endémico":

    canal_endemico.mostrar()

elif menu=="📄 Exportar":

    exportar.mostrar()

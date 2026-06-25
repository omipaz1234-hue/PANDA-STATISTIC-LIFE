import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# CSS para mejor apariencia
st.markdown("""
<style>
    .main-header {font-size: 48px; color: #1E88E5; text-align: center; font-weight: bold;}
    .sub-header {font-size: 22px; color: #424242; text-align: center;}
</style>
""", unsafe_allow_html=True)

# Header bonito con logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png", width=140)
with col2:
    st.markdown('<h1 class="main-header">🐼 PANDA STATISTIC LIFE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Estadística Descriptiva y Bioestadística para Salud Pública - Bolivia</p>', unsafe_allow_html=True)

st.markdown("**Basado en el libro de Bayarre, Hersford y Oliva**")

# Sidebar
with st.sidebar:
    st.header("📁 Cargar Datos SNIS")
    uploaded_file = st.file_uploader("Sube tu archivo CSV o Excel del SNIS", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Limpieza fuerte
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
            
            st.success(f"✅ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.dataframe(df.head(10), use_container_width=True)
            st.session_state.df = df
        except:
            st.error("Error al leer el archivo")
    else:
        if st.button("Usar Datos de Ejemplo"):
            df = pd.DataFrame({
                'Semana': range(1,53),
                'Casos': [5,8,12,15,22,28,35,42,38,45,52,48,55,60,58,65,72,80,75,68,55,48,42,38,35,32,28,25,22,20,18,15,12,10,8,7,6,5,4,3,4,5,6,8,10,12,15,18,22,25,20,15]
            })
            st.session_state.df = df
            st.success("Datos de ejemplo cargados")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"])

df = st.session_state.get('df', None)

# TAB DESCRIPTIVA
with tab1:
    st.header("1. Estadística Descriptiva")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Selecciona columna", numeric_cols)
            data = df[col].dropna()
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Media", f"{data.mean():.2f}")
                st.metric("Mediana", f"{data.median():.2f}")
            with c2:
                st.metric("Desv. Estándar", f"{data.std():.2f}")
                st.metric("Coef. Variación", f"{(data.std()/data.mean()*100):.1f}%")
            fig = px.box(df, y=col, title=f"Diagrama de Caja - {col}")
            st.plotly_chart(fig, use_container_width=True)

# CANAL ENDÉMICO (con zonas de colores)
with tab6:
    st.header("📉 Canal Endémico")
    if df is not None and len(df) > 5:
        caso_col = 'Casos'
        if caso_col not in df.columns:
            for col in df.columns:
                if 'caso' in str(col).lower():
                    caso_col = col
                    break
        casos = df[caso_col].dropna()
        media = casos.mean()
        de = casos.std()
        
        fig = go.Figure()
        fig.add_hrect(0, max(0,media-de), fillcolor="green", opacity=0.2, annotation_text="🟢 ÉXITO / SEGURIDAD")
        fig.add_hrect(max(0,media-de), media+de, fillcolor="blue", opacity=0.15, annotation_text="🔵 NORMAL")
        fig.add_hrect(media+de, media+2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ALARMA")
        fig.add_hrect(media+2*de, casos.max()*1.2, fillcolor="red", opacity=0.25, annotation_text="🔴 EPIDEMIA")
        
        fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
        
        fig.update_layout(title="Canal Endémico con Zonas de Color", height=650)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Carga datos para ver el Canal Endémico")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Bolivia")

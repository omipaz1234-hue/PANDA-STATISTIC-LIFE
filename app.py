import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# ==================== HEADER ====================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png", width=140)
with col2:
    st.markdown("# 🐼 PANDA STATISTIC LIFE")
    st.markdown("### Estadística Descriptiva y Bioestadística para Salud Pública en Bolivia")

st.caption("Basado en el libro de Bayarre, Hersford y Oliva")

# ==================== CARGAR DATOS ====================
with st.sidebar:
    st.header("📁 Cargar Datos SNIS")
    uploaded_file = st.file_uploader("Sube CSV o Excel del SNIS", type=["csv", "xlsx", "xls"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Limpieza fuerte para SNIS
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
            
            st.success(f"✅ Cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.session_state.df = df
            st.dataframe(df.head(8), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("📊 Usar Datos de Ejemplo"):
        df = pd.DataFrame({
            'Semana': range(1, 53),
            'Casos': [5,8,12,15,22,28,35,42,38,45,52,48,55,60,58,65,72,80,75,68,55,48,42,38,35,32,28,25,22,20,18,15,12,10,8,7,6,5,4,3,4,5,6,8,10,12,15,18,22,25,20,15]
        })
        st.session_state.df = df
        st.success("Datos de ejemplo cargados")

# ==================== TABS ====================
df = st.session_state.get('df', None)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", 
    "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"
])

# ==================== TAB 1 - DESCRIPTIVA ====================
with tab1:
    st.header("1. Estadística Descriptiva")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Selecciona una columna numérica", numeric_cols)
            data = df[col].dropna()
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Media", f"{data.mean():.2f}")
                st.metric("Mediana", f"{data.median():.2f}")
            with c2:
                st.metric("Desv. Estándar", f"{data.std():.2f}")
                st.metric("Coef. Variación", f"{(data.std()/data.mean()*100 if data.mean() != 0 else 0):.1f}%")
            
            fig = go.Figure()
            fig.add_trace(go.Box(y=data, name=col))
            fig.update_layout(title=f"Diagrama de Caja - {col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay columnas numéricas")
    else:
        st.info("Carga un archivo para empezar")

# ==================== CANAL ENDÉMICO (TAB 6) ====================
with tab6:
    st.header("📉 Canal Endémico")
    if df is not None:
        # Buscar columna de casos automáticamente
        caso_col = None
        for col in df.columns:
            if any(x in str(col).lower() for x in ['caso', 'enfermo', 'positivo', 'report', 'incid']):
                caso_col = col
                break
        if not caso_col and len(df.select_dtypes(include=np.number).columns) > 0:
            caso_col = df.select_dtypes(include=np.number).columns[0]
        
        if caso_col:
            casos = df[caso_col].dropna()
            media = casos.mean()
            de = casos.std()
            
            st.success(f"Usando columna: **{caso_col}** | Media = {media:.2f} | DE = {de:.2f}")
            
            fig = go.Figure()
            
            # Zonas de color
            fig.add_hrect(0, max(0, media-de), fillcolor="green", opacity=0.2, annotation_text="🟢 ÉXITO / SEGURIDAD")
            fig.add_hrect(max(0, media-de), media+de, fillcolor="lightblue", opacity=0.2, annotation_text="🔵 NORMAL")
            fig.add_hrect(media+de, media+2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ALARMA")
            fig.add_hrect(media+2*de, casos.max()*1.2, fillcolor="red", opacity=0.25, annotation_text="🔴 EPIDEMIA")
            
            fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos', line=dict(color='#1E88E5', width=3)))
            fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
            
            fig.update_layout(title="Canal Endémico - Vigilancia Epidemiológica Bolivia", height=650)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No se encontró columna numérica")
    else:
        st.info("Carga tu archivo del SNIS")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Bolivia")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# ==================== HEADER CON LOGO ====================
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png", width=180)
with col2:
    st.markdown("# 🐼 PANDA STATISTIC LIFE")
    st.markdown("### Estadística Descriptiva y Bioestadística para Salud Pública - Bolivia")
    st.caption("Basado en el libro de Bayarre, Hersford y Oliva")

# Sidebar
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
            
            st.success(f"✅ Cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.session_state.df = df
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("📊 Usar Datos de Ejemplo"):
        df = pd.DataFrame({
            'Semana': range(1, 53),
            'Casos': [5,8,12,15,22,28,35,42,38,45,52,48,55,60,58,65,72,80,75,68,55,48,42,38,35,32,28,25,22,20,18,15,12,10,8,7,6,5,4,3,4,5,6,8,10,12,15,18,22,25,20,15]
        })
        st.session_state.df = df
        st.success("Datos de ejemplo (Dengue) cargados")

df = st.session_state.get('df', None)

# Tabs
tabs = st.tabs(["📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"])

# ==================== CANAL ENDÉMICO CON ZONAS DE COLOR ====================
with tabs[5]:
    st.header("📉 Canal Endémico")
    
    if df is not None:
        # Buscar columna de casos
        caso_col = next((col for col in df.columns if 'caso' in str(col).lower() or 'enfermo' in str(col).lower()), None)
        if not caso_col and 'Casos' in df.columns:
            caso_col = 'Casos'
        
        if caso_col:
            casos = df[caso_col].dropna()
            media = casos.mean()
            de = casos.std()
            
            st.write(f"**Media**: {media:.2f} | **Desv. Estándar**: {de:.2f}")
            
            fig = go.Figure()
            
            # Zonas de color con hrect
            fig.add_hrect(y0=0, y1=max(0, media - de), fillcolor="green", opacity=0.18, annotation_text="🟢 ZONA DE ÉXITO / SEGURIDAD")
            fig.add_hrect(y0=max(0, media - de), y1=media + de, fillcolor="lightblue", opacity=0.2, annotation_text="🔵 ZONA NORMAL")
            fig.add_hrect(y0=media + de, y1=media + 2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ZONA DE ALARMA")
            fig.add_hrect(y0=media + 2*de, y1=casos.max()*1.15, fillcolor="red", opacity=0.25, annotation_text="🔴 ZONA DE EPIDEMIA")
            
            fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos Observados', line=dict(color='#1E88E5', width=3)))
            fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
            
            fig.update_layout(
                title="Canal Endémico - Vigilancia Epidemiológica Bolivia",
                xaxis_title="Semana / Período",
                yaxis_title="Número de Casos",
                height=650,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de alertas
            def estado(x):
                if x >= media + 2*de: return "🔴 EPIDEMIA"
                elif x >= media + de: return "🟠 ALARMA"
                elif x <= media - de: return "🟢 SEGURIDAD"
                else: return "🔵 NORMAL"
            
            df['Estado'] = df[caso_col].apply(estado)
            st.dataframe(df[['Semana' if 'Semana' in df.columns else df.columns[0], caso_col, 'Estado']], use_container_width=True)
        else:
            st.warning("No se encontró columna de 'Casos'. Renómbrala como 'Casos'.")
    else:
        st.info("Carga tus datos SNIS para ver el Canal Endémico")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Herramienta para SEDES Bolivia")

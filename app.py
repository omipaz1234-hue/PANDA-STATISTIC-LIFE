import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# Header con estilo
st.markdown("""
<style>
    .main-header {font-size: 42px; color: #1E88E5; text-align: center;}
    .sub-header {font-size: 24px; color: #424242;}
</style>
""", unsafe_allow_html=True)

st.title("🐼 PANDA STATISTIC LIFE")
st.subheader("Estadística Descriptiva y Bioestadística para Salud Pública - Bolivia")
st.markdown("**Basado en el libro de Bayarre, Hersford y Oliva** | Herramienta para SEDES y Unidades de Salud")

# Sidebar
with st.sidebar:
    st.header("📁 Cargar Datos SNIS")
    uploaded_file = st.file_uploader("Sube tu archivo CSV o Excel del SNIS", 
                                   type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Limpieza automática fuerte para SNIS
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
            
            st.success(f"✅ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.dataframe(df.head(8), use_container_width=True)
        except Exception as e:
            st.error(f"Error al leer archivo: {e}")
            df = None
    else:
        if st.button("📊 Usar Datos de Ejemplo (Dengue Semanal)"):
            dates = pd.date_range(start='2024-01-01', periods=52, freq='W')
            df = pd.DataFrame({
                'Semana': range(1, 53),
                'Fecha': dates,
                'Casos': [5,8,12,15,22,28,35,42,38,45,52,48,55,60,58,65,72,80,75,68,55,48,42,38,35,32,28,25,22,20,18,15,12,10,8,7,6,5,4,3,4,5,6,8,10,12,15,18,22,25,20,15]
            })
            st.success("Datos de ejemplo cargados")

# Tabs con colores
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", 
    "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"
])

# ==================== CANAL ENDÉMICO MEJORADO ====================
with tab6:
    st.header("📉 Canal Endémico")
    st.markdown("**Cálculo automático con zonas de colores**")
    
    if 'df' in locals() and df is not None and 'Casos' in df.columns:
        casos = df['Casos'].dropna()
        media = casos.mean()
        de = casos.std()
        
        st.write(f"**Media Histórica**: {media:.2f} | **Desviación Estándar**: {de:.2f}")
        
        # Crear bandas
        df['Media'] = media
        df['Zona_Seguridad_Inf'] = max(0, media - de)
        df['Zona_Alarma_Sup'] = media + de
        df['Zona_Epidemia'] = media + 2 * de
        
        # Gráfico con zonas de colores
        fig = go.Figure()
        
        # Zonas de color
        fig.add_hrect(y0=0, y1=media- de, fillcolor="green", opacity=0.15, line_width=0, annotation_text="ZONA DE ÉXITO / SEGURIDAD", annotation_position="top left")
        fig.add_hrect(y0=media-de, y1=media+de, fillcolor="lightblue", opacity=0.2, line_width=0, annotation_text="ZONA NORMAL")
        fig.add_hrect(y0=media+de, y1=media+2*de, fillcolor="orange", opacity=0.25, line_width=0, annotation_text="ZONA DE ALARMA")
        fig.add_hrect(y0=media+2*de, y1=casos.max()*1.1, fillcolor="red", opacity=0.25, line_width=0, annotation_text="ZONA DE EPIDEMIA")
        
        # Líneas principales
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Casos'], mode='lines+markers', name='Casos Observados', line=dict(color='#1E88E5', width=3)))
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Media'], mode='lines', name='Media', line=dict(color='black', dash='dash')))
        
        fig.update_layout(
            title="Canal Endémico - Vigilancia Epidemiológica Bolivia",
            xaxis_title="Semana Epidemiológica",
            yaxis_title="Número de Casos",
            height=650,
            template="plotly_white",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de clasificación
        def clasificar(x):
            if x >= media + 2*de: return "🔴 EPIDEMIA"
            elif x >= media + de: return "🟠 ALARMA"
            elif x <= media - de: return "🟢 SEGURIDAD"
            else: return "🔵 NORMAL"
        
        df['Estado'] = df['Casos'].apply(clasificar)
        st.dataframe(df[['Semana', 'Casos', 'Estado']], use_container_width=True)
        
        # Descargar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Resultados", csv, "canal_endemico.csv", "text/csv")
    else:
        st.info("Carga tus datos o usa los datos de ejemplo para ver el Canal Endémico con zonas de colores.")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Desarrollado para fortalecer la vigilancia en salud de Bolivia")

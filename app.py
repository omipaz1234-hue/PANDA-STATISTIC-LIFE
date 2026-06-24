import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

st.title("🐼 PANDA STATISTIC LIFE")
st.subheader("Estadística Descriptiva y Bioestadística para Salud - Bolivia")
st.markdown("**Basado en el libro de Bayarre et al.** | Herramienta para Vigilancia en Salud")

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
            st.success(f"✅ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        except:
            st.error("Error al leer el archivo")
            df = None
    else:
        st.info("Carga un archivo para comenzar")
        # Datos de ejemplo
        if st.button("Usar Datos de Ejemplo (Dengue)"):
            dates = pd.date_range(start='2024-01-01', periods=52, freq='W')
            df = pd.DataFrame({
                'Semana': range(1, 53),
                'Fecha': dates,
                'Casos': [5, 8, 12, 15, 22, 28, 35, 42, 38, 45, 52, 48, 55, 60, 58, 65, 72, 80, 75, 68, 55, 48, 42, 38, 35, 32, 28, 25, 22, 20, 18, 15, 12, 10, 8, 7, 6, 5, 4, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 25, 20, 15]
            })
            st.success("Datos de ejemplo cargados (Dengue semanal)")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", 
    "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"
])

with tab1:
    st.header("1. Estadística Descriptiva")
    if 'df' in locals() and df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns
        col = st.selectbox("Selecciona columna numérica", numeric_cols)
        
        if col:
            st.write(f"**Media**: {df[col].mean():.2f}")
            st.write(f"**Mediana**: {df[col].median():.2f}")
            st.write(f"**Moda**: {df[col].mode()[0] if not df[col].mode().empty else 'N/A'}")
            st.write(f"**Desviación Estándar**: {df[col].std():.2f}")
            st.write(f"**Varianza**: {df[col].var():.2f}")
            st.write(f"**Coeficiente de Variación**: {(df[col].std()/df[col].mean()*100):.2f}%")
            
            fig = px.box(df, y=col, title=f"Diagrama de Caja - {col}")
            st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.header("6. Canal Endémico")
    st.markdown("**Cálculo automático según método clásico (media ± DE)**")
    
    if 'df' in locals() and df is not None and 'Casos' in df.columns:
        casos = df['Casos']
        media = casos.mean()
        de = casos.std()
        
        st.write(f"**Media histórica**: {media:.2f}")
        st.write(f"**Desviación Estándar**: {de:.2f}")
        
        # Bandas
        df['Media'] = media
        df['Limite_Superior_1'] = media + de
        df['Limite_Inferior_1'] = max(0, media - de)
        df['Limite_Superior_2'] = media + 2*de
        df['Limite_Inferior_2'] = max(0, media - 2*de)
        
        # Clasificación
        def clasificar(x):
            if x > media + 2*de:
                return "Epidemia (Alerta Roja)"
            elif x > media + de:
                return "Zona de Alarma (Naranja)"
            elif x < media - de:
                return "Zona de Seguridad (Verde)"
            else:
                return "Normal"
        
        df['Estado'] = df['Casos'].apply(clasificar)
        
        # Gráfico Canal Endémico
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Casos'], mode='lines+markers', name='Casos Observados', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Media'], mode='lines', name='Media', line=dict(color='black', dash='dash')))
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Limite_Superior_2'], mode='lines', name='+2DE', line=dict(color='red', dash='dot')))
        fig.add_trace(go.Scatter(x=df['Semana'], y=df['Limite_Inferior_2'], mode='lines', name='-2DE', line=dict(color='red', dash='dot')))
        
        fig.update_layout(title="Canal Endémico - Vigilancia Epidemiológica", 
                         xaxis_title="Semana Epidemiológica",
                         yaxis_title="Número de Casos",
                         height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df[['Semana', 'Casos', 'Estado']], use_container_width=True)
        
        # Exportar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Resultados CSV", csv, "canal_endemico.csv", "text/csv")
    else:
        st.info("Carga datos o usa los datos de ejemplo para ver el Canal Endémico")

st.caption("PANDA STATISTIC LIFE © 2026 - Herramienta educativa y de apoyo para salud pública en Bolivia")

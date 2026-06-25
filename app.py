import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png", width=160)
with col2:
    st.markdown("# 🐼 PANDA STATISTIC LIFE")
    st.markdown("### Estadística y Vigilancia en Salud - Bolivia")

st.caption("Optimizado para reportes del SNIS - Ministerio de Salud")

# ==================== CARGAR DATOS ====================
with st.sidebar:
    st.header("📁 Cargar Reporte SNIS")
    uploaded_file = st.file_uploader("Sube tu archivo Excel del SNIS", type=["xlsx", "xls"])
    
    if uploaded_file:
        try:
            # Lectura especial para archivos sucios del SNIS
            df = pd.read_excel(uploaded_file, header=None)
            
            # Buscar la fila donde empiezan los datos reales
            for i in range(min(20, len(df))):
                row = df.iloc[i].astype(str).str.lower()
                if row.str.contains('total_gral|tot_pri_varones|la paz', case=False, na=False).any():
                    start_row = i + 1
                    break
            else:
                start_row = 5  # fallback
            
            # Leer desde esa fila
            df_clean = pd.read_excel(uploaded_file, header=None, skiprows=start_row)
            
            # Limpiar columnas vacías
            df_clean = df_clean.dropna(axis=1, how='all')
            df_clean = df_clean.dropna(axis=0, how='all')
            
            # Renombrar columnas numéricas
            numeric_cols = df_clean.select_dtypes(include=np.number).columns
            for col in numeric_cols:
                df_clean = df_clean.rename(columns={col: f"Valor_{col}"})
            
            st.success(f"✅ Archivo SNIS procesado: {df_clean.shape[0]} filas, {df_clean.shape[1]} columnas")
            st.dataframe(df_clean.head(10), use_container_width=True)
            st.session_state.df = df_clean
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("📊 Usar Datos de Ejemplo"):
        df = pd.DataFrame({
            'Grupo_Edad': ['<6m', '6m-1a', '1-4a', '5-9a'],
            'Casos': [8312, 4351, 14802, 13004]
        })
        st.session_state.df = df
        st.success("Datos de ejemplo cargados")

df = st.session_state.get('df', None)

# Tabs
tab1, tab2, tab6 = st.tabs(["📊 Descriptiva", "📈 Frecuencias", "📉 Canal Endémico"])

# ==================== DESCRIPTIVA ====================
with tab1:
    st.header("1. Estadística Descriptiva")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Selecciona columna numérica", numeric_cols)
            data = df[col].dropna()
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Media", f"{data.mean():.2f}")
                st.metric("Mediana", f"{data.median():.2f}")
            with c2:
                st.metric("Desv. Estándar", f"{data.std():.2f}")
                st.metric("Mínimo", f"{data.min():.2f}")
            with c3:
                st.metric("Máximo", f"{data.max():.2f}")
                st.metric("Coef. Variación", f"{(data.std()/data.mean()*100 if data.mean() != 0 else 0):.1f}%")
            
            fig = go.Figure(data=[go.Box(y=data, name=col)])
            fig.update_layout(title=f"Diagrama de Caja - {col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontraron columnas numéricas. Revisa tu archivo.")

# ==================== CANAL ENDÉMICO ====================
with tab6:
    st.header("📉 Canal Endémico")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            caso_col = st.selectbox("Selecciona la columna de casos/enfermos", numeric_cols)
            casos = df[caso_col].dropna()
            media = casos.mean()
            de = casos.std()
            
            st.success(f"Columna usada: **{caso_col}** | Media: {media:.2f} | DE: {de:.2f}")
            
            fig = go.Figure()
            
            fig.add_hrect(y0=0, y1=max(0, media-de), fillcolor="green", opacity=0.2, annotation_text="🟢 ÉXITO / SEGURIDAD")
            fig.add_hrect(y0=max(0, media-de), y1=media+de, fillcolor="lightblue", opacity=0.2, annotation_text="🔵 NORMAL")
            fig.add_hrect(y0=media+de, y1=media+2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ALARMA")
            fig.add_hrect(y0=media+2*de, y1=casos.max()*1.15, fillcolor="red", opacity=0.25, annotation_text="🔴 EPIDEMIA")
            
            fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos', line=dict(color='#1E88E5', width=3)))
            fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
            
            fig.update_layout(title="Canal Endémico - SNIS Bolivia", height=650)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Carga tu archivo SNIS")
    else:
        st.info("Sube tu reporte del SNIS")

st.caption("🐼 PANDA STATISTIC LIFE - Optimizado para reportes reales del SNIS")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# ==================== HEADER ====================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Panda_Logo.svg/512px-Panda_Logo.svg.png", width=160)
with col2:
    st.markdown("# 🐼 PANDA STATISTIC LIFE")
    st.markdown("### Estadística Descriptiva y Bioestadística para Salud Pública - Bolivia")
    st.caption("Optimizado para reportes del SNIS - Ministerio de Salud")

# ==================== CARGA DE DATOS ====================
with st.sidebar:
    st.header("📁 Cargar Reporte SNIS")
    uploaded_file = st.file_uploader("Sube tu archivo Excel del SNIS", type=["xlsx", "xls", "csv"])
    
    if uploaded_file:
        try:
            # Lectura especial para archivos sucios del SNIS
            df_raw = pd.read_excel(uploaded_file, header=None)
            
            # Buscar fila de inicio de datos
            start_row = 0
            for i in range(min(30, len(df_raw))):
                if df_raw.iloc[i].astype(str).str.contains('TOTAL_GRAL|LA PAZ|SEDES', case=False, na=False).any():
                    start_row = i
                    break
            
            df = pd.read_excel(uploaded_file, skiprows=start_row)
            df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
            
            # Convertir columnas a numéricas
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
            
            st.success(f"✅ Datos SNIS cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.dataframe(df.head(10), use_container_width=True)
            st.session_state.df = df
        except Exception as e:
            st.error(f"Error al leer archivo: {e}")

    if st.button("📊 Usar Datos de Ejemplo"):
        df = pd.DataFrame({
            'Grupo_Edad': ['<6m', '6m-1a', '1-4a', '5-9a', '10-14a', '15-19a'],
            'Casos': [8312, 4351, 14802, 13004, 11262, 11040]
        })
        st.session_state.df = df
        st.success("Datos de ejemplo cargados")

df = st.session_state.get('df', None)

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", 
    "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"
])

# ====================== 1. DESCRIPTIVA ======================
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
            
            fig = px.box(df, y=col, title=f"Diagrama de Caja - {col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontraron columnas numéricas")
    else:
        st.info("Carga tu archivo SNIS")

# ====================== 2. FRECUENCIAS ======================
with tab2:
    st.header("2. Tablas de Frecuencia")
    if df is not None:
        col = st.selectbox("Selecciona una columna", df.columns, key="freq_tab")
        freq = df[col].value_counts().reset_index()
        freq.columns = ['Valor', 'Frecuencia Absoluta']
        freq['Frecuencia Relativa (%)'] = (freq['Frecuencia Absoluta'] / freq['Frecuencia Absoluta'].sum() * 100).round(2)
        st.dataframe(freq, use_container_width=True)

# ====================== 3. VISUALIZACIÓN ======================
with tab3:
    st.header("3. Visualización de Datos")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col_x = st.selectbox("Variable categórica (X)", df.columns, key="viz_x")
            col_y = st.selectbox("Variable numérica (Y)", numeric_cols, key="viz_y")
            
            fig1 = px.bar(df, x=col_x, y=col_y, title=f"{col_y} por {col_x}")
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.pie(df, names=col_x, values=col_y, title="Gráfico Circular")
            st.plotly_chart(fig2, use_container_width=True)

# ====================== 4. BIOESTADÍSTICA ======================
with tab4:
    st.header("4. Bioestadística y Epidemiología")
    st.subheader("Tabla 2×2 y Medidas de Asociación")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a = Enfermo + Expuesto", value=45, min_value=0)
        c = st.number_input("c = Enfermo + No Expuesto", value=25, min_value=0)
    with col2:
        b = st.number_input("b = Sano + Expuesto", value=120, min_value=0)
        d = st.number_input("d = Sano + No Expuesto", value=210, min_value=0)
    
    if st.button("Calcular RR y OR"):
        rr = (a / (a + b)) / (c / (c + d)) if (c + d) > 0 else 0
        or_val = (a * d) / (b * c) if (b * c) > 0 else 0
        
        st.success("**Resultados**")
        st.metric("Riesgo Relativo (RR)", f"{rr:.2f}")
        st.metric("Odds Ratio (OR)", f"{or_val:.2f}")
        
        tabla = pd.DataFrame([[a, b], [c, d]], 
                           index=["Enfermo", "No Enfermo"], 
                           columns=["Expuesto", "No Expuesto"])
        st.dataframe(tabla)

# ====================== 5. INDICADORES ======================
with tab5:
    st.header("5. Indicadores de Salud")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col_casos = st.selectbox("Columna de Casos", numeric_cols, key="ind_casos")
            poblacion = st.number_input("Población total", value=1000000, min_value=1000)
            
            casos_total = df[col_casos].sum()
            
            incidencia = (casos_total / poblacion) * 100000
            prevalencia = (casos_total / poblacion) * 100
            
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Incidencia (x 100,000 hab)", f"{incidencia:.2f}")
            with c2: st.metric("Prevalencia (%)", f"{prevalencia:.2f}")
            with c3: st.metric("Total Casos", int(casos_total))
    else:
        st.info("Carga datos para calcular indicadores")

# ====================== 6. CANAL ENDÉMICO ======================
with tab6:
    st.header("6. Canal Endémico")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            caso_col = st.selectbox("Selecciona columna de Casos", numeric_cols, key="canal_col")
            casos = df[caso_col].dropna()
            media = casos.mean()
            de = casos.std()
            
            st.success(f"**Columna usada:** {caso_col} | Media: {media:.2f} | DE: {de:.2f}")
            
            fig = go.Figure()
            fig.add_hrect(0, max(0, media-de), fillcolor="green", opacity=0.2, annotation_text="🟢 ÉXITO / SEGURIDAD")
            fig.add_hrect(max(0, media-de), media+de, fillcolor="lightblue", opacity=0.2, annotation_text="🔵 NORMAL")
            fig.add_hrect(media+de, media+2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ALARMA")
            fig.add_hrect(media+2*de, casos.max()*1.2, fillcolor="red", opacity=0.25, annotation_text="🔴 EPIDEMIA")
            
            fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos', line=dict(color='#1E88E5', width=3)))
            fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
            
            fig.update_layout(title="Canal Endémico - Vigilancia SNIS Bolivia", height=650)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay columnas numéricas")
    else:
        st.info("Carga tu archivo SNIS")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Desarrollado para Bolivia")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="PANDA STATISTIC LIFE", page_icon="🐼", layout="wide")

# Header
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
            df = pd.read_excel(uploaded_file, header=None)
            start_row = 0
            for i in range(min(30, len(df))):
                if df.iloc[i].astype(str).str.contains('TOTAL_GRAL|LA PAZ', case=False, na=False).any():
                    start_row = i
                    break
            df = pd.read_excel(uploaded_file, skiprows=start_row)
            df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
            
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
            
            st.success(f"✅ Datos SNIS cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.dataframe(df.head(8), use_container_width=True)
            st.session_state.df = df
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

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Descriptiva", "📈 Frecuencias", "📉 Visualización", 
    "🦠 Bioestadística", "🏥 Indicadores", "📉 Canal Endémico"
])

# ====================== BIOESTADÍSTICA ======================
with tab4:
    st.header("4. Bioestadística y Epidemiología")
    st.subheader("Tabla 2x2 y Medidas de Asociación")
    
    if df is not None:
        st.info("Ingresa manualmente los valores para Tabla 2x2 (ejemplo: Enfermedad vs Exposición)")
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("a (Enfermo + Expuesto)", value=50)
            c = st.number_input("c (Enfermo + No expuesto)", value=30)
        with col2:
            b = st.number_input("b (Sano + Expuesto)", value=100)
            d = st.number_input("d (Sano + No expuesto)", value=200)
        
        if st.button("Calcular Medidas"):
            total = a + b + c + d
            rr = (a/(a+b)) / (c/(c+d)) if (c+d) > 0 else 0
            or_val = (a*d) / (b*c) if (b*c) > 0 else 0
            
            st.write("**Resultados:**")
            st.metric("Riesgo Relativo (RR)", f"{rr:.2f}")
            st.metric("Odds Ratio (OR)", f"{or_val:.2f}")
            
            tabla = pd.DataFrame([[a,b],[c,d]], index=["Enfermo", "Sano"], columns=["Expuesto", "No Expuesto"])
            st.dataframe(tabla)
    else:
        st.info("Carga datos o usa el ejemplo")

# ====================== INDICADORES DE SALUD ======================
with tab5:
    st.header("5. Indicadores de Salud")
    st.subheader("Cálculo de Indicadores Básicos")
    
    if df is not None and len(df) > 0:
        col_casos = st.selectbox("Columna de Casos/Nuevos", df.select_dtypes(include=np.number).columns, key="ind1")
        poblacion = st.number_input("Población total (ejemplo: 1000000)", value=1000000)
        
        casos_total = df[col_casos].sum()
        
        incidencia = (casos_total / poblacion) * 100000
        prevalencia = (casos_total / poblacion) * 100
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Incidencia (por 100,000 hab.)", f"{incidencia:.2f}")
        with c2:
            st.metric("Prevalencia (%)", f"{prevalencia:.2f}")
        with c3:
            st.metric("Casos Totales", f"{int(casos_total)}")
    else:
        st.info("Carga tu archivo SNIS para calcular indicadores")

# ====================== CANAL ENDÉMICO ======================
with tab6:
    st.header("6. Canal Endémico")
    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            caso_col = st.selectbox("Selecciona columna de Casos", numeric_cols, key="canal")
            casos = df[caso_col].dropna()
            media = casos.mean()
            de = casos.std()
            
            fig = go.Figure()
            fig.add_hrect(0, max(0,media-de), fillcolor="green", opacity=0.2, annotation_text="🟢 ÉXITO/SEGURIDAD")
            fig.add_hrect(max(0,media-de), media+de, fillcolor="lightblue", opacity=0.2, annotation_text="🔵 NORMAL")
            fig.add_hrect(media+de, media+2*de, fillcolor="orange", opacity=0.25, annotation_text="🟠 ALARMA")
            fig.add_hrect(media+2*de, casos.max()*1.2, fillcolor="red", opacity=0.25, annotation_text="🔴 EPIDEMIA")
            
            fig.add_trace(go.Scatter(x=df.index, y=casos, mode='lines+markers', name='Casos', line=dict(color='#1E88E5', width=3)))
            fig.add_trace(go.Scatter(x=df.index, y=[media]*len(df), mode='lines', name='Media', line=dict(color='black', dash='dash')))
            
            fig.update_layout(title="Canal Endémico", height=650)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Carga datos")

st.caption("🐼 PANDA STATISTIC LIFE © 2026 - Bolivia")

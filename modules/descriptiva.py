import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =====================================================
# CÁLCULO DE ESTADÍSTICAS
# =====================================================

def calcular_estadisticas(datos):

    estadisticas = {}

    estadisticas["Media"] = datos.mean()

    estadisticas["Mediana"] = datos.median()

    moda = datos.mode()

    estadisticas["Moda"] = moda.iloc[0] if not moda.empty else np.nan

    estadisticas["Mínimo"] = datos.min()

    estadisticas["Máximo"] = datos.max()

    estadisticas["Rango"] = datos.max() - datos.min()

    estadisticas["Varianza"] = datos.var()

    estadisticas["Desviación estándar"] = datos.std()

    estadisticas["Coeficiente de variación"] = (
        datos.std()/datos.mean()*100
        if datos.mean()!=0 else np.nan
    )

    estadisticas["Q1"] = datos.quantile(0.25)

    estadisticas["Q2"] = datos.quantile(0.50)

    estadisticas["Q3"] = datos.quantile(0.75)

    estadisticas["Asimetría"] = datos.skew()

    estadisticas["Curtosis"] = datos.kurt()

    return estadisticas


# =====================================================
# INTERPRETACIÓN
# =====================================================

def interpretar_cv(cv):

    if np.isnan(cv):
        return "No se pudo calcular."

    if cv < 15:
        return "Variabilidad baja."

    elif cv < 30:
        return "Variabilidad moderada."

    else:
        return "Variabilidad alta."


# =====================================================
# INTERFAZ
# =====================================================

def mostrar():

    st.title("📊 Estadística Descriptiva")

    if "df" not in st.session_state:

        st.warning("Primero importa un archivo.")

        return

    df = st.session_state["df"]

    numericas = df.select_dtypes(include=np.number).columns

    if len(numericas)==0:

        st.error("No existen columnas numéricas.")

        return

    columna = st.selectbox(

        "Selecciona una variable",

        numericas

    )

    datos = df[columna].dropna()

    estadisticas = calcular_estadisticas(datos)

    c1,c2,c3 = st.columns(3)

    c1.metric("Media",f"{estadisticas['Media']:.2f}")

    c2.metric("Mediana",f"{estadisticas['Mediana']:.2f}")

    c3.metric("Moda",f"{estadisticas['Moda']:.2f}")

    st.divider()

    tabla = pd.DataFrame({

        "Medida":estadisticas.keys(),

        "Valor":estadisticas.values()

    })

    st.dataframe(tabla,use_container_width=True)

    st.info(

        interpretar_cv(

            estadisticas["Coeficiente de variación"]

        )

    )

    fig = px.histogram(

        df,

        x=columna,

        nbins=30,

        title=f"Histograma - {columna}"

    )

    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.box(

        df,

        y=columna,

        title=f"Diagrama de Caja - {columna}"

    )

    st.plotly_chart(fig2,use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================================
# TABLA DE FRECUENCIAS
# =====================================================

def calcular_frecuencias(df, columna):

    frecuencia = (
        df[columna]
        .value_counts(dropna=False)
        .reset_index()
    )

    frecuencia.columns = [
        "Valor",
        "Frecuencia"
    ]

    frecuencia["Frecuencia Relativa (%)"] = (
        frecuencia["Frecuencia"] /
        frecuencia["Frecuencia"].sum()
    ) * 100

    frecuencia["Frecuencia Acumulada"] = (
        frecuencia["Frecuencia"].cumsum()
    )

    frecuencia["Porcentaje Acumulado"] = (
        frecuencia["Frecuencia Relativa (%)"].cumsum()
    )

    return frecuencia


# =====================================================
# INTERPRETACIÓN
# =====================================================

def interpretar(tabla):

    mayor = tabla.iloc[0]

    texto = f"""
La categoría con mayor frecuencia es:

**{mayor['Valor']}**

con **{mayor['Frecuencia']} registros**,
equivalente al **{mayor['Frecuencia Relativa (%)']:.2f}%**
del total.
"""

    return texto


# =====================================================
# INTERFAZ
# =====================================================

def mostrar():

    st.title("📈 Tabla de Frecuencias")

    if "df" not in st.session_state:

        st.warning("Primero importa un archivo.")

        return

    df = st.session_state["df"]

    columna = st.selectbox(

        "Selecciona una variable",

        df.columns

    )

    tabla = calcular_frecuencias(df, columna)

    st.dataframe(

        tabla,

        use_container_width=True

    )

    st.info(

        interpretar(tabla)

    )

    fig = px.bar(

        tabla,

        x="Valor",

        y="Frecuencia",

        text="Frecuencia",

        title=f"Frecuencia de {columna}"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    fig2 = px.pie(

        tabla,

        names="Valor",

        values="Frecuencia",

        title="Distribución porcentual"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

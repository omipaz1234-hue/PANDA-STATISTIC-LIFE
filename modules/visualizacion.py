import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =====================================================
# VISUALIZACIONES
# =====================================================

def mostrar():

    st.title("📈 Visualización de Datos")

    if "df" not in st.session_state:

        st.warning("Primero importa un archivo.")

        return

    df = st.session_state["df"]

    columnas = df.columns.tolist()

    numericas = df.select_dtypes(include=np.number).columns.tolist()

    grafico = st.selectbox(

        "Selecciona el tipo de gráfico",

        [

            "Barras",

            "Histograma",

            "Circular",

            "Línea",

            "Caja",

            "Violín",

            "Dispersión",

            "Área"

        ]

    )

    # -------------------------------------------------

    if grafico == "Barras":

        x = st.selectbox("Variable X", columnas)

        y = st.selectbox("Variable Y", numericas)

        fig = px.bar(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Histograma":

        x = st.selectbox("Variable", numericas)

        fig = px.histogram(df, x=x)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Circular":

        nombres = st.selectbox("Categorías", columnas)

        valores = st.selectbox("Valores", numericas)

        fig = px.pie(

            df,

            names=nombres,

            values=valores

        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Línea":

        x = st.selectbox("Variable X", columnas)

        y = st.selectbox("Variable Y", numericas)

        fig = px.line(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Caja":

        y = st.selectbox("Variable", numericas)

        fig = px.box(df, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Violín":

        y = st.selectbox("Variable", numericas)

        fig = px.violin(df, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Dispersión":

        x = st.selectbox("Variable X", numericas)

        y = st.selectbox("Variable Y", numericas)

        fig = px.scatter(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    elif grafico == "Área":

        x = st.selectbox("Variable X", columnas)

        y = st.selectbox("Variable Y", numericas)

        fig = px.area(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    st.divider()

    st.info(
        "💡 Consejo: Selecciona el gráfico según el tipo de variable. "
        "En futuras versiones, PANDA AI recomendará automáticamente el gráfico más adecuado."
    )

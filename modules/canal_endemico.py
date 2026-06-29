import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ==========================================================
# MÉTODO MEDIA ± DE
# ==========================================================

def canal_media_desviacion(datos):

    media = datos.mean()

    de = datos.std()

    return media, de


# ==========================================================
# MÉTODO CUARTILES
# ==========================================================

def canal_cuartiles(datos):

    q1 = datos.quantile(0.25)

    q2 = datos.quantile(0.50)

    q3 = datos.quantile(0.75)

    return q1, q2, q3


# ==========================================================
# MÉTODO PERCENTILES
# ==========================================================

def canal_percentiles(datos):

    p25 = np.percentile(datos,25)

    p50 = np.percentile(datos,50)

    p75 = np.percentile(datos,75)

    return p25,p50,p75


# ==========================================================
# INTERFAZ
# ==========================================================

def mostrar():

    st.title("📉 Canal Endémico")

    if "df" not in st.session_state:

        st.warning("Primero importa un archivo.")

        return

    df = st.session_state["df"]

    numericas = df.select_dtypes(include=np.number).columns.tolist()

    if len(numericas)==0:

        st.error("No existen variables numéricas.")

        return

    columna = st.selectbox(

        "Selecciona la variable",

        numericas

    )

    metodo = st.selectbox(

        "Método",

        [

            "Media ± DE",

            "Cuartiles",

            "Percentiles"

        ]

    )

    datos = df[columna].dropna()

    fig = go.Figure()

    if metodo=="Media ± DE":

        media,de = canal_media_desviacion(datos)

        fig.add_hrect(
            y0=0,
            y1=max(0,media-de),
            fillcolor="green",
            opacity=0.20
        )

        fig.add_hrect(
            y0=max(0,media-de),
            y1=media+de,
            fillcolor="lightblue",
            opacity=0.25
        )

        fig.add_hrect(
            y0=media+de,
            y1=media+2*de,
            fillcolor="orange",
            opacity=0.25
        )

        fig.add_hrect(
            y0=media+2*de,
            y1=max(datos)*1.10,
            fillcolor="red",
            opacity=0.25
        )

        fig.add_trace(

            go.Scatter(

                x=df.index,

                y=datos,

                mode="lines+markers",

                name="Casos"

            )

        )

        fig.add_trace(

            go.Scatter(

                x=df.index,

                y=[media]*len(datos),

                mode="lines",

                name="Media"

            )

        )

        st.success(f"Media = {media:.2f}")

        st.success(f"Desviación = {de:.2f}")

    elif metodo=="Cuartiles":

        q1,q2,q3 = canal_cuartiles(datos)

        st.metric("Q1",f"{q1:.2f}")

        st.metric("Q2",f"{q2:.2f}")

        st.metric("Q3",f"{q3:.2f}")

        fig.add_trace(

            go.Box(

                y=datos,

                name="Cuartiles"

            )

        )

    else:

        p25,p50,p75 = canal_percentiles(datos)

        st.metric("P25",f"{p25:.2f}")

        st.metric("P50",f"{p50:.2f}")

        st.metric("P75",f"{p75:.2f}")

        fig.add_trace(

            go.Box(

                y=datos,

                name="Percentiles"

            )

        )

    fig.update_layout(

        height=700,

        title="Canal Endémico"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

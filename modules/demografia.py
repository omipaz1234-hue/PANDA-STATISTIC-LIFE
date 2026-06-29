import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# =====================================================
# PIRÁMIDE POBLACIONAL
# =====================================================

def mostrar():

    st.title("👥 Demografía")

    if "df" not in st.session_state:

        st.warning("Primero importa un archivo.")

        return

    df = st.session_state["df"]

    columnas = df.columns.tolist()

    edad = st.selectbox(

        "Columna Edad",

        columnas

    )

    sexo = st.selectbox(

        "Columna Sexo",

        columnas

    )

    if st.button("Generar Pirámide"):

        datos = df[[edad, sexo]].copy()

        datos = datos.dropna()

        bins = list(range(0, 101, 5))

        etiquetas = [

            "0-4","5-9","10-14","15-19","20-24",

            "25-29","30-34","35-39","40-44",

            "45-49","50-54","55-59","60-64",

            "65-69","70-74","75-79","80-84",

            "85-89","90-94","95-99"

        ]

        datos["Grupo"] = pd.cut(

            datos[edad],

            bins=bins,

            labels=etiquetas,

            right=False

        )

        hombres = datos[
            datos[sexo].astype(str).str.upper().isin(["M","HOMBRE","MASCULINO"])
        ]

        mujeres = datos[
            datos[sexo].astype(str).str.upper().isin(["F","MUJER","FEMENINO"])
        ]

        h = hombres.groupby("Grupo").size()

        m = mujeres.groupby("Grupo").size()

        fig = go.Figure()

        fig.add_trace(

            go.Bar(

                y=h.index,

                x=-h.values,

                orientation="h",

                name="Hombres"

            )

        )

        fig.add_trace(

            go.Bar(

                y=m.index,

                x=m.values,

                orientation="h",

                name="Mujeres"

            )

        )

        fig.update_layout(

            title="Pirámide Poblacional",

            barmode="overlay",

            height=700

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        st.success("Pirámide generada correctamente.")

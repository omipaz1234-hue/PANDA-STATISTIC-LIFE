import streamlit as st
import pandas as pd
import numpy as np


# ==========================================================
# CARGAR ARCHIVO
# ==========================================================

def cargar_archivo(uploaded_file):
    """
    Carga archivos CSV, XLS y XLSX.
    """

    if uploaded_file is None:
        return None

    nombre = uploaded_file.name.lower()

    try:

        if nombre.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif nombre.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        elif nombre.endswith(".xls"):
            df = pd.read_excel(uploaded_file)

        else:
            st.error("Formato no soportado.")
            return None

        return df

    except Exception as e:
        st.error(f"Error al cargar archivo: {e}")
        return None


# ==========================================================
# LIMPIEZA
# ==========================================================

def limpiar_dataframe(df):

    if df is None:
        return None

    # eliminar filas vacías
    df = df.dropna(axis=0, how="all")

    # eliminar columnas vacías
    df = df.dropna(axis=1, how="all")

    # quitar espacios en nombres
    df.columns = df.columns.astype(str).str.strip()

    # reiniciar índice
    df.reset_index(drop=True, inplace=True)

    return df


# ==========================================================
# DETECTAR COLUMNAS
# ==========================================================

def detectar_columnas(df):

    numericas = df.select_dtypes(include=np.number).columns.tolist()

    categoricas = df.select_dtypes(include="object").columns.tolist()

    return numericas, categoricas


# ==========================================================
# INFORMACIÓN
# ==========================================================

def resumen(df):

    numericas, categoricas = detectar_columnas(df)

    st.success("Archivo cargado correctamente")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Filas", df.shape[0])

    c2.metric("Columnas", df.shape[1])

    c3.metric("Numéricas", len(numericas))

    c4.metric("Categóricas", len(categoricas))

    st.subheader("Vista previa")

    st.dataframe(df.head(10), use_container_width=True)


# ==========================================================
# INTERFAZ
# ==========================================================

def mostrar():

    st.title("📥 Importación de Datos")

    st.info(
        "Carga archivos Excel o CSV para comenzar el análisis."
    )

    archivo = st.file_uploader(

        "Selecciona un archivo",

        type=["csv", "xls", "xlsx"]

    )

    if archivo:

        with st.spinner("Cargando archivo..."):

            df = cargar_archivo(archivo)

            df = limpiar_dataframe(df)

            if df is not None:

                resumen(df)

                st.session_state["df"] = df

                st.success(
                    "Los datos quedaron almacenados para el resto del sistema."
                )

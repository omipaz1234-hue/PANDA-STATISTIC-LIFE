import streamlit as st
import pandas as pd

def mostrar():

    st.title("📈 Canal Endémico")

    st.markdown("""
    Construya el Canal Endémico utilizando un archivo histórico independiente.
    """)

    st.info("""
Para generar un Canal Endémico se requiere:

✅ Cinco años históricos

✅ Año actual

✅ Semana Epidemiológica

✅ Número de casos
""")

    archivo = st.file_uploader(
        "Seleccione el archivo histórico",
        type=["xlsx", "xls", "csv"]
    )

    if archivo is not None:

        try:

            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)

            st.success("✅ Archivo cargado correctamente")

            # ============================
            # VALIDAR COLUMNAS
            # ============================

            columnas_requeridas = [
                "Año",
                "Semana",
                "Casos"
            ]

            faltantes = []

            for col in columnas_requeridas:
                if col not in df.columns:
                    faltantes.append(col)

            if faltantes:

                st.error("❌ Faltan las siguientes columnas:")

                for col in faltantes:
                    st.write(f"• {col}")

                st.stop()

            else:

                st.success("✅ El archivo cumple con la estructura requerida.")

            st.write("### Vista previa")

            st.dataframe(df.head())

            st.write("### Información")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Filas", len(df))

            with c2:
                st.metric("Columnas", len(df.columns))

            with c3:
                st.metric(
                    "Años encontrados",
                    df["Año"].nunique() if "Año" in df.columns else 0
                )

            st.divider()

            if st.button("📈 Generar Canal Endémico"):

                st.warning("Aquí construiremos el Canal Endémico en la versión 2.")

        except Exception as e:

            st.error(e)

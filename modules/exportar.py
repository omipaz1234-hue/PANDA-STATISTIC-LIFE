import streamlit as st
import pandas as pd
from io import BytesIO


# ==========================================================
# EXPORTAR A EXCEL
# ==========================================================

def exportar_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Resultados"
        )

    return output.getvalue()


# ==========================================================
# INTERFAZ
# ==========================================================

def mostrar():

    st.title("📄 Exportar Resultados")

    if "df" not in st.session_state:

        st.warning("No existen datos cargados.")

        return

    df = st.session_state["df"]

    st.subheader("Vista previa")

    st.dataframe(df.head())

    archivo = exportar_excel(df)

    st.download_button(

        "📥 Descargar Excel",

        archivo,

        file_name="PANDA_Resultados.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        "📥 Descargar CSV",

        csv,

        file_name="PANDA_Resultados.csv",

        mime="text/csv"

    )

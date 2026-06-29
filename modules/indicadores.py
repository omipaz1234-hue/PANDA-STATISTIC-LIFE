import streamlit as st


# ==========================================================
# FUNCIONES
# ==========================================================

def incidencia(casos, poblacion):

    if poblacion == 0:
        return 0

    return (casos / poblacion) * 100000


def prevalencia(casos, poblacion):

    if poblacion == 0:
        return 0

    return (casos / poblacion) * 100


def letalidad(defunciones, casos):

    if casos == 0:
        return 0

    return (defunciones / casos) * 100


def mortalidad(defunciones, poblacion):

    if poblacion == 0:
        return 0

    return (defunciones / poblacion) * 100000


# ==========================================================
# INTERPRETACIÓN
# ==========================================================

def interpretar(inc):

    if inc < 50:

        return "Incidencia baja."

    elif inc < 200:

        return "Incidencia moderada."

    else:

        return "Incidencia alta."


# ==========================================================
# INTERFAZ
# ==========================================================

def mostrar():

    st.title("🏥 Indicadores de Salud")

    casos = st.number_input(

        "Número de casos",

        0,

        value=120

    )

    poblacion = st.number_input(

        "Población",

        1,

        value=10000

    )

    defunciones = st.number_input(

        "Defunciones",

        0,

        value=10

    )

    if st.button("Calcular indicadores"):

        inc = incidencia(casos, poblacion)

        prev = prevalencia(casos, poblacion)

        let = letalidad(defunciones, casos)

        mort = mortalidad(defunciones, poblacion)

        c1, c2 = st.columns(2)

        c1.metric(

            "Incidencia",

            f"{inc:.2f} x100 000"

        )

        c2.metric(

            "Prevalencia",

            f"{prev:.2f}%"

        )

        c1.metric(

            "Letalidad",

            f"{let:.2f}%"

        )

        c2.metric(

            "Mortalidad",

            f"{mort:.2f} x100 000"

        )

        st.success(

            interpretar(inc)

        )

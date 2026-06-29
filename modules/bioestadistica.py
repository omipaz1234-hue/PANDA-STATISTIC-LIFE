import streamlit as st
import pandas as pd


# ==========================================================
# FUNCIONES
# ==========================================================

def calcular_medidas(a, b, c, d):

    resultados = {}

    try:

        rr = (a / (a + b)) / (c / (c + d))

    except:

        rr = 0

    try:

        orr = (a * d) / (b * c)

    except:

        orr = 0

    try:

        sensibilidad = a / (a + c)

    except:

        sensibilidad = 0

    try:

        especificidad = d / (b + d)

    except:

        especificidad = 0

    try:

        vpp = a / (a + b)

    except:

        vpp = 0

    try:

        vpn = d / (c + d)

    except:

        vpn = 0

    try:

        exactitud = (a + d) / (a + b + c + d)

    except:

        exactitud = 0

    resultados["RR"] = rr

    resultados["OR"] = orr

    resultados["Sensibilidad"] = sensibilidad

    resultados["Especificidad"] = especificidad

    resultados["VPP"] = vpp

    resultados["VPN"] = vpn

    resultados["Exactitud"] = exactitud

    return resultados


# ==========================================================
# INTERPRETACIÓN RR
# ==========================================================

def interpretar_rr(rr):

    if rr < 1:

        return "La exposición parece actuar como un factor protector."

    elif rr == 1:

        return "No se observa asociación."

    else:

        return "La exposición incrementa el riesgo de enfermedad."


# ==========================================================
# INTERFAZ
# ==========================================================

def mostrar():

    st.title("🦠 Bioestadística")

    st.subheader("Tabla 2 × 2")

    c1, c2 = st.columns(2)

    with c1:

        a = st.number_input(
            "Enfermo + Expuesto (a)",
            0,
            value=20
        )

        c = st.number_input(
            "Enfermo + No expuesto (c)",
            0,
            value=15
        )

    with c2:

        b = st.number_input(
            "Sano + Expuesto (b)",
            0,
            value=35
        )

        d = st.number_input(
            "Sano + No expuesto (d)",
            0,
            value=60
        )

    if st.button("Calcular"):

        tabla = pd.DataFrame(

            [[a, b], [c, d]],

            index=["Enfermo", "No Enfermo"],

            columns=["Expuesto", "No Expuesto"]

        )

        st.dataframe(tabla, use_container_width=True)

        r = calcular_medidas(a, b, c, d)

        c1, c2, c3 = st.columns(3)

        c1.metric("RR", f"{r['RR']:.2f}")

        c2.metric("OR", f"{r['OR']:.2f}")

        c3.metric("Exactitud", f"{r['Exactitud']:.2%}")

        st.divider()

        st.metric("Sensibilidad", f"{r['Sensibilidad']:.2%}")

        st.metric("Especificidad", f"{r['Especificidad']:.2%}")

        st.metric("VPP", f"{r['VPP']:.2%}")

        st.metric("VPN", f"{r['VPN']:.2%}")

        st.success(

            interpretar_rr(

                r["RR"]

            )

        )

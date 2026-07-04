import streamlit as st

def mostrar():

    # ============================
    # BANNER
    # ============================

    st.markdown('<div style="position:relative;">', unsafe_allow_html=True)

    st.image("assets/banner.png", use_container_width=True)

    col1, col2, col3 = st.columns([1.3, 3.8, 1.3])

    with col1:
        st.image("assets/panda.png", width=190)

    with col2:

        st.markdown("""
        <div style="text-align:center; margin-top:25px;">

        <h1 style="
        font-size:60px;
        color:#2F2FA2;
        margin-bottom:5px;
        ">
        PANDA STATISTIC LIFE
        </h1>

        <h3 style="
        color:#3F3F46;
        margin-top:0;
        ">
        Plataforma Boliviana de Estadística
        </h3>

        <h3 style="
        color:#3F3F46;
        margin-top:-10px;
        ">
        y Vigilancia Epidemiológica
        </h3>

        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.image("assets/bolivia.png", width=190)

    st.divider()

    # ============================
    # MENÚ RÁPIDO
    # ============================

    c1,c2,c3,c4,c5,c6=st.columns(6)

    with c1:
        st.button("📊 Estadística",use_container_width=True)

    with c2:
        st.button("🦠 Bioestadística",use_container_width=True)

    with c3:
        st.button("👥 Demografía",use_container_width=True)

    with c4:
        st.button("🛡 Vigilancia",use_container_width=True)

    with c5:
        st.button("🗄 SNIS",use_container_width=True)

    with c6:
        st.button("📈 Canal Endémico",use_container_width=True)

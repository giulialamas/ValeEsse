import streamlit as st

st.set_page_config(page_title="Vale Esse", page_icon="💸", layout="centered")

st.title("💸 Vale Esse")
st.caption("Compare o que realmente rende mais pelo custo real.")

tab1, tab2 = st.tabs(["⛽ Combustível", "🧴 Produtos"])

# ======================================================
# ABA PRINCIPAL — COMBUSTÍVEL
# ======================================================
with tab1:
    st.subheader("⛽ Etanol vs Gasolina")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Etanol")
        preco_e = st.number_input("Preço (R$/L)", value=4.55, key="pe")
        consumo_e = st.number_input("Consumo (km/L)", value=11.5, key="ce")

    with col2:
        st.markdown("### Gasolina")
        preco_g = st.number_input("Preço (R$/L)", value=6.55, key="pg")
        consumo_g = st.number_input("Consumo (km/L)", value=15.0, key="cg")

    st.divider()

    if st.button("Comparar combustível", use_container_width=True):
        custo_km_e = preco_e / consumo_e
        custo_km_g = preco_g / consumo_g

        st.markdown("### Custo real por km")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Etanol (R$/km)", f"{custo_km_e:.3f}")
        with c2:
            st.metric("Gasolina (R$/km)", f"{custo_km_g:.3f}")

        if custo_km_e < custo_km_g:
            economia = (custo_km_g - custo_km_e) / custo_km_g * 100
            st.success(f"✅ Vale mais a pena: **Etanol** ({economia:.1f}% mais barato por km)")
        elif custo_km_g < custo_km_e:
            economia = (custo_km_e - custo_km_g) / custo_km_e * 100
            st.success(f"✅ Vale mais a pena: **Gasolina** ({economia:.1f}% mais barato por km)")
        else:
            st.info("Empate: os dois custam igual por km.")

# ======================================================
# ABA SECUNDÁRIA — PRODUTOS
# ======================================================
with tab2:
    st.subheader("🧴 Comparador de produtos por volume")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Produto A")
        nome_a = st.text_input("Nome", value="Vichy antiqueda refil", key="na")
        preco_a = st.number_input("Preço (R$)", value=60.0, key="pa")
        vol_a = st.number_input("Volume (mL)", value=200.0, key="va")

    with col2:
        st.markdown("### Produto B")
        nome_b = st.text_input("Nome", value="Vichy antiqueda dispenser", key="nb")
        preco_b = st.number_input("Preço (R$)", value=120.0, key="pb")
        vol_b = st.number_input("Volume (mL)", value=400.0, key="vb")

    if st.button("Comparar produtos", use_container_width=True):
        ppm_a = preco_a / vol_a
        ppm_b = preco_b / vol_b

        st.markdown("### Custo real por mL")

        if ppm_a < ppm_b:
            st.success(f"Vale mais a pena: **{nome_a}**")
        elif ppm_b < ppm_a:
            st.success(f"Vale mais a pena: **{nome_b}**")
        else:
            st.info("Empate: os dois rendem igual.")

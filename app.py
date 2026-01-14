import streamlit as st

st.set_page_config(page_title="Vale Esse", page_icon="💸", layout="centered")

st.title("💸 Vale Esse")
st.caption("Compare o que realmente rende mais pelo custo real.")

tab1, tab2 = st.tabs(["🧴 Produtos", "⛽ Combustível"])

# ---------------------------
# ABA 1 — PRODUTOS
# ---------------------------
with tab1:
    st.subheader("🧴 Comparador de produtos por volume")

    with st.container(border=True):
        st.markdown("### Produto A")
        nome_a = st.text_input("Nome (A)", value="Vichy antiqueda refil")
        preco_a = st.number_input("Preço (R$)", value=60.0)
        vol_a = st.number_input("Volume (mL)", value=200.0)

    with st.container(border=True):
        st.markdown("### Produto B")
        nome_b = st.text_input("Nome (B)", value="Vichy antiqueda dispenser")
        preco_b = st.number_input("Preço (R$)", value=120.0)
        vol_b = st.number_input("Volume (mL)", value=400.0)

    if st.button("Comparar produtos"):
        ppm_a = preco_a / vol_a
        ppm_b = preco_b / vol_b

        st.markdown("### Resultado")

        st.metric(f"{nome_a} (R$/mL)", f"{ppm_a:.4f}")
        st.metric(f"{nome_b} (R$/mL)", f"{ppm_b:.4f}")

        if ppm_a < ppm_b:
            st.success(f"Vale mais a pena: **{nome_a}**")
        elif ppm_b < ppm_a:
            st.success(f"Vale mais a pena: **{nome_b}**")
        else:
            st.info("Empate: os dois rendem igual por mL.")

# ---------------------------
# ABA 2 — COMBUSTÍVEL
# ---------------------------
with tab2:
    st.subheader("⛽ Etanol vs Gasolina")

    with st.container(border=True):
        preco_e = st.number_input("Preço Etanol (R$/L)", value=4.55)
        consumo_e = st.number_input("Consumo Etanol (km/L)", value=11.5)

    with st.container(border=True):
        preco_g = st.number_input("Preço Gasolina (R$/L)", value=6.55)
        consumo_g = st.number_input("Consumo Gasolina (km/L)", value=15.0)

    if st.button("Comparar combustível"):
        custo_km_e = preco_e / consumo_e
        custo_km_g = preco_g / consumo_g

        st.markdown("### Custo real por km")

        st.metric("Etanol (R$/km)", f"{custo_km_e:.3f}")
        st.metric("Gasolina (R$/km)", f"{custo_km_g:.3f}")

        if custo_km_e < custo_km_g:
            st.success("Vale mais a pena: **Etanol**")
        elif custo_km_g < custo_km_e:
            st.success("Vale mais a pena: **Gasolina**")
        else:
            st.info("Empate: os dois custam igual por km.")

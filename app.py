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
        preco_e = st.number_input("Preço (R$/L)", value=4.55, key="pe", min_value=0.0, step=0.05)
        consumo_e = st.number_input("Consumo (km/L)", value=11.5, key="ce", min_value=0.0, step=0.1)

    with col2:
        st.markdown("### Gasolina")
        preco_g = st.number_input("Preço (R$/L)", value=6.55, key="pg", min_value=0.0, step=0.05)
        consumo_g = st.number_input("Consumo (km/L)", value=15.0, key="cg", min_value=0.0, step=0.1)

    st.divider()

    if st.button("Comparar combustível", use_container_width=True):
        if consumo_e <= 0 or consumo_g <= 0:
            st.error("O consumo (km/L) precisa ser maior que zero.")
        else:
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

    # ------------------------------------------------------
    # NOVO BLOCO — DESCOBRIR CONSUMO AO COMPLETAR O TANQUE
    # ------------------------------------------------------
    st.divider()
    st.subheader("🔎 Descubra o consumo ao completar o tanque")
    st.caption("Preencha com a quilometragem rodada desde o último abastecimento e os litros necessários para completar o tanque.")

    col3, col4 = st.columns(2)
    with col3:
        km_rodados = st.number_input("Quilometragem rodada (km)", value=300.0, min_value=0.0, step=10.0, key="km_rodados")
    with col4:
        litros_usados = st.number_input("Litros abastecidos para completar (L)", value=25.0, min_value=0.0, step=1.0, key="litros_usados")

    combustivel_usado = st.radio(
        "Qual combustível você usou nesse período?",
        ["Etanol", "Gasolina"],
        horizontal=True,
        key="comb_usado"
    )

    if st.button("Calcular consumo", use_container_width=True):
        if km_rodados <= 0 or litros_usados <= 0:
            st.error("Quilometragem e litros precisam ser maiores que zero.")
        else:
            km_por_l = km_rodados / litros_usados
            l_por_100km = 100 / km_por_l

            st.markdown("### Resultado do seu consumo")
            r1, r2 = st.columns(2)
            with r1:
                st.metric("Consumo (km/L)", f"{km_por_l:.2f}")
            with r2:
                st.metric("Consumo (L/100 km)", f"{l_por_100km:.2f}")

            preco_ref = preco_e if combustivel_usado == "Etanol" else preco_g
            custo_por_km = preco_ref / km_por_l
            st.write(f"Com o preço informado para **{combustivel_usado}**, seu custo ficou em **R$ {custo_por_km:.3f}/km**.")

# ======================================================
# ABA SECUNDÁRIA — PRODUTOS
# ======================================================
with tab2:
    st.subheader("🧴 Comparador de produtos por volume")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Produto A")
        preco_a = st.number_input("Preço (R$)", value=120.18, key="pa", min_value=0.0, step=0.10)
        vol_a = st.number_input("Volume (mL)", value=200.0, key="va", min_value=0.0, step=10.0)

    with col2:
        st.markdown("### Produto B")
        preco_b = st.number_input("Preço (R$)", value=65.35, key="pb", min_value=0.0, step=0.10)
        vol_b = st.number_input("Volume (mL)", value=400.0, key="vb", min_value=0.0, step=10.0)

    if st.button("Comparar produtos", use_container_width=True):
        if vol_a <= 0 or vol_b <= 0:
            st.error("Os volumes precisam ser maiores que zero.")
        else:
            ppm_a = preco_a / vol_a
            ppm_b = preco_b / vol_b

            st.markdown("### Custo real por mL")

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Produto A (R$/mL)", f"{ppm_a:.4f}")
                st.caption(f"R$ {ppm_a*100:.2f} por 100 mL")
            with c2:
                st.metric("Produto B (R$/mL)", f"{ppm_b:.4f}")
                st.caption(f"R$ {ppm_b*100:.2f} por 100 mL")

            if ppm_a < ppm_b:
                st.success("Vale mais a pena: **Produto A**")
            elif ppm_b < ppm_a:
                st.success("Vale mais a pena: **Produto B**")
            else:
                st.info("Empate: os dois rendem igual por mL.")

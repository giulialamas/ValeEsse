import streamlit as st

st.set_page_config(page_title="Vale Esse", page_icon="💸", layout="centered")

st.title("💸 Vale Esse")
st.caption("Compare o que realmente rende mais pelo custo real.")

# ======================================================
# NAVEGAÇÃO (no lugar de tabs)
# ======================================================
pagina = st.sidebar.radio("Ir para", ["⛽ Combustível", "🧴 Produtos"], index=0)

# ======================================================
# PÁGINA: COMBUSTÍVEL
# ======================================================
if pagina == "⛽ Combustível":
    st.subheader("⛽ Etanol vs Gasolina")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Etanol")
        preco_e = st.number_input("Preço (R$/L)", value=4.55, min_value=0.0, step=0.05, key="pe")
        consumo_e = st.number_input("Consumo (km/L)", value=11.5, min_value=0.0, step=0.1, key="ce")

    with col2:
        st.markdown("### Gasolina")
        preco_g = st.number_input("Preço (R$/L)", value=6.55, min_value=0.0, step=0.05, key="pg")
        consumo_g = st.number_input("Consumo (km/L)", value=15.0, min_value=0.0, step=0.1, key="cg")

    if st.button("Comparar combustível", use_container_width=True, key="btn_compare_fuel"):
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

    # ---------------- SIDEBAR específica de combustível ----------------
    st.sidebar.divider()
    st.sidebar.subheader("🔎 Descubra seu consumo")
    st.sidebar.caption("Use quando completou o tanque.")

    km_rodados = st.sidebar.number_input("Km rodados", value=300.0, min_value=0.0, step=10.0, key="km_rodados")
    litros_usados = st.sidebar.number_input("Litros abastecidos", value=25.0, min_value=0.0, step=1.0, key="litros_usados")
    combustivel_usado = st.sidebar.radio("Combustível usado", ["Etanol", "Gasolina"], horizontal=True, key="comb_usado")

    if st.sidebar.button("Calcular consumo", use_container_width=True, key="btn_consumo"):
        if km_rodados <= 0 or litros_usados <= 0:
            st.sidebar.error("Km e litros precisam ser > 0.")
        else:
            km_por_l = km_rodados / litros_usados
            l_por_100km = 100 / km_por_l
            st.sidebar.success("Calculado!")
            st.sidebar.metric("km/L", f"{km_por_l:.2f}")
            st.sidebar.metric("L/100 km", f"{l_por_100km:.2f}")

            preco_ref = preco_e if combustivel_usado == "Etanol" else preco_g
            custo_por_km = preco_ref / km_por_l
            st.sidebar.metric("R$/km", f"{custo_por_km:.3f}")

# ======================================================
# PÁGINA: PRODUTOS
# ======================================================
else:
    st.subheader("🧴 Comparador de produtos")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Produto A")
        preco_a = st.number_input("Preço (R$)", value=120.18, min_value=0.0, step=0.10, key="pa")
        vol_a = st.number_input("Volume (mL)", value=200.0, min_value=0.0, step=10.0, key="va")

    with col2:
        st.markdown("### Produto B")
        preco_b = st.number_input("Preço (R$)", value=65.35, min_value=0.0, step=0.10, key="pb")
        vol_b = st.number_input("Volume (mL)", value=400.0, min_value=0.0, step=10.0, key="vb")

    if st.button("Comparar produtos", use_container_width=True, key="btn_compare_products"):
        if vol_a <= 0 or vol_b <= 0:
            st.error("Volumes precisam ser maiores que zero.")
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

    # ---------------- SIDEBAR específica de produtos ----------------
    st.sidebar.divider()
    st.sidebar.subheader("🧴 Calculadora unitária")
    st.sidebar.caption("Para checar um item sozinho (volume ou unidades).")

    modo = st.sidebar.radio("Modo", ["Por volume", "Por unidades"], horizontal=True, key="modo_unitario")

    preco = st.sidebar.number_input("Preço total (R$)", value=65.35, min_value=0.0, step=0.10, key="preco_unit")

    if modo == "Por volume":
        unidade_vol = st.sidebar.selectbox("Unidade", ["mL", "L"], index=0, key="unidade_vol")
        quantidade = st.sidebar.number_input(
            f"Volume ({unidade_vol})",
            value=200.0 if unidade_vol == "mL" else 0.2,
            min_value=0.0,
            step=10.0 if unidade_vol == "mL" else 0.1,
            key="qtd_vol"
        )

        if st.sidebar.button("Calcular unitário", use_container_width=True, key="btn_unitario_vol"):
            if quantidade <= 0:
                st.sidebar.error("Volume precisa ser > 0.")
            else:
                volume_ml = quantidade if unidade_vol == "mL" else quantidade * 1000.0
                r_por_ml = preco / volume_ml
                st.sidebar.metric("R$/mL", f"{r_por_ml:.4f}")
                st.sidebar.metric("R$ por 100 mL", f"{r_por_ml*100:.2f}")
                st.sidebar.metric("R$ por 1 L", f"{r_por_ml*1000:.2f}")

    else:
        unidades = st.sidebar.number_input("Quantidade (un)", value=12.0, min_value=0.0, step=1.0, key="qtd_un")

        if st.sidebar.button("Calcular unitário", use_container_width=True, key="btn_unitario_un"):
            if unidades <= 0:
                st.sidebar.error("Unidades precisam ser > 0.")
            else:
                st.sidebar.metric("R$/unidade", f"{(preco/unidades):.2f}")

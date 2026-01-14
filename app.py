import streamlit as st

st.set_page_config(page_title="Vale Esse", page_icon="💸", layout="centered")

st.title("💸 Vale Esse")
st.caption("Compare o que realmente rende mais pelo custo real.")

# =========================
# Navegação mobile-friendly
# =========================
pagina = st.segmented_control(
    "Escolha",
    options=["⛽ Combustível", "🧴 Produtos"],
    default="⛽ Combustível",
)

# ======================================================
# PÁGINA: COMBUSTÍVEL
# ======================================================
if pagina == "⛽ Combustível":
    st.subheader("⛽ Etanol vs Gasolina")

    # Consumos (podem ser atualizados pelo consumo medido abaixo)
    consumo_real = st.session_state.get("consumo_real")
    comb_real = st.session_state.get("comb_real")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Etanol")
        preco_e = st.number_input("Preço (R$/L)", value=4.55, min_value=0.0, step=0.05, key="pe")

        valor_default_e = consumo_real if (consumo_real and comb_real == "Etanol") else 11.5
        consumo_e = st.number_input("Consumo (km/L)", value=float(valor_default_e), min_value=0.1, step=0.1, key="ce")

    with col2:
        st.markdown("### Gasolina")
        preco_g = st.number_input("Preço (R$/L)", value=6.55, min_value=0.0, step=0.05, key="pg")

        valor_default_g = consumo_real if (consumo_real and comb_real == "Gasolina") else 15.0
        consumo_g = st.number_input("Consumo (km/L)", value=float(valor_default_g), min_value=0.1, step=0.1, key="cg")

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

    # -----------------------------
    # Mobile-friendly: expander no corpo
    # -----------------------------
    with st.expander("🔎 Descubra o consumo ao completar o tanque", expanded=False):
        st.caption("Informe km rodados desde o último abastecimento e litros para completar o tanque.")

        km_rodados = st.number_input("Quilometragem rodada (km)", value=300.0, min_value=0.0, step=10.0, key="km_rodados")
        litros_usados = st.number_input("Litros abastecidos (L)", value=25.0, min_value=0.0, step=1.0, key="litros_usados")

        combustivel_usado = st.radio("Combustível usado", ["Etanol", "Gasolina"], horizontal=True, key="comb_usado")

        if st.button("Calcular e usar no painel", use_container_width=True, key="btn_consumo"):
            if km_rodados <= 0 or litros_usados <= 0:
                st.error("Km e litros precisam ser maiores que zero.")
            else:
                km_por_l = km_rodados / litros_usados
                st.session_state["consumo_real"] = km_por_l
                st.session_state["comb_real"] = combustivel_usado

                st.success(f"Consumo salvo: **{km_por_l:.2f} km/L** (aplicado ao {combustivel_usado}).")
                st.info("Agora volte acima e rode **Comparar combustível** para ver o resultado com seu consumo real.")

# ======================================================
# PÁGINA: PRODUTOS
# ======================================================
else:
    st.subheader("🧴 Produtos por volume (A vs B)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Produto A")
        preco_a = st.number_input("Preço (R$)", value=120.18, min_value=0.0, step=0.10, key="pa")
        vol_a = st.number_input("Volume (mL)", value=200.0, min_value=0.0, step=10.0, key="va")

    with col2:
        st.markdown("### Produto B")
        preco_b = st.number_input("Preço (R$)", value=65.35, min_value=0.0, step=0.10, key="pb")
        vol_b = st.number_input("Volume (mL)", value=400.0, min_value=0.0, step=10.0, key="vb")

    if st.button("Comparar produtos", use_container_width=True):
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

    with st.expander("🧮 Calculadora unitária (1 item)", expanded=False):
        st.caption("Use quando você quer checar só 1 item: por volume (mL/L) ou por unidades (un).")

        modo = st.radio("Modo", ["Por volume", "Por unidades"], horizontal=True, key="modo_unitario")

        preco = st.number_input("Preço total (R$)", value=65.35, min_value=0.0, step=0.10, key="preco_unit")

        if modo == "Por volume":
            unidade_vol = st.selectbox("Unidade", ["mL", "L"], index=0, key="unidade_vol")
            quantidade = st.number_input(
                f"Volume ({unidade_vol})",
                value=200.0 if unidade_vol == "mL" else 0.2,
                min_value=0.0,
                step=10.0 if unidade_vol == "mL" else 0.1,
                key="qtd_vol"
            )

            if st.button("Calcular unitário", use_container_width=True, key="btn_unit_vol"):
                if quantidade <= 0:
                    st.error("Volume precisa ser maior que zero.")
                else:
                    volume_ml = quantidade if unidade_vol == "mL" else quantidade * 1000.0
                    r_por_ml = preco / volume_ml
                    st.metric("R$/mL", f"{r_por_ml:.4f}")
                    st.metric("R$ por 100 mL", f"{r_por_ml*100:.2f}")
                    st.metric("R$ por 1 L", f"{r_por_ml*1000:.2f}")

        else:
            unidades = st.number_input("Quantidade (un)", value=12.0, min_value=0.0, step=1.0, key="qtd_un")

            if st.button("Calcular unitário", use_container_width=True, key="btn_unit_un"):
                if unidades <= 0:
                    st.error("Unidades precisam ser maiores que zero.")
                else:
                    st.metric("R$/unidade", f"{(preco/unidades):.2f}")

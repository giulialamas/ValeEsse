import streamlit as st

st.set_page_config(page_title="Vale Esse", page_icon="💸", layout="centered")

st.title("💸 Vale Esse")
st.caption("Compare o que realmente rende mais pelo custo real.")

# =========================
# Navegação mobile-friendly
# =========================
pagina = st.segmented_control(
    "Escolha",
    options=["⛽ Combustível", "🛒 Produtos"],
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

        if st.button("Calcular", use_container_width=True, key="btn_consumo"):
            if km_rodados <= 0 or litros_usados <= 0:
                st.error("Km e litros precisam ser maiores que zero.")
            else:
                km_por_l = km_rodados / litros_usados
                st.session_state["consumo_real"] = km_por_l
                st.session_state["comb_real"] = combustivel_usado

                st.success(f"Consumo salvo: **{km_por_l:.2f} km/L** (aplicado ao {combustivel_usado}).")
                st.info("Agora volte acima, cole esse novo valor e rode **Comparar combustível** para ver o resultado com seu consumo real.")

# ======================================================
# PÁGINA: PRODUTOS
# ======================================================
else:
    st.subheader("🛒 Produtos")

    sub = st.segmented_control(
        "Tipo de produto",
        options=["🧴 Líquidos & Cremes", "📦 Pacotes & Unidades", "🧻 Papéis & Rolos"],
        default="🧴 Líquidos & Cremes",
        key="prod_sub"
    )

    # -----------------------------
    # SUBABA: LÍQUIDOS & CREMES
    # -----------------------------
    if sub == "🧴 Líquidos & Cremes":
        st.caption("Compare por volume (mL, L ou m³).")
    
        def to_ml(valor: float, unidade: str) -> float:
            if unidade == "mL": return valor
            if unidade == "L": return valor * 1000
            if unidade == "m³": return valor * 1_000_000
            return 0
    
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Produto A")
            preco_a = st.number_input("Preço (R$)", value=120.18, min_value=0.0, step=0.10, key="pa_vol")
            unidade_a = st.selectbox("Unidade", ["mL", "L", "m³"], index=0, key="ua_vol")
            vol_a = st.number_input(f"Volume ({unidade_a})", value=200.0, min_value=0.0, step=10.0, key="va_vol")
    
        with col2:
            st.markdown("### Produto B")
            preco_b = st.number_input("Preço (R$)", value=65.35, min_value=0.0, step=0.10, key="pb_vol")
            unidade_b = st.selectbox("Unidade ", ["mL", "L", "m³"], index=0, key="ub_vol")
            vol_b = st.number_input(f"Volume ({unidade_b})", value=400.0, min_value=0.0, step=10.0, key="vb_vol")
    
        if st.button("Comparar (volume)", use_container_width=True, key="btn_cmp_vol"):
            va = to_ml(vol_a, unidade_a)
            vb = to_ml(vol_b, unidade_b)
    
            if va <= 0 or vb <= 0:
                st.error("Volumes precisam ser maiores que zero.")
            else:
                ra = preco_a / va
                rb = preco_b / vb
    
                c1, c2 = st.columns(2)
                
                with c1:
                    st.metric("Produto A (R$/mL)", f"{ra:.6f}")
                    st.caption(f"{brl(ra*100)} por 100 mL • {brl(ra*1000)} por 1 L")
                
                with c2:
                    st.metric("Produto B (R$/mL)", f"{rb:.6f}")
                    st.caption(f"{brl(rb*100)} por 100 mL • {brl(rb*1000)} por 1 L")
    
                if ra < rb:
                    st.success("✅ Vale mais a pena: **Produto A**")
                elif rb < ra:
                    st.success("✅ Vale mais a pena: **Produto B**")
                else:
                    st.info("Empate: os dois custam igual por volume.")

    # -----------------------------
    # SUBABA: PACOTES & UNIDADES
    # -----------------------------
    elif sub == "📦 Pacotes & Unidades":
        st.caption("Compare por unidade.")

        col1, col2 = st.columns(2)
        with col1:
            preco_a = st.number_input("Preço A (R$)", 120.18, key="pa_un")
            un_a = st.number_input("Unidades A", 12, key="qa_un")

        with col2:
            preco_b = st.number_input("Preço B (R$)", 65.35, key="pb_un")
            un_b = st.number_input("Unidades B", 6, key="qb_un")

        if st.button("Comparar (unidades)", use_container_width=True):
            ra = preco_a / un_a
            rb = preco_b / un_b
            st.metric("Produto A (R$/un)", f"{ra:.2f}")
            st.metric("Produto B (R$/un)", f"{rb:.2f}")
            st.success("Vale mais a pena: **Produto A**" if ra < rb else "Vale mais a pena: **Produto B**")

    # -----------------------------
    # SUBABA: PAPÉIS & ROLOS
    # -----------------------------
    elif sub == "🧻 Papéis & Rolos":
        st.caption("Compare por metragem.")

        col1, col2 = st.columns(2)
        with col1:
            preco_a = st.number_input("Preço A (R$)", 120.18, key="pa_m")
            un_a = st.number_input("Rolos A", 12, key="qa_m")
            m_a = st.number_input("Metros por rolo A", 30.0, key="ma_m")

        with col2:
            preco_b = st.number_input("Preço B (R$)", 65.35, key="pb_m")
            un_b = st.number_input("Rolos B", 6, key="qb_m")
            m_b = st.number_input("Metros por rolo B", 20.0, key="mb_m")

        if st.button("Comparar (metragem)", use_container_width=True):
            ta = un_a * m_a
            tb = un_b * m_b
            ra = preco_a / ta
            rb = preco_b / tb
            st.metric("Produto A (R$/m)", f"{ra:.3f}")
            st.metric("Produto B (R$/m)", f"{rb:.3f}")
            st.success("Vale mais a pena: **Produto A**" if ra < rb else "Vale mais a pena: **Produto B**")

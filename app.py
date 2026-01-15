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
        
        if custo_km_e < custo_km_g:
            economia = (custo_km_g - custo_km_e) / custo_km_g * 100
            st.success(f"✅ Vale mais a pena: **Etanol** ({economia:.1f}% mais barato por km)")
        elif custo_km_g < custo_km_e:
            economia = (custo_km_e - custo_km_g) / custo_km_e * 100
            st.success(f"✅ Vale mais a pena: **Gasolina** ({economia:.1f}% mais barato por km)")
        else:
            st.info("Empate: os dois custam igual por km.")
        
        st.markdown("### Custo real por km")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Etanol (R$/km)", f"{custo_km_e:.3f}")
        with c2:
            st.metric("Gasolina (R$/km)", f"{custo_km_g:.3f}")


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

    st.markdown("""
    <div style="
        background-color:#F7F7F7;
        padding:14px 16px;
        border-radius:12px;
        margin-bottom:14px;
        font-size:15px;
        line-height:1.4;
    ">
    <b>ℹ️ Como usar</b><br>
    Os campos <b>Produto A</b> e <b>Produto B</b> representam <b>quaisquer dois produtos que você queira comparar</b>.<br>
    Os valores que aparecem inicialmente são <b>apenas exemplos</b> — substitua pelos preços, volumes, quantidades ou metragem dos produtos reais que você está avaliando.
    </div>
    """, unsafe_allow_html=True)

    sub = st.segmented_control(
        "Tipo de produto",
        options=["📦 Pacotes & Unidades", "🧴 Líquidos & Cremes", "🧻 Papéis & Rolos"],
        default="📦 Pacotes & Unidades",
        key="prod_sub"
    )

    # -----------------------------
    # SUBABA: PACOTES & UNIDADES
    # -----------------------------
    if sub == "📦 Pacotes & Unidades":
        st.caption("Compare por unidade.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Produto A")
            preco_a = st.number_input("Preço A (R$)", value=32.99, min_value=0.0, step=0.10, key="pa_un")
            un_a = st.number_input("Unidades A", value=8, min_value=0, step=1, format="%d", key="qa_un")

        with col2:
            st.markdown("### Produto B")
            preco_b = st.number_input("Preço B (R$)", value=27.90, min_value=0.0, step=0.10, key="pb_un")
            un_b = st.number_input("Unidades B", value=6, min_value=0, step=1, format="%d", key="qb_un")

        if st.button("Comparar (unidades)", use_container_width=True, key="btn_cmp_un"):
            if un_a <= 0 or un_b <= 0:
                st.error("As quantidades (un) precisam ser maiores que zero.")
            else:
                rpu_a = preco_a / un_a
                rpu_b = preco_b / un_b

                # 1️⃣ Decisão
                if rpu_a < rpu_b:
                    st.success("✅ Vale mais a pena: **Produto A**")
                elif rpu_b < rpu_a:
                    st.success("✅ Vale mais a pena: **Produto B**")
                else:
                    st.info("Empate: os dois rendem igual por unidade.")

                # 2️⃣ Valores
                st.metric("Produto A (R$/un)", f"{rpu_a:.2f}")
                st.metric("Produto B (R$/un)", f"{rpu_b:.2f}")

    # -----------------------------
    # SUBABA: LÍQUIDOS & CREMES
    # -----------------------------
    elif sub == "🧴 Líquidos & Cremes":
        st.caption("Compare por volume (mL, L ou m³).")

        def to_ml(valor: float, unidade: str) -> float:
            if unidade == "mL":
                return valor
            if unidade == "L":
                return valor * 1000.0
            if unidade == "m³":
                return valor * 1_000_000.0
            return 0.0

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Produto A")
            preco_a = st.number_input("Preço A (R$)", value=120.18, min_value=0.0, step=0.10, key="pa_vol")
            unidade_a = st.selectbox("Unidade A", ["mL", "L", "m³"], index=0, key="ua_vol")
            vol_a = st.number_input(f"Volume A ({unidade_a})", value=400, min_value=0, step=10, format="%d", key="va_vol")

        with col2:
            st.markdown("### Produto B")
            preco_b = st.number_input("Preço B (R$)", value=65.35, min_value=0.0, step=0.10, key="pb_vol")
            unidade_b = st.selectbox("Unidade B", ["mL", "L", "m³"], index=0, key="ub_vol")
            vol_b = st.number_input(f"Volume B ({unidade_b})", value=200, min_value=0, step=10, format="%d", key="vb_vol")

        if st.button("Comparar (volume)", use_container_width=True, key="btn_cmp_vol"):
            va_ml = to_ml(vol_a, unidade_a)
            vb_ml = to_ml(vol_b, unidade_b)

            if va_ml <= 0 or vb_ml <= 0:
                st.error("Volumes precisam ser maiores que zero.")
            else:
                ra = preco_a / va_ml
                rb = preco_b / vb_ml

                # 1️⃣ Decisão
                if ra < rb:
                    st.success("✅ Vale mais a pena: **Produto A**")
                elif rb < ra:
                    st.success("✅ Vale mais a pena: **Produto B**")
                else:
                    st.info("Empate: os dois rendem igual por volume.")

                # 2️⃣ Valores
                st.metric("Produto A (R$/mL)", f"{ra:.6f}")
                st.metric("Produto B (R$/mL)", f"{rb:.6f}")
                st.caption(f"R\\$ {ra*100:.2f} por 100 mL • R\\$ {ra*1000:.2f} por 1 L")
                st.caption(f"R\\$ {rb*100:.2f} por 100 mL • R\\$ {rb*1000:.2f} por 1 L")


    # -----------------------------
    # SUBABA: PAPÉIS & ROLOS
    # -----------------------------
    elif sub == "🧻 Papéis & Rolos":
        st.caption("Compare por metragem (papel higiênico, papel toalha, filme, alumínio).")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Produto A")
            preco_a = st.number_input("Preço A (R$)", value=66.22, min_value=0.0, step=0.10, key="pa_m")
            rolos_a = st.number_input("Rolos A", value=20, min_value=0, step=1, format="%d", key="qa_m")
            metros_a = st.number_input("Metros por rolo A (m)", value=50, min_value=0, step=1, format="%d", key="ma_m")

        with col2:
            st.markdown("### Produto B")
            preco_b = st.number_input("Preço B (R$)", value=55.98, min_value=0.0, step=0.10, key="pb_m")
            rolos_b = st.number_input("Rolos B", value=24, min_value=0, step=1, format="%d", key="qb_m")
            metros_b = st.number_input("Metros por rolo B (m)", value=20, min_value=0, step=1, format="%d", key="mb_m")

        if st.button("Comparar (metragem)", use_container_width=True, key="btn_cmp_m"):
            total_a = rolos_a * metros_a
            total_b = rolos_b * metros_b

            if total_a <= 0 or total_b <= 0:
                st.error("Metragens precisam ser maiores que zero.")
            else:
                custo_m_a = preco_a / total_a
                custo_m_b = preco_b / total_b

                # 1️⃣ Decisão
                if custo_m_a < custo_m_b:
                    st.success("✅ Vale mais a pena: **Produto A**")
                elif custo_m_b < custo_m_a:
                    st.success("✅ Vale mais a pena: **Produto B**")
                else:
                    st.info("Empate: os dois custam igual por metro.")

                # 2️⃣ Valores
                st.metric("Produto A (R$/m)", f"{custo_m_a:.3f}")
                st.metric("Produto B (R$/m)", f"{custo_m_b:.3f}")

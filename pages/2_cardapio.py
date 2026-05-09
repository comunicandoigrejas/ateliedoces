import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Menu Inicial"): st.switch_page("app.py")

st.header("🍰 Nosso Cardápio")

# Exemplo de item
if st.button("Adicionar Trufa - R$ 4,00"):
    st.session_state.carrinho.append({"item": "Trufa", "preco": 4.00})
    st.toast("Adicionado!")

st.write(f"Itens no carrinho: {len(st.session_state.carrinho)}")

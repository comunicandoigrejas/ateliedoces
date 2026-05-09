import streamlit as st
import os

st.set_page_config(page_title="Página - Ateliê", initial_sidebar_state="collapsed")

# Esconde a barra lateral via CSS
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar para o Menu Inicial"):
    st.switch_page("app.py")

st.divider()
# ... restante do código da página ...
st.set_page_config(page_title="Cardápio - Ateliê", page_icon="🍰")

if 'carrinho' not in st.session_state: st.session_state.carrinho = []

st.header("🍰 Nosso Cardápio")

lista_doces = [
    {"nome": "Trufas", "preco": 4.00, "img": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "img": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "img": "assets/paodemel1.png"},
    {"nome": "Kit 4 Trufas", "preco": 15.00, "img": "assets/trufas4unidades1.png"}
]

for doce in lista_doces:
    c1, c2 = st.columns([1, 2])
    with c1:
        if os.path.exists(doce['img']): st.image(doce['img'], width=150)
    with c2:
        st.subheader(doce['nome'])
        st.write(f"Preço: R$ {doce['preco']:.2f}")
        if st.button(f"Adicionar", key=doce['nome']):
            st.session_state.carrinho.append(doce)
            st.toast(f"{doce['nome']} no carrinho!")

st.divider()
if st.button("Finalizar Pedido 🛒"):
    st.switch_page("pages/3_🛒_Pedidos.py")

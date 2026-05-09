import streamlit as st

st.set_page_config(page_title="Página - Ateliê", initial_sidebar_state="collapsed")

# Esconde a barra lateral via CSS
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar para o Menu Inicial"):
    st.switch_page("app.py")

st.divider()
# ... restante do código da página ...
import streamlit as st
import requests

st.set_page_config(initial_sidebar_state="collapsed")
URL_PLANILHA = "SUA_URL_AQUI"

st.header("🛒 Seu Carrinho")

if not st.session_state.carrinho:
    st.warning("Seu carrinho está vazio!")
else:
    total = sum(item['preco'] for item in st.session_state.carrinho)
    for item in st.session_state.carrinho:
        st.write(f"- {item['item']}: R$ {item['preco']:.2f}")
    
    st.subheader(f"Total: R$ {total:.2f}")
    st.info(f"✨ Com esta compra você ganhará {int(total)} pontos!")

    if st.button("Confirmar Pedido"):
        # Enviar para a planilha
        st.success("Pedido enviado com sucesso!")
        st.session_state.carrinho = [] # Limpa após enviar

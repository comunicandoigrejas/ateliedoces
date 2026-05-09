import streamlit as st
import os

st.set_page_config(page_title="Ateliê Denise Borges", page_icon="🧁", layout="centered", initial_sidebar_state="collapsed")

# 1. INICIALIZAR CARRINHO (Fundamental para não sumir)
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

# Logo
if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=200)

st.title("Bem-vindo ao Ateliê!")

# LOGIN SIMPLES
if not st.session_state.usuario:
    zap = st.text_input("Para entrar, digite seu WhatsApp (apenas números):")
    if st.button("Entrar"):
        if zap == "240805": # Coloque seu número aqui para ser o Admin
            st.session_state.usuario = {"nome": "Denise", "tipo": "admin", "zap": zap}
        else:
            st.session_state.usuario = {"nome": "Cliente", "tipo": "cliente", "zap": zap}
        st.rerun()
else:
    st.write(f"Olá, bem-vindo(a)!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍰 Ver Cardápio"): st.switch_page("pages/2_cardapio.py")
        if st.button("🛒 Meu Carrinho"): st.switch_page("pages/3_pedidos.py")
    with col2:
        if st.button("🚚 Rastreio"): st.switch_page("pages/4_rastreio.py")
        if st.button("👤 Meu Cadastro"): st.switch_page("pages/1_cadastro.py")

    # BOTÃO SECRETO SÓ PARA A DENISE
    if st.session_state.usuario['tipo'] == "admin":
        st.divider()
        if st.button("🔐 PAINEL ADMINISTRATIVO"):
            st.switch_page("pages/5_admin.py")

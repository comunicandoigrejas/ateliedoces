import streamlit as st
import os

# Configuração para esconder a barra lateral (initial_sidebar_state="collapsed")
st.set_page_config(
    page_title="Ateliê Denise Borges", 
    page_icon="🧁", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para esconder o botão de abrir a barra lateral e estilizar os botões
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 3.5em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    # Verificamos se o caminho está correto. Se o logo sumiu, 
    # confirme se a pasta no GitHub se chama 'assets' (minúsculo)
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        # Se não achar o arquivo, ele avisa onde o Python está procurando
        st.error(f"Logo não encontrado em: {caminho}")

# Exibição do Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    exibir_imagem("assets/logo.png", 220)

st.markdown("<h1 style='text-align: center;'>Ateliê Denise Borges</h1>", unsafe_allow_html=True)
st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8 (ARA)")

st.write("### O que deseja fazer hoje, abençoado(a)?")

col_a, col_b = st.columns(2)
with col_a:
    if st.button("👤 Fazer Cadastro"):
        st.switch_page("pages/1_cadastro.py")
    if st.button("🍰 Ver Cardápio"):
        st.switch_page("pages/2_cardapio.py")

with col_b:
    if st.button("🛒 Ver Carrinho"):
        st.switch_page("pages/3_pedidos.py")
    if st.button("🚚 Rastreio"):
        st.switch_page("pages/4_rastreio.py")

import streamlit as st
import os

st.set_page_config(page_title="Início - Ateliê Denise Borges", page_icon="🧁", layout="centered")

# Estilização para os botões ficarem bonitos e centralizados
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #4B0082 !important; }
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 3.5em;
        width: 100%;
        margin-bottom: 10px;
    }
    div.stButton > button:hover { background-color: #FFB6C1; color: #4B0082 !important; }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Ateliê+Denise+Borges", width=largura)

# Centralizando a Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    exibir_imagem("assets/logo.png", 220)

st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8 (ARA)")

st.write("### O que deseja fazer hoje, abençoado(a)?")

# Criando botões de atalho para as páginas
col_a, col_b = st.columns(2)

with col_a:
    if st.button("👤 Fazer Meu Cadastro"):
        st.switch_page("pages/1_👤_Cadastro.py")
    
    if st.button("🍰 Ver Cardápio"):
        st.switch_page("pages/2_🍰_Cardapio.py")

with col_b:
    if st.button("🚚 Rastrear Pedido"):
        st.switch_page("pages/4_🚚_Rastreio.py")
    
    if st.button("🛒 Ver Meu Carrinho"):
        st.switch_page("pages/3_🛒_Pedidos.py")

st.divider()
st.caption("Você também pode navegar pelo menu no canto esquerdo da tela.")

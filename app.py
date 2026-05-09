import streamlit as st
import os

st.set_page_config(page_title="Início - Ateliê Denise Borges", page_icon="🧁", layout="centered")

# Estilo para os botões ocuparem a largura total e ficarem destacados
st.markdown("""
    <style>
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

# Título e Logo
st.markdown("<h1 style='text-align: center;'>Ateliê Denise Borges</h1>", unsafe_allow_html=True)

# Botões de Navegação - O caminho deve ser EXATAMENTE como está na pasta
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

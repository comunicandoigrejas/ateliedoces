import streamlit as st
import os

st.set_page_config(page_title="Início - Ateliê Denise Borges", page_icon="🧁", layout="centered")

# Estilo Global (Roxo e Rosa)
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #4B0082 !important; }
    div.stButton > button { background-color: #8E44AD; color: white !important; border-radius: 15px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Logo+Atelie", width=largura)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    exibir_imagem("assets/logo.png", 250)

st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Ateliê Denise Borges</h1>", unsafe_allow_html=True)
st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8 (ARA)")

st.write("### A paz do Senhor, irmão(ã)!")
st.write("Ficamos felizes em ter você aqui. Use o menu lateral para navegar e conhecer nossas delícias.")

if st.button("Ver Cardápio Agora"):
    st.switch_page("pages/2_🍰_Cardapio.py")

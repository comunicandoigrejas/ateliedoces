import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse
import requests

# Substitua pela URL que você copiou do Google
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbx0jYmFYArWmPBfOXYZDcvRKfF8BmzNF3S1U-mSr_WAHsMN71tLztUfMBbfs76Eaz44zA/exec"

def salvar_na_planilha(nome, whatsapp, pedido, total):
    dados = {
        "nome": nome,
        "whatsapp": whatsapp,
        "pedido": pedido,
        "total": float(total)
    }
    try:
        # Envia os dados para o Google Sheets
        requests.post(URL_PLANILHA, json=dados)
        return True
    except:
        return False
# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CSS (Fontes Roxas no Geral e Brancas nos Botões) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0F5;
    }
    
    /* Texto Geral em Roxo */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #4B0082 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* FORÇANDO FONTE BRANCA NOS BOTÕES (Padrão e Link) */
    div.stButton > button, 
    div.stButton > button p, 
    div.stButton > button span,
    .stLinkButton a,
    .stLinkButton a p,
    .stLinkButton a span {
        color: white !important;
    }

    /* Cores dos Botões Padrão */
    div.stButton > button {
        background-color: #8E44AD; 
        border-radius: 15px;
        font-weight: bold;
    }
    
    div.stButton > button:hover {
        background-color: #2980B9;
    }

    /* Ajuste para inputs não ficarem brancos */
    .stTextInput input {
        color: #4B0082 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Doce+Abençoado", width=largura)

if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'pontos' not in st.session_state:
    st.session_state.pontos = {}
if 'status_pedidos' not in st.session_state:
    st.session_state.status_pedidos = {}

# --- MENU ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Contato", "Admin"],
    icons=["house", "book", "cart4", "truck", "chat-dots", "shield-lock"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff"},
        "nav-link": {"color": "#4B0082", "font-size": "13px"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"},
    }
)

lista_doces = [
    {"nome": "Trufas", "preco": 4.00, "img": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "img": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "img": "assets/paodemel1.png"},
    {"nome": "Trufas (4 unidades)", "preco": 15.00, "img": "assets/trufas4unidades1.png"}
]

if selected == "Início":
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        exibir_imagem("assets/logo.png", 220) 
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Bem-vindo(a), abençoado(a)!")
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    for doce in lista_doces:
        c1, c2 = st.columns([1, 2])
        with c1:
            exibir_imagem(doce["img"], 140) 
        with c2:
            st.subheader(doce["nome"])
            st.write(f"Valor: **R$ {doce['preco']:.2f}**")
            if st.button(f"Adicionar {doce['nome']}", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} adicionado!")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Seu Pedido")
    id_cliente = st.text_input("WhatsApp (apenas números)")
    if id_cliente:
        pts = st.session_state.pontos.get(id_cliente, 0)
        st.write(f"✨ **Seus Pontos:** {pts}")

    if not st.session_state.carrinho:
        st.warning("O carrinho está vazio, irmão.")
    else:
        df_cart = pd.DataFrame(st.session_state.carrinho)
        resumo = df_cart.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Qtd', 'Subtotal']
        st.table(resumo)
        total_geral = resumo['Subtotal'].sum()
        st.markdown(f"### **Total: R$ {total_geral:.2f}**")
        
        nome_contato = st.text_input("Seu Nome")
  File "/mount/src/ateliedoces/app.py", line 142
      if nome_contato and id_cliente:
      ^
IndentationError: expected an indented block after 'if' statement on line 141
elif selected == "Rastreio":
    st.header("🚚 Rastreio")
    busca = st.text_input("Seu WhatsApp:")
    if busca in st.session_state.status_pedidos:
        st.success(f"Status: **{st.session_state.status_pedidos[busca]}**")
    elif busca:
        st.error("Nenhum pedido encontrado.")

elif selected == "Contato":
    st.header("📞 Fale Conosco")
    st.write("Estamos à disposição para atender você com todo carinho!")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("WhatsApp")
        msg_padrao = urllib.parse.quote("Vim pelo Aplicativo, e quero mais informações")
        link_whatsapp = f"https://api.whatsapp.com/send?phone=5519992709717&text={msg_padrao}"
        st.markdown(f'''
            <a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white !important; padding:10px; 
                text-align:center; border-radius:10px; font-weight:bold;">
                    ABRIR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    with col2:
        st.subheader("Instagram")
        st.link_button("Seguir no Instagram", "https://www.instagram.com/deniseborges.doces")
    st.write("---")
    exibir_imagem("assets/logo.png", 180)

elif selected == "Admin":
    st.header("🔐 Admin")
    if st.text_input("Senha", type="password") == "denise123":
        for zap, stat in st.session_state.status_pedidos.items():
            st.write(f"Cliente: {zap}")
            novo = st.selectbox("Mudar Status", ["Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue"], key=zap)
            if st.button(f"Atualizar {zap}"):
                st.session_state.status_pedidos[zap] = novo
                st.rerun()

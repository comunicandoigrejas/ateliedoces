import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse
import requests

# URL do seu Apps Script
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbyM8IUPE7mo9ilgf5Yo2xB0JK4VZrsSnCVXLaK2Hj_lkYcNrlhbRB8zaL5IZshJdJCyxA/exec"

# --- FUNÇÕES DE COMUNICAÇÃO ---
def salvar_na_planilha(nome, whatsapp, pedido, total):
    dados = {"action": "create", "nome": nome, "whatsapp": whatsapp, "pedido": pedido, "total": float(total)}
    try:
        requests.post(URL_PLANILHA, json=dados)
        return True
    except: return False

def buscar_dados_planilha():
    try:
        resposta = requests.get(URL_PLANILHA, timeout=10)
        return resposta.json() if resposta.status_code == 200 else []
    except: return []

def atualizar_status_na_planilha(whatsapp, novo_status):
    dados = {"action": "update", "whatsapp": whatsapp, "status": novo_status}
    try:
        requests.post(URL_PLANILHA, json=dados)
        return True
    except: return False

# --- CONFIGURAÇÕES E ESTILO ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #4B0082 !important; }
    div.stButton > button { background-color: #8E44AD; color: white !important; border-radius: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Doce+Abençoado", width=largura)

if 'carrinho' not in st.session_state: st.session_state.carrinho = []

# --- MENU ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    orientation="horizontal"
)

# --- TRATAMENTO DE ERRO DE NÚMERO ---
def limpar_valor(valor):
    try:
        if not valor or valor == "": return 0.0
        # Remove R$, espaços e troca vírgula por ponto
        v = str(valor).replace('R$', '').replace(' ', '').replace(',', '.').strip()
        return float(v)
    except:
        return 0.0

# --- ABAS ---
if selected == "Início":
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c: exibir_imagem("assets/logo.png", 220) 
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    lista_doces = [
        {"nome": "Trufas", "preco": 4.00, "img": "assets/trufas1.png"},
        {"nome": "Cone Trufado", "preco": 8.00, "img": "assets/conetrufado1.png"},
        {"nome": "Pão de Mel", "preco": 8.00, "img": "assets/paodemel1.png"},
        {"nome": "Kit 4 Trufas", "preco": 15.00, "img": "assets/trufas4unidades1.png"}
    ]
    for doce in lista_doces:
        c1, c2 = st.columns([1, 2])
        with c1: exibir_imagem(doce["img"], 140) 
        with c2:
            st.subheader(doce["nome"])
            st.write(f"Valor: **R$ {doce['preco']:.2f}**")
            if st.button(f"Adicionar", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} adicionado!")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Checkout")
    id_cliente = st.text_input("WhatsApp (apenas números)")
    if id_cliente:
        dados = buscar_dados_planilha()
        # USANDO A FUNÇÃO limpar_valor PARA NÃO DAR ERRO
        pts = sum(limpar_valor(item.get('total', 0)) for item in dados if str(item.get('whatsapp')) == id_cliente)
        st.write(f"✨ **Seus Pontos:** {int(pts)}")

    if st.session_state.carrinho:
        total = sum(d['preco'] for d in st.session_state.carrinho)
        st.write(f"### Total: R$ {total:.2f}")
        nome = st.text_input("Seu Nome")
        if st.button("Finalizar Pedido"):
            resumo = ", ".join([d['nome'] for d in st.session_state.carrinho])
            if salvar_na_planilha(nome, id_cliente, resumo, total):
                st.success("Pedido Salvo!")
                st.session_state.carrinho = []

elif selected == "Rastreio":
    st.header("🚚 Rastreio")
    busca = st.text_input("WhatsApp:")
    if busca:
        dados = buscar_dados_planilha()
        pedido = next((item for item in reversed(dados) if str(item.get('whatsapp')) == busca), None)
        if pedido: st.success(f"Status: **{pedido.get('status')}**")

elif selected == "Admin":
    st.header("🔐 Admin")
    if st.text_input("Senha", type="password") == "denise123":
        dados = buscar_dados_planilha()
        for i, item in enumerate(dados):
            whatsapp = str(item.get('whatsapp'))
            with st.expander(f"Pedido: {item.get('nome')} ({whatsapp})"):
                opcoes = ["Aguardando Confirmação", "Confirmado", "Em Preparo", "Entregue"]
                status_atual = item.get('status', "Aguardando Confirmação")
                idx = opcoes.index(status_atual) if status_atual in opcoes else 0
                
                novo = st.selectbox("Mudar Status", opcoes, index=idx, key=f"sel_{whatsapp}_{i}")
                if st.button("Gravar", key=f"btn_{whatsapp}_{i}"):
                    if atualizar_status_na_planilha(whatsapp, novo):
                        st.success("Status Atualizado!")
                        st.rerun()

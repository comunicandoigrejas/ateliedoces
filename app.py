import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse
import requests

# URL do seu Apps Script (Mantenha sempre a versão mais recente publicada)
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbyM8IUPE7mo9ilgf5Yo2xB0JK4VZrsSnCVXLaK2Hj_lkYcNrlhbRB8zaL5IZshJdJCyxA/exec"

# --- FUNÇÕES DE COMUNICAÇÃO (Falam com o Apps Script) ---

def salvar_na_planilha(nome, whatsapp, pedido, total):
    dados = {
        "action": "create",
        "nome": nome, 
        "whatsapp": whatsapp, 
        "pedido": pedido, 
        "total": float(total)
    }
    try:
        requests.post(URL_PLANILHA, json=dados)
        return True
    except:
        return False

def buscar_dados_planilha():
    try:
        # O timeout evita que o app trave se o Google demorar a responder
        resposta = requests.get(URL_PLANILHA, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()
        return []
    except:
        return []

def atualizar_status_na_planilha(whatsapp, novo_status):
    dados = {
        "action": "update",
        "whatsapp": whatsapp,
        "status": novo_status
    }
    try:
        requests.post(URL_PLANILHA, json=dados)
        return True
    except:
        return False

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# Estilização visual (Roxo e Rosa)
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #4B0082 !important; }
    div.stButton > button { background-color: #8E44AD; color: white !important; border-radius: 15px; font-weight: bold; }
    div.stButton > button:hover { background-color: #2980B9; }
    </style>
    """, unsafe_allow_html=True)

if 'carrinho' not in st.session_state: st.session_state.carrinho = []

# --- MENU DE NAVEGAÇÃO ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    orientation="horizontal"
)

# --- LÓGICA DAS ABAS ---

if selected == "Início":
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    lista_doces = [
        {"nome": "Trufas", "preco": 4.00}, 
        {"nome": "Cone Trufado", "preco": 8.00}, 
        {"nome": "Pão de Mel", "preco": 8.00},
        {"nome": "Trufas (4 unidades)", "preco": 15.00}
    ]
    for doce in lista_doces:
        col1, col2 = st.columns([2, 1])
        with col1: st.write(f"**{doce['nome']}** - R$ {doce['preco']:.2f}")
        with col2:
            if st.button(f"Adicionar", key=f"add_{doce['nome']}"):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} adicionado ao carrinho!")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Finalizar Pedido")
    id_cliente = st.text_input("Seu WhatsApp (apenas números)")
    
    if id_cliente:
        dados = buscar_dados_planilha()
        # Soma os pontos baseados na coluna 'total' da planilha
        pts = sum(float(item.get('total', 0)) for item in dados if str(item.get('whatsapp')) == id_cliente)
        st.write(f"✨ **Seus Pontos Acumulados:** {int(pts)}")

    if not st.session_state.carrinho:
        st.warning("O carrinho está vazio, irmão.")
    else:
        total_geral = sum(d['preco'] for d in st.session_state.carrinho)
        st.write(f"### Total do Pedido: R$ {total_geral:.2f}")
        nome_contato = st.text_input("Seu Nome")
        
        if st.button("Confirmar e Salvar Pedido"):
            if nome_contato and id_cliente:
                # Criamos um resumo simples para a planilha
                resumo_txt = ", ".join([d['nome'] for d in st.session_state.carrinho])
                if salvar_na_planilha(nome_contato, id_cliente, resumo_txt, total_geral):
                    st.success("Pedido registrado com sucesso na planilha!")
                    st.session_state.carrinho = [] # Limpa o carrinho
                else:
                    st.error("Erro ao salvar. Verifique sua conexão.")
            else:
                st.error("Preencha nome e WhatsApp para continuar.")

elif selected == "Rastreio":
    st.header("🚚 Rastreio de Pedidos")
    busca = st.text_input("Digite seu WhatsApp para consultar:")
    if busca:
        dados = buscar_dados_planilha()
        # Pega o último pedido feito por esse número
        pedido = next((item for item in reversed(dados) if str(item.get('whatsapp')) == busca), None)
        if pedido:
            st.success(f"Olá {pedido.get('nome')}! O status do seu pedido é: **{pedido.get('status')}**")
        else:
            st.warning("Nenhum pedido encontrado para este número.")

elif selected == "Admin":
    st.header("🔐 Painel da Denise")
    if st.text_input("Senha de Acesso", type="password") == "denise123":
        dados = buscar_dados_planilha()
        if not dados:
            st.info("Aguardando os primeiros pedidos...")
        else:
            for i, item in enumerate(dados):
                whatsapp = str(item.get('whatsapp'))
                nome = item.get('nome', 'Sem nome')
                status_atual = item.get('status', 'Aguardando Confirmação')
                
                with st.expander(f"Pedido de {nome} ({whatsapp})"):
                    opcoes = ["Aguardando Confirmação", "Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue"]
                    idx = opcoes.index(status_atual) if status_atual in opcoes else 0
                    
                    # Chave única para evitar erro de duplicidade
                    novo_st = st.selectbox("Atualizar Status:", opcoes, index=idx, key=f"sel_{whatsapp}_{i}")
                    
                    if st.button("Gravar Alteração", key=f"btn_{whatsapp}_{i}"):
                        if atualizar_status_na_planilha(whatsapp, novo_st):
                            st.success("Status atualizado com sucesso!")
                            st.rerun()
                st.write("---")

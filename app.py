import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse
import requests

# Sua URL do Apps Script
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwMZdOsNj3ffgu4vyJxASUdkckobH9sdresxItUiyj39AGmsFLRuyk-x9395F465E5PIg/exec"

def salvar_na_planilha(nome, whatsapp, pedido, total):
    # Adicionamos a 'action': 'create'
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

def atualizar_status_na_planilha(whatsapp, novo_status):
    # Adicionamos a 'action': 'update'
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

# Estilização
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #4B0082 !important; }
    div.stButton > button { background-color: #8E44AD; color: white !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'carrinho' not in st.session_state: st.session_state.carrinho = []

selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    orientation="horizontal"
)

if selected == "Início":
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.info("📖 Provai e vede que o Senhor é bom. - Salmos 34:8")

elif selected == "Cardápio":
    lista_doces = [{"nome": "Trufas", "preco": 4.00}, {"nome": "Cone Trufado", "preco": 8.00}, {"nome": "Pão de Mel", "preco": 8.00}]
    for doce in lista_doces:
        col1, col2 = st.columns([2, 1])
        with col1: st.write(f"**{doce['nome']}** - R$ {doce['preco']:.2f}")
        with col2:
            if st.button(f"Adicionar", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} no carrinho!")

elif selected == "Pedidos & Pontos":
    id_cliente = st.text_input("WhatsApp (apenas números)")
    if id_cliente:
        dados = buscar_dados_planilha()
        total_pts = sum(float(item.get('total', 0)) for item in dados if str(item.get('whatsapp')) == id_cliente)
        st.write(f"✨ Seus Pontos: {int(total_pts)}")

    if st.session_state.carrinho:
        total = sum(d['preco'] for d in st.session_state.carrinho)
        st.write(f"### Total: R$ {total:.2f}")
        nome = st.text_input("Seu Nome")
        if st.button("Finalizar Pedido"):
            if salvar_na_planilha(nome, id_cliente, "Pedido App", total):
                st.success("Pedido Salvo na Planilha!")

elif selected == "Rastreio":
    busca = st.text_input("WhatsApp para Rastrear:")
    if busca:
        dados = buscar_dados_planilha()
        pedido = next((item for item in reversed(dados) if str(item.get('whatsapp')) == busca), None)
        if pedido:
            st.success(f"Status: **{pedido.get('status')}**")

elif selected == "Admin":
    st.header("🔐 Painel Admin")
    if st.text_input("Senha", type="password") == "denise123":
        dados = buscar_dados_planilha()
        if not dados:
            st.info("Nenhum pedido encontrado na planilha.")
        else:
            # Usamos enumerate para ter um número único (i) para cada pedido
            for i, item in enumerate(dados):
                nome_cliente = item.get('nome', 'Cliente sem nome')
                whatsapp_cliente = item.get('whatsapp', 'Sem Zap')
                status_atual = item.get('status', 'Aguardando Confirmação')
                
                # Criamos uma chave única combinando o Zap com o índice da linha
                chave_unica = f"{whatsapp_cliente}_{i}"
                
                with st.expander(f"Pedido {i+1}: {nome_cliente}"):
                    st.write(f"**WhatsApp:** {whatsapp_cliente}")
                    st.write(f"**Pedido:** {item.get('pedido', 'Não informado')}")
                    
                    # Lista de opções para o Selectbox
                    opcoes = ["Aguardando Confirmação", "Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue"]
                    
                    # Tenta marcar a opção atual como padrão
                    indice_padrao = opcoes.index(status_atual) if status_atual in opcoes else 0
                    
                    novo = st.selectbox(
                        "Mudar Status", 
                        opcoes, 
                        index=indice_padrao,
                        key=f"sel_{chave_unica}" # Chave Única garantida!
                    )
                    
                    if st.button("Atualizar Status", key=f"btn_{chave_unica}"):
                        if atualizar_status_na_planilha(whatsapp_cliente, novo):
                            st.success(f"Status de {nome_cliente} atualizado!")
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar na planilha.")
                st.write("---")

import streamlit as st
import requests
import os

st.set_page_config(page_title="Ateliê Denise Borges", page_icon="🧁", layout="centered", initial_sidebar_state="collapsed")

# URL do seu Apps Script
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbxLIgR7YPRDnMCuWBh1gnfzH0U2JhH9UrOkXkZMmb4nerzTYimOWu2bGQoHw1tu5KQnSA/exec"

# Inicializa as variáveis de memória (Session State)
if 'carrinho' not in st.session_state: st.session_state.carrinho = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# Esconde barra lateral e estiliza botões
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    div.stButton > button { background-color: #8E44AD; color: white !important; border-radius: 15px; font-weight: bold; height: 3.5em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Logo
if os.path.exists("assets/logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.image("assets/logo.png", width=220)

st.markdown("<h1 style='text-align: center;'>Ateliê Denise Borges</h1>", unsafe_allow_html=True)

# --- LÓGICA DE ACESSO ---
if st.session_state.usuario is None:
    st.subheader("Olá! Para continuar, informe seu WhatsApp:")
    zap_login = st.text_input("WhatsApp (apenas números):", placeholder="Ex: 19999999999")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
      # Dentro do botão de Entrar no app.py
if st.button("Entrar"):
    if zap_login:
        try:
            resposta = requests.get(URL_PLANILHA).json()
            # Note que agora pegamos especificamente a parte 'clientes'
            lista_clientes = resposta.get('clientes', [])
            
            # Procuramos o zap na coluna index 2 (WhatsApp)
            encontrado = next((c for c in lista_clientes if str(c[2]) == zap_login), None)
            
            if encontrado:
                st.session_state.usuario = {"nome": encontrado[1], "zap": zap_login, "tipo": "cliente"}
                if zap_login == "240805": # Defina seu número admin
                    st.session_state.usuario["tipo"] = "admin"
                st.rerun()
            else:
                st.error("Número não encontrado. Por favor, cadastre-se primeiro!")
        except Exception as e:
            st.error("Erro ao buscar dados. Verifique se a aba 'clientes' existe na planilha.")

    with col_btn2:
        if st.button("Sou Novo (Cadastrar)"):
            st.switch_page("pages/1_cadastro.py")

# --- MENU APÓS LOGIN ---
else:
    st.write(f"### Olá, {st.session_state.usuario['nome']}! 👋")
    
    # Se for a Denise, mostra o botão de Admin
    if st.session_state.usuario['tipo'] == "admin":
        if st.button("🔐 ACESSAR PAINEL ADMINISTRATIVO"):
            st.switch_page("pages/5_admin.py")
        st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🍰 Ver Cardápio"): st.switch_page("pages/2_cardapio.py")
        if st.button("🚚 Meus Pedidos"): st.switch_page("pages/4_rastreio.py")
    with col_b:
        if st.button("🛒 Ver Carrinho"): st.switch_page("pages/3_pedidos.py")
        if st.button("🚪 Sair"):
            st.session_state.usuario = None
            st.rerun()

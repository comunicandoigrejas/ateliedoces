import streamlit as st
import requests
import os

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre a primeira linha de código)
st.set_page_config(
    page_title="Ateliê Denise Borges", 
    page_icon="🧁", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÕES DE ACESSO ---
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbzUgW_aJbbZRPpdoKgwpNDOc-4-f1sEKvhOMgC5xMCiPIo5Ytz-SrVLYm98peH3A-Ca3Q/exec" 
WHATSAPP_ADMIN = "19992709717" 

# --- INICIALIZAÇÃO DA MEMÓRIA (Session State) ---
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; } 
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 3.5em;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #FFB6C1; 
        color: #4B0082 !important;
    }
    h1, h2, h3 { color: #4B0082 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO COM LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=220)
    else:
        st.markdown("### 🧁 Ateliê Denise Borges")

# --- LÓGICA DE NAVEGAÇÃO / ACESSO ---

if st.session_state.usuario is None:
    st.markdown("## Bem-vindo(a)!")
    st.write("Para continuar, informe seu WhatsApp cadastrado:")
    
    zap_login = st.text_input("WhatsApp (apenas números)", placeholder="Ex: 19988776655")
    
    col_entrar, col_novo = st.columns(2)
    
    with col_entrar:
        if st.button("Entrar"):
            if zap_login:
                try:
                    with st.spinner("Verificando cadastro..."):
                        resposta = requests.get(URL_PLANILHA).json()
                        lista_clientes = resposta.get('clientes', [])
                        
                        # Limpa o zap digitado (remove espaços e possíveis .0)
                        zap_digitado = str(zap_login).strip().replace(".0", "")
                        
                        cliente = None
                        for c in lista_clientes:
                            # Compara limpando o formato que vem da planilha também
                            if str(c[2]).strip().replace(".0", "") == zap_digitado:
                                cliente = c
                                break
                        
                        if cliente:
                            zap_configurado = str(WHATSAPP_ADMIN).strip().replace(".0", "")
                            
                            # Define se é Admin ou Cliente
                            tipo_usuario = "admin" if zap_digitado == zap_configurado else "cliente"
                            
                            st.session_state.usuario = {
                                "nome": cliente[1], 
                                "zap": zap_digitado, 
                                "tipo": tipo_usuario
                            }
                            st.success(f"A paz do Senhor, {cliente[1]}!")
                            st.rerun()
                        else:
                            st.error("Número não encontrado. Por favor, faça seu cadastro.")
                except Exception as e:
                    st.error(f"Erro técnico: {e}")
            else:
                st.warning("Por favor, digite seu número.")

    with col_novo:
        if st.button("Sou Novo (Cadastrar)"):
            st.switch_page("pages/1_cadastro.py")

else:
    st.markdown(f"## Olá, {st.session_state.usuario['nome']}!")
    st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8 (ARA)")

    # ÁREA DO ADMIN
    if st.session_state.usuario['tipo'] == "admin":
        st.subheader("🛠️ Painel de Gestão")
        if st.button("📊 ACESSAR ADMINISTRAÇÃO"):
            st.switch_page("pages/5_admin.py")
        st.divider()

    # MENU PRINCIPAL
    st.write("### O que deseja fazer?")
    
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🍰 Ver Cardápio"):
            st.switch_page("pages/2_cardapio.py")
        if st.button("🛒 Ver Meu Carrinho"):
            st.switch_page("pages/3_pedidos.py")
            
    with m2:
        if st.button("🚚 Rastrear Pedidos"):
            st.switch_page("pages/4_rastreio.py")
        if st.button("🚪 Sair / Trocar Conta"):
            st.session_state.usuario = None
            st.session_state.carrinho = []
            st.rerun()

    st.divider()
    st.caption("Ateliê Doces Denise Borges - Doces feitos com amor e benção!")

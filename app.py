import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Ateliê Denise Borges", 
    page_icon="🧁", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ====================== CONFIGURAÇÕES ======================
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"
WHATSAPP_ADMIN = "19992009129"

# ====================== SESSION STATE ======================
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# ====================== CSS GLOBAL ======================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    
    /* Fontes pretas e legíveis */
    h1, h2, h3, h4, .stMarkdown, p, label, .stRadio, .stSelectbox {
        color: #1a1a1a !important;
    }
    
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 3.8em;
        width: 100%;
        border: none;
        font-size: 1.05em;
    }
    div.stButton > button:hover {
        background-color: #9B59B6;
        color: white !important;
    }
    
    .stSuccess { background-color: #d4edda; color: #155724; }
    .stError { background-color: #f8d7da; color: #721c24; }
    </style>
    """, unsafe_allow_html=True)

# ====================== CABEÇALHO ======================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=240)
    else:
        st.title("🧁 Ateliê Denise Borges")

# ====================== LÓGICA ======================
if st.session_state.usuario is None:
    st.markdown("## Bem-vindo(a)!")
    st.write("Para continuar, informe seu WhatsApp cadastrado:")

    zap_login = st.text_input("WhatsApp (apenas números)", placeholder="Ex: 19988776655", key="zap_login")

    col_entrar, col_novo = st.columns(2)
    with col_entrar:
        if st.button("Entrar", type="primary"):
            if zap_login:
                with st.spinner("Verificando cadastro..."):
                    try:
                        resposta = requests.get(URL_PLANILHA).json()
                        lista_clientes = resposta.get('clientes', [])

                        zap_digitado = str(zap_login).strip().replace(".0", "")
                        cliente = None
                        for c in lista_clientes:
                            if str(c[2]).strip().replace(".0", "") == zap_digitado:
                                cliente = c
                                break

                        if cliente:
                            tipo_usuario = "admin" if zap_digitado == WHATSAPP_ADMIN else "cliente"
                            st.session_state.usuario = {
                                "nome": cliente[1], 
                                "zap": zap_digitado, 
                                "tipo": tipo_usuario
                            }
                            st.success(f"A paz do Senhor, {cliente[1]}! 🙏")
                            st.rerun()
                        else:
                            st.error("Número não encontrado. Faça seu cadastro.")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
            else:
                st.warning("Digite seu número de WhatsApp.")

    with col_novo:
        if st.button("Sou Novo (Cadastrar)"):
            st.switch_page("pages/1_cadastro.py")

else:
    st.markdown(f"## Olá, {st.session_state.usuario['nome']}! 👋")
    st.info("📖 'Provai e vede que o Senhor é bom...' - Salmos 34:8")

    # ADMIN
    if st.session_state.usuario['tipo'] == "admin":
        st.subheader("🛠️ Painel Administrativo")
        if st.button("📊 Acessar Administração", type="primary"):
            st.switch_page("pages/5_admin.py")
        st.divider()

    # MENU CLIENTE
    st.write("### O que deseja fazer hoje?")

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
    st.caption("Ateliê Doces Denise Borges - Feito com amor e benção ❤️")

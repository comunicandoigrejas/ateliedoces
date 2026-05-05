import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mercadopago

# --- CONFIGURAÇÕES E ESTILO ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁")

st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; } /* Fundo Rosa Claro */
    h1, h2, h3 { color: #5D4037; font-family: 'Arial'; }
    /* Estilização dos botões com sua paleta */
    div.stButton > button {
        border-radius: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .btn-roxo { background-color: #8E44AD; color: white; }
    .btn-verde { background-color: #27AE60; color: white; }
    .btn-azul { background-color: #2980B9; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INTEGRAÇÃO MERCADO PAGO ---
# O token deve ser configurado nos Secrets do Streamlit Cloud
try:
    sdk = mercadopago.SDK(st.secrets["MP_ACCESS_TOKEN"])
except:
    sdk = None

def gerar_pagamento(itens, total):
    if not sdk: return "#"
    preference_data = {
        "items": [{"title": "Pedido Ateliê Denise", "quantity": 1, "unit_price": float(total), "currency_id": "BRL"}],
        "back_urls": {"success": "https://share.streamlit.io/"},
        "auto_return": "approved",
    }
    result = sdk.preference().create(preference_data)
    return result["response"]["init_point"]

# --- BANCO DE DADOS (SESSION STATE) ---
if 'carrinho' not in st.session_state: st.session_state.carrinho = []
if 'pontos' not in st.session_state: st.session_state.pontos = {}
if 'status' not in st.session_state: st.session_state.status = {}

# --- MENU ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"},
    }
)

# --- PRODUTOS ---
doces = [
    {"nome": "Brigadeiro Gourmet", "preco": 5.0, "img": "assets/logo.jpg"},
    {"nome": "Bolo de Pote", "preco": 15.0, "img": "assets/logo.jpg"},
    {"nome": "Copo da Felicidade", "preco": 22.0, "img": "assets/logo.jpg"}
]

# --- LÓGICA DAS TELAS ---

if selected == "Início":
    # Logo diminuído conforme solicitado
    st.image("assets/logo.jpg", width=250) 
    st.title("Ateliê Doces Denise Borges")
    st.write("---")
    st.subheader("Bem-vindo, abençoado(a)!")
    st.write("Doces artesanais feitos para a glória de Deus e alegria do seu coração.")
    # Versão ARA conforme solicitado
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    for d in doces:
        col1, col2 = st.columns([1, 2])
        with col1: st.image(d["img"], width=130)
        with col2:
            st.subheader(d["nome"])
            st.write(f"Preço: R$ {d['preco']:.2f}")
            if st.button(f"Adicionar {d['nome']}", key=d['nome']):
                st.session_state.carrinho.append(d)
                st.toast(f"{d['nome']} na cesta!", icon="🧁")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Finalizar Pedido")
    
    # Login e Pontos
    whats = st.text_input("Seu WhatsApp (ex: 19992709717)")
    if whats:
        pts = st.session_state.pontos.get(whats, 0)
        st.write(f"✨ **Seus Pontos Atuais:** {pts} pts")

    if not st.session_state.carrinho:
        st.warning("O carrinho está vazio, irmão.")
    else:
        df = pd.DataFrame(st.session_state.carrinho)
        total = df['preco'].sum()
        st.table(df.groupby('nome').size().reset_index(name='Qtd'))
        st.subheader(f"Total: R$ {total:.2f}")

        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

        if whats:
            nome = st.text_input("Seu Nome")
            if st.button("💳 Pagar e Finalizar"):
                # Simula acúmulo de pontos
                st.session_state.pontos[whats] = pts + int(total)
                st.session_state.status[whats] = "Pedido Recebido"
                
                # Gera link Mercado Pago
                link = gerar_pagamento(df, total)
                st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:#009EE3;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">PAGAR COM MERCADO PAGO</div></a>', unsafe_allow_html=True)
                
                # WhatsApp Confirmation
                zap_msg = f"Olá Denise! Fiz o pedido de {nome}. Total: R$ {total:.2f}."
                zap_link = f"https://api.whatsapp.com/send?phone=5519992709717&text={zap_msg}"
                st.markdown(f'<a href="{zap_link}" target="_blank" style="text-decoration:none; margin-top:10px; display:block;"><div style="background-color:#25D366;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">CONFIRMAR NO WHATSAPP</div></a>', unsafe_allow_html=True)

elif selected == "Rastreio":
    st.header("🚚 Rastreie sua Benção")
    busca = st.text_input("Digite seu WhatsApp para rastrear")
    if busca in st.session_state.status:
        st.success(f"Status do seu pedido: **{st.session_state.status[busca]}**")
        progresso = {"Pedido Recebido": 25, "Em Preparação": 50, "Saiu para Entrega": 75, "Entregue": 100}
        st.progress(progresso.get(st.session_state.status[busca], 0))
    elif busca:
        st.error("Nenhum pedido ativo encontrado.")

elif selected == "Admin":
    st.header("🔐 Área da Denise")
    senha = st.text_input("Senha", type="password")
    if senha == "123":
        for cli, stat in st.session_state.status.items():
            col1, col2 = st.columns([2,1])
            novo = col1.selectbox(f"Cliente: {cli}", ["Pedido Recebido", "Em Preparação", "Saiu para Entrega", "Entregue"], key=cli)
            if col2.button("Atualizar", key=f"up_{cli}"):
                st.session_state.status[cli] = novo
                st.success("Atualizado!")

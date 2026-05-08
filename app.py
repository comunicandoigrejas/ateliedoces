import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CSS (Foco em Fontes Roxas e Visibilidade) ---
st.markdown("""
    <style>
    /* Fundo Rosa Claro conforme solicitado */
    .stApp {
        background-color: #FFF0F5;
    }
    
    /* FORÇANDO FONTE ROXA EM TUDO */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #4B0082 !important; /* Roxo Escuro (Indigo) */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Ajuste específico para labels de campos de entrada */
    .stTextInput label, .stSelectbox label {
        color: #4B0082 !important;
        font-weight: bold;
    }

    /* Estilização dos botões (Paleta: Roxo e Azul) */
    div.stButton > button {
        background-color: #8E44AD; /* Roxo */
        color: white !important; /* Texto do botão sempre branco para contraste */
        border-radius: 15px;
        font-weight: bold;
    }
    
    div.stButton > button:hover {
        background-color: #2980B9; /* Azul no hover */
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA EXIBIÇÃO DE IMAGEM SEGURA ---
def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Doce+Abençoado", width=largura)

# --- INICIALIZAÇÃO DE DADOS ---
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'pontos' not in st.session_state:
    st.session_state.pontos = {}
if 'status_pedidos' not in st.session_state:
    st.session_state.status_pedidos = {}

# --- MENU SUPERIOR ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff"},
        "nav-link": {"color": "#4B0082"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"},
    }
)

# --- NOVO CARDÁPIO ATUALIZADO (Sequência solicitada) ---
lista_doces = [
    {"nome": "Trufas", "preco": 4.00, "img": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "img": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "img": "assets/paodemel1.png"},
    {"nome": "Trufas (4 unidades)", "preco": 15.00, "img": "assets/trufas4unidades1.png"}
]

# --- LÓGICA DAS PÁGINAS ---

if selected == "Início":
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        exibir_imagem("assets/logo.png", 220) 
    
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Bem-vindo(a), abençoado(a)!")
    st.write("Doces feitos com amor para a glória de Deus.")
    # Versão ARA
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    for doce in lista_doces:
        c1, c2 = st.columns([1, 2])
        with c1:
            exibir_imagem(doce["img"], 140) # Imagens 1:1
        with c2:
            st.subheader(doce["nome"])
            st.write(f"Valor: **R$ {doce['preco']:.2f}**")
            if st.button(f"Adicionar {doce['nome']}", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} na cesta!", icon="🧁")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Seu Pedido")
    id_cliente = st.text_input("WhatsApp (ex: 19992709717)")
    
    if id_cliente:
        pts = st.session_state.pontos.get(id_cliente, 0)
        st.write(f"✨ **Seus Pontos:** {pts}")

    if not st.session_state.carrinho:
        st.warning("Seu carrinho está vazio, irmão.")
    else:
        df_cart = pd.DataFrame(st.session_state.carrinho)
        resumo = df_cart.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Qtd', 'Subtotal']
        st.table(resumo)
        total_geral = resumo['Subtotal'].sum()
        st.markdown(f"### **Total: R$ {total_geral:.2f}**")
        
        nome_contato = st.text_input("Seu Nome")
        if st.button("💬 Solicitar Pagamento via WhatsApp"):
            if nome_contato and id_cliente:
                st.session_state.pontos[id_cliente] = pts + int(total_geral)
                st.session_state.status_pedidos[id_cliente] = "Aguardando Confirmação"
                
                texto = f"A Paz do Senhor, Denise! Pedido de *{nome_contato}* no valor de *R$ {total_geral:.2f}*. Pode me enviar o link de pagamento?"
                link_zap = f"https://api.whatsapp.com/send?phone=5519992709717&text={texto}"
                st.markdown(f'<a href="{link_zap}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">SOLICITAR PAGAMENTO (WHATSAPP)</div></a>', unsafe_allow_html=True)
            else:
                st.error("Preencha o nome e WhatsApp, benção!")

elif selected == "Rastreio":
    st.header("🚚 Acompanhe seu Pedido")
    busca = st.text_input("Seu WhatsApp:")
    if busca in st.session_state.status_pedidos:
        status = st.session_state.status_pedidos[busca]
        st.success(f"Status: **{status}**")
    elif busca:
        st.error("Nenhum pedido encontrado.")

elif selected == "Admin":
    st.header("🔐 Área Administrativa")
    if st.text_input("Senha", type="password") == "denise123":
        for zap, stat in st.session_state.status_pedidos.items():
            st.write(f"Cliente: {zap}")
            novo = st.selectbox("Mudar Status", ["Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue"], key=zap)
            if st.button(f"Atualizar {zap}"):
                st.session_state.status_pedidos[zap] = novo
                st.rerun()

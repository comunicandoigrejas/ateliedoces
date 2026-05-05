import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CSS (Layout Leve e Tons Pastel) ---
st.markdown("""
    <style>
    /* Fundo Rosa Claro */
    .stApp {
        background-color: #FFF0F5;
    }
    /* Cores da Paleta nos Títulos e Botões */
    h1, h2, h3, p {
        color: #4B0082; /* Roxo suave */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Botões personalizados */
    div.stButton > button {
        background-color: #8E44AD; /* Roxo */
        color: white;
        border-radius: 15px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #2980B9; /* Azul ao passar o mouse */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA EXIBIÇÃO DE IMAGEM SEGURA ---
def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        # Placeholder se o arquivo não estiver na pasta assets
        st.image("https://via.placeholder.com/400x400?text=Doce+Abençoado", width=largura)

# --- INICIALIZAÇÃO DE DADOS (SESSION STATE) ---
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
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff"},
        "icon": {"color": "#BA55D3", "font-size": "18px"}, 
        "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"}, # Rosa médio para aba selecionada
    }
)

# --- LISTA DE DOCES (Imagens 1:1) ---
caminho_img = "assets/logo.png"
lista_doces = [
    {"nome": "Brigadeiro Gourmet", "preco": 5.00, "img": caminho_img},
    {"nome": "Bolo de Pote", "preco": 15.00, "img": caminho_img},
    {"nome": "Copo da Felicidade", "preco": 22.00, "img": caminho_img},
    {"nome": "Fatia de Torta", "preco": 12.00, "img": caminho_img}
]

# --- LÓGICA DAS PÁGINAS ---

if selected == "Início":
    # Logo reduzido conforme solicitado
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        exibir_imagem("assets/logo.png", 200) 
    
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Bem-vindo(a), benção!")
    st.write("Adoçando vidas com amor e dedicação para a honra do Senhor.")
    
    # Versão ARA
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🧁 Nosso Cardápio")
    st.write("Escolha as delícias para seu dia:")
    
    for doce in lista_doces:
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                exibir_imagem(doce["img"], 140) # Formato 1:1
            with c2:
                st.subheader(doce["nome"])
                st.write(f"Valor: **R$ {doce['preco']:.2f}**")
                if st.button(f"Adicionar {doce['nome']}", key=doce['nome']):
                    st.session_state.carrinho.append(doce)
                    st.toast(f"{doce['nome']} adicionado ao carrinho!", icon="🛒")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Seu Pedido")
    
    # Login Simples por WhatsApp
    id_cliente = st.text_input("Informe seu WhatsApp para acumular pontos (ex: 19992709717)")
    
    if id_cliente:
        pts = st.session_state.pontos.get(id_cliente, 0)
        st.write(f"✨ **Seus Pontos de Fidelidade:** {pts} pontos")
    
    if not st.session_state.carrinho:
        st.warning("O carrinho está vazio, varão!")
    else:
        df_cart = pd.DataFrame(st.session_state.carrinho)
        resumo = df_cart.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Qtd', 'Subtotal']
        
        st.table(resumo)
        total_geral = resumo['Subtotal'].sum()
        st.markdown(f"### **Total do Pedido: R$ {total_geral:.2f}**")
        
        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

        st.write("---")
        nome_contato = st.text_input("Seu Nome")
        
        if st.button("💬 Finalizar e Solicitar Pagamento"):
            if nome_contato and id_cliente:
                # 1. Acumular pontos (1 ponto por real)
                st.session_state.pontos[id_cliente] = pts + int(total_geral)
                # 2. Iniciar status de rastreio
                st.session_state.status_pedidos[id_cliente] = "Aguardando Confirmação"
                
                # 3. Formatar Mensagem WhatsApp
                msg_itens = ""
                for n, r in resumo.iterrows():
                    msg_itens += f"- {r['Qtd']}x {n}%0A"
                
                texto = (
                    f"A Paz do Senhor, Denise! Me chamo *{nome_contato}* e gostaria de confirmar meu pedido:%0A%0A"
                    f"{msg_itens}"
                    f"*Total: R$ {total_geral:.2f}*%0A%0A"
                    f"Poderia me enviar o link de pagamento ou chave PIX, por favor?"
                )
                
                link_zap = f"https://api.whatsapp.com/send?phone=5519992709717&text={texto}"
                
                # Botão verde WhatsApp
                st.markdown(f'''
                    <a href="{link_zap}" target="_blank" style="text-decoration:none;">
                        <div style="background-color:#25D366; color:white; padding:15px; 
                        text-align:center; border-radius:10px; font-weight:bold; font-size:16px;">
                            SOLICITAR PAGAMENTO NO WHATSAPP
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Por favor, preencha nome e WhatsApp para finalizar o pedido.")

elif selected == "Rastreio":
    st.header("🚚 Rastreie sua Encomenda")
    busca_zap = st.text_input("Informe seu WhatsApp para ver o status:")
    
    if busca_zap in st.session_state.status_pedidos:
        status_atual = st.session_state.status_pedidos[busca_zap]
        st.success(f"Status Atual: **{status_atual}**")
        
        # Barra de progresso visual
        progresso_map = {"Aguardando Confirmação": 25, "Preparando com Carinho": 50, "Saiu para Entrega": 75, "Entregue": 100}
        st.progress(progresso_map.get(status_atual, 0))
    elif busca_zap:
        st.error("Nenhum pedido ativo encontrado para este número.")

elif selected == "Admin":
    st.header("🔐 Painel Administrativo")
    senha = st.text_input("Senha de Acesso", type="password")
    
    if senha == "denise123":
        if not st.session_state.status_pedidos:
            st.info("Nenhum pedido registrado no momento.")
        else:
            for zap_c, stat_c in st.session_state.status_pedidos.items():
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    novo_status = st.selectbox(f"Cliente: {zap_c}", 
                        ["Aguardando Confirmação", "Preparando com Carinho", "Saiu para Entrega", "Entregue"], 
                        key=f"sel_{zap_c}", index=0)
                with col_b:
                    if st.button("Atualizar", key=f"btn_{zap_c}"):
                        st.session_state.status_pedidos[zap_c] = novo_status
                        st.success("Status Atualizado!")

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
    <style>
    /* Fundo rosa claro */
    .stApp {
        background-color: #FFF0F5;
    }
    /* Títulos e textos */
    h1, h2, h3, p {
        color: #000000;
        font-family: 'Arial', sans-serif;
    }
    /* Botões coloridos conforme paleta preferida */
    div.stButton > button:first-child {
        background-color: #8E44AD; /* Roxo */
        color: white;
        border-radius: 10px;
        border: none;
    }
    .btn-whatsapp {
        background-color: #27AE60 !important; /* Verde */
        color: white !important;
        padding: 15px;
        text-align: center;
        border-radius: 10px;
        text-decoration: none;
        display: block;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS EM MEMÓRIA (SESSION STATE) ---
# Em uma aplicação real, aqui conectaríamos com Google Sheets.
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'banco_pontos' not in st.session_state:
    st.session_state.banco_pontos = {"19992709717": 50} # Exemplo de pontos existentes
if 'status_pedidos' not in st.session_state:
    st.session_state.status_pedidos = {}

# --- MENU SUPERIOR ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedido & Pontos", "Rastreio", "Admin"],
    icons=["house", "book", "cart4", "truck", "shield-lock"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff"},
        "icon": {"color": "#BA55D3", "font-size": "18px"}, 
        "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"},
    }
)

# --- LISTA DE PRODUTOS ---
doces = [
    {"id": 1, "nome": "Brigadeiro Gourmet", "preco": 5.00, "img": "assets/brigadeiro.jpg"},
    {"id": 2, "nome": "Bolo de Pote", "preco": 15.00, "img": "assets/bolo_pote.jpg"},
    {"id": 3, "nome": "Copo da Felicidade", "preco": 22.00, "img": "assets/copo.jpg"},
    {"id": 4, "nome": "Caixa Presente (12 unid)", "preco": 55.00, "img": "assets/caixa.jpg"}
]

# --- LÓGICA DAS TELAS ---

if selected == "Início":
    st.image("Cópia de ATELIÊ DOCES Denise Borges.jpg", use_column_width=True)
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Ateliê!</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### A Paz do Senhor, varão e varoa!")
    st.write("É uma benção ter você aqui. Denise Borges prepara cada doce com amor e ingredientes selecionados para adoçar sua vida.")
    st.info("📖 'Provai e vede que o Senhor é bom.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nosso Cardápio")
    st.write("Selecione as bençãos que deseja hoje:")
    
    for doce in doces:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                # Placeholder caso a imagem ainda não exista na pasta assets
                try:
                    st.image(doce["img"], width=150)
                except:
                    st.image("https://via.placeholder.com/400x400?text=Doce+1:1", width=150)
            with col2:
                st.subheader(doce["nome"])
                st.write(f"**Preço:** R$ {doce['preco']:.2f}")
                if st.button(f"Adicionar ao Carrinho", key=f"btn_{doce['id']}"):
                    st.session_state.carrinho.append(doce)
                    st.toast(f"{doce['nome']} adicionado!", icon="✅")

elif selected == "Pedido & Pontos":
    st.header("🛒 Seu Carrinho e Fidelidade")
    
    # 1. Login para Pontos
    with st.expander("💎 Ver Meus Pontos", expanded=False):
        zap_login = st.text_input("Informe seu WhatsApp (DDD + Número)")
        if zap_login in st.session_state.banco_pontos:
            pts = st.session_state.banco_pontos[zap_login]
            st.success(f"Você tem {pts} pontos acumulados!")
        elif zap_login:
            st.warning("Primeira vez aqui? Ganhe pontos no seu primeiro pedido!")

    # 2. Resumo do Pedido
    if not st.session_state.carrinho:
        st.info("O carrinho está vazio. Vá ao cardápio e escolha um doce!")
    else:
        df = pd.DataFrame(st.session_state.carrinho)
        resumo = df.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Qtd', 'Subtotal']
        
        st.table(resumo)
        total = resumo['Subtotal'].sum()
        st.markdown(f"### **Total: R$ {total:.2f}**")
        
        if st.button("Limpar Tudo"):
            st.session_state.carrinho = []
            st.rerun()

        st.write("---")
        st.subheader("Finalizar")
        nome = st.text_input("Seu Nome")
        zap = st.text_input("Seu WhatsApp para Contato")
        
        if st.button("🚀 Enviar Pedido"):
            if nome and zap:
                # Lógica de Pontos (1 ponto por real)
                st.session_state.banco_pontos[zap] = st.session_state.banco_pontos.get(zap, 0) + int(total)
                # Salva Status Inicial para Rastreio
                st.session_state.status_pedidos[zap] = {"status": "Recebido", "progresso": 20}
                
                # Formata Mensagem WhatsApp
                msg = f"Olá Denise! Pedido de *{nome}*:%0A"
                for n, r in resumo.iterrows():
                    msg += f"- {r['Qtd']}x {n}%0A"
                msg += f"*Total: R$ {total:.2f}*"
                
                link = f"https://api.whatsapp.com/send?phone=5519992709717&text={msg}"
                
                st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">CONFIRMAR PEDIDO NO WHATSAPP</a>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Por favor, preencha nome e contato, irmão!")

elif selected == "Rastreio":
    st.header("🚚 Onde está meu doce?")
    zap_rastreio = st.text_input("Digite seu WhatsApp cadastrado:")
    
    if zap_rastreio in st.session_state.status_pedidos:
        dados = st.session_state.status_pedidos[zap_rastreio]
        st.info(f"Status Atual: **{dados['status']}**")
        st.progress(dados['progresso'])
        
        st.write("✅ Pedido Recebido")
        if dados['progresso'] >= 50: st.write("👨‍🍳 Em Preparação")
        if dados['progresso'] >= 80: st.write("🛵 Saiu para Entrega")
        if dados['progresso'] == 100: st.write("🎂 Entregue! Bom apetite.")
    elif zap_rastreio:
        st.error("Pedido não encontrado ou já finalizado.")

elif selected == "Admin":
    st.header("🔐 Painel Administrativo")
    acesso = st.text_input("Senha de Acesso", type="password")
    
    if acesso == "123": # Altere para a senha da irmã Denise
        st.subheader("Gerenciar Status")
        if not st.session_state.status_pedidos:
            st.write("Nenhum pedido ativo no momento.")
        else:
            for z, d in st.session_state.status_pedidos.items():
                col1, col2 = st.columns([2, 1])
                with col1:
                    novo_s = st.selectbox(f"Status para {z}", ["Recebido", "Cozinhando", "Entrega", "Concluído"], key=z)
                with col2:
                    if st.button("Atualizar", key=f"up_{z}"):
                        prog = {"Recebido": 20, "Cozinhando": 50, "Entrega": 80, "Concluído": 100}
                        st.session_state.status_pedidos[z] = {"status": novo_s, "progresso": prog[novo_s]}
                        st.success("Status Atualizado!")

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import urllib.parse

# Configurações da página
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #FFF0F5; /* Rosa claro conforme pedido */
    }}
    .stButton>button {{
        background-color: #8E44AD;
        color: white;
        border-radius: 10px;
    }}
    .main-title {{
        color: #5D4037;
        text-align: center;
        font-family: 'Playfair Display', serif;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MENU SUPERIOR ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Meus Pedidos"],
    icons=["house", "book", "cart4"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff"},
        "icon": {"color": "#BA55D3", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FFB6C1"},
    }
)

# Inicializar o carrinho na sessão se não existir
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# --- BANCO DE DADOS SIMULADO ---
doces = [
    {"nome": "Brigadeiro Gourmet", "preco": 5.00, "img": "https://via.placeholder.com/400x400?text=Brigadeiro"},
    {"nome": "Bolo de Pote", "preco": 15.00, "img": "https://via.placeholder.com/400x400?text=Bolo+de+Pote"},
    {"nome": "Copo da Felicidade", "preco": 22.00, "img": "https://via.placeholder.com/400x400?text=Copo+Felicidade"}
]

# --- LÓGICA DAS PÁGINAS ---

if selected == "Início":
    # No início do arquivo ou na aba "Início"
    st.image("assets/logo.png", width=200)
    st.markdown("<h1 class='main-title'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/800x400?text=Logo+Denise+Borges", use_column_width=True)
    st.write("---")
    st.markdown("### Bem-vinda(o), benção!")
    st.write("Doces feitos com amor e dedicação para adoçar a sua vida e glorificar ao Senhor.")
    st.info("📖 'Provai e vede que o Senhor é bom.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nosso Cardápio")
    st.write("Escolha suas delícias e adicione ao carrinho.")
    
    for doce in doces:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(doce["img"], width=150)
        with col2:
            st.subheader(doce["nome"])
            st.write(f"Valor: R$ {doce['preco']:.2f}")
            if st.button(f"Adicionar {doce['nome']}", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.success(f"{doce['nome']} adicionado!")

elif selected == "Meus Pedidos":
    st.header("🛒 Seu Pedido")
    
    if not st.session_state.carrinho:
        st.warning("Irmão(ã), seu carrinho ainda está vazio!")
    else:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
        resumo = df_carrinho.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Quantidade', 'Subtotal']
        
        st.table(resumo)
        total_geral = resumo['Subtotal'].sum()
        st.markdown(f"### **Total do Pedido: R$ {total_geral:.2f}**")
        
        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

        st.write("---")
        st.subheader("Finalize seu pedido")
        nome_cliente = st.text_input("Seu Nome")
        whats_cliente = st.text_input("Seu WhatsApp (com DDD)")
        
        if st.button("🚀 Enviar Pedido para o WhatsApp"):
            if nome_cliente and whats_cliente:
                # Formata a mensagem para o Zap
                itens_msg = ""
                for nome, row in resumo.iterrows():
                    itens_msg += f"- {row['Quantidade']}x {nome}%0A"
                
                texto_final = f"Olá Denise! Me chamo *{nome_cliente}*.%0AGostaria de fazer o seguinte pedido:%0A%0A{itens_msg}%0A*Total: R$ {total_geral:.2f}*%0A%0AContato: {whats_cliente}"
                
                # Link do WhatsApp da Denise (Coloque o número dela aqui)
                numero_denise = "5519992709717"
                link_whatsapp = f"https://api.whatsapp.com/send?phone={numero_denise}&text={texto_final}"
                
                st.markdown(f'<a href="{link_whatsapp}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:10px;text-align:center;border-radius:10px;">CLIQUE AQUI PARA CONFIRMAR NO WHATSAPP</div></a>', unsafe_allow_html=True)
            else:
                st.error("Por favor, preencha seu nome e contato para prosseguir, varão!")

import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Cardápio - Ateliê Denise Borges",
    page_icon="🍰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    .card-doces {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #8E44AD;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    h1, h2 { color: #4B0082 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Menu Inicial"):
    st.switch_page("app.py")

st.header("🍰 Nosso Cardápio")
st.write("Escolha as bênçãos de hoje:")

# Inicializa o carrinho se não existir
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# --- LISTA DE PRODUTOS ---
# Cada item contém: Nome, Preço e Caminho da Imagem
produtos = [
    {"nome": "Trufa", "preco": 4.00, "imagem": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "imagem": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "imagem": "assets/paodemel1.png"},
    {"nome": "Kit 4 Trufas", "preco": 15.00, "imagem": "assets/trufas4unidades1.png"}
]

# Exibição em Grid (2 colunas)
cols = st.columns(2)

for i, produto in enumerate(produtos):
    with cols[i % 2]:
        st.markdown(f'<div class="card-doces">', unsafe_allow_html=True)
        
        # Tenta carregar a imagem, se não conseguir mostra um aviso
        try:
            st.image(produto["imagem"], use_container_width=True)
        except:
            st.warning(f"Imagem de {produto['nome']} não encontrada.")
            
        st.markdown(f"### {produto['nome']}")
        st.markdown(f"**R$ {produto['preco']:.2f}**")
        
        if st.button(f"Adicionar {produto['nome']}", key=f"btn_{i}"):
            st.session_state.carrinho.append({"item": produto["nome"], "preco": produto["preco"]})
            st.toast(f"{produto['nome']} adicionado ao carrinho! ✨")
            
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Botão flutuante para ver o carrinho
if st.session_state.carrinho:
    if st.button(f"🛒 Ver Meu Carrinho ({len(st.session_state.carrinho)} itens)"):
        st.switch_page("pages/3_pedidos.py")

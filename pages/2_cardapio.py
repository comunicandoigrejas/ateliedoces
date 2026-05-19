import streamlit as st

st.set_page_config(
    page_title="Cardápio - Ateliê Denise Borges",
    page_icon="🍰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== CSS AGRESSIVO ======================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none !important;}
    .stApp { background-color: #FFF0F5; }
    
    h1, h2, h3, p, label { color: #1a1a1a !important; }

    /* Remove TODOS os espaços e caixas brancas no topo */
    div[data-testid="column"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .stMarkdown, .element-container, div[data-testid="stVerticalBlock"] > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Esconde qualquer elemento vazio ou caixa branca */
    div[data-testid="stVerticalBlock"] > div:first-child {
        display: none !important;
    }

    .card-doces {
        background-color: white;
        padding: 15px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 15px 0 25px 0;
    }
    
    .card-doces img {
        border-radius: 12px;
        margin-bottom: 12px;
    }
    
    div.stButton > button {
        background-color: #8E44AD;
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Menu Inicial"):
    st.switch_page("app.py")

st.header("🍰 Nosso Cardápio")
st.markdown("Escolha as bênçãos de hoje:")

if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# ====================== PRODUTOS ======================
produtos = [
    {"nome": "Trufa", "preco": 4.00, "imagem": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "imagem": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "imagem": "assets/paodemel1.png"},
    {"nome": "Kit 4 Trufas", "preco": 15.00, "imagem": "assets/trufas4unidades1.png"}
]

# Layout sem colunas tradicionais para evitar caixas
for i in range(0, len(produtos), 2):
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        if i < len(produtos):
            produto = produtos[i]
            st.markdown('<div class="card-doces">', unsafe_allow_html=True)
            try:
                st.image(produto["imagem"], width=200)
            except:
                st.warning(f"Imagem não encontrada")
            st.subheader(produto['nome'])
            st.markdown(f"**R$ {produto['preco']:.2f}**")
            if st.button(f"Adicionar {produto['nome']}", key=f"add_{i}"):
                st.session_state.carrinho.append({"item": produto["nome"], "preco": produto["preco"]})
                st.toast(f"✅ {produto['nome']} adicionado!", icon="🛒")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if i + 1 < len(produtos):
            produto = produtos[i+1]
            st.markdown('<div class="card-doces">', unsafe_allow_html=True)
            try:
                st.image(produto["imagem"], width=200)
            except:
                st.warning(f"Imagem não encontrada")
            st.subheader(produto['nome'])
            st.markdown(f"**R$ {produto['preco']:.2f}**")
            if st.button(f"Adicionar {produto['nome']}", key=f"add_{i+1}"):
                st.session_state.carrinho.append({"item": produto["nome"], "preco": produto["preco"]})
                st.toast(f"✅ {produto['nome']} adicionado!", icon="🛒")
            st.markdown('</div>', unsafe_allow_html=True)

st.divider()

if st.session_state.carrinho:
    if st.button(f"🛒 Ver Meu Carrinho ({len(st.session_state.carrinho)} itens)", type="primary"):
        st.switch_page("pages/3_pedidos.py")

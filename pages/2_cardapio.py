import streamlit as st

st.set_page_config(
    page_title="Cardápio - Ateliê Denise Borges",
    page_icon="🍰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== CSS MELHORADO ======================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    
    /* Remove espaços e caixas indesejadas */
    .stMarkdown, .element-container, div[data-testid="column"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    .card-doces {
        background-color: white;
        padding: 12px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 25px;
    }
    
    .card-doces img {
        border-radius: 12px;
        margin: 8px 0 10px 0;
    }
    
    div.stButton > button {
        background-color: #8E44AD;
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
        margin-top: 8px;
    }
    
    /* Remove qualquer caixa branca vazia */
    .stTextInput, .stTextArea, .stSelectbox {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Menu Inicial"):
    st.switch_page("app.py")

st.header("🍰 Nosso Cardápio")
st.write("Escolha as bênçãos de hoje:")

# Carrinho
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# ====================== PRODUTOS ======================
produtos = [
    {"nome": "Trufa", "preco": 4.00, "imagem": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "imagem": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "imagem": "assets/paodemel1.png"},
    {"nome": "Kit 4 Trufas", "preco": 15.00, "imagem": "assets/trufas4unidades1.png"}
]

# Layout em colunas
cols = st.columns(2)

for i, produto in enumerate(produtos):
    with cols[i % 2]:
        st.markdown('<div class="card-doces">', unsafe_allow_html=True)
        
        # Imagem com tamanho controlado
        try:
            st.image(produto["imagem"], width=200)
        except:
            st.warning(f"Imagem não encontrada: {produto['nome']}")
        
        st.subheader(produto['nome'])
        st.markdown(f"**R$ {produto['preco']:.2f}**")
        
        if st.button(f"Adicionar {produto['nome']}", key=f"add_{i}"):
            st.session_state.carrinho.append({"item": produto["nome"], "preco": produto["preco"]})
            st.toast(f"✅ {produto['nome']} adicionado!", icon="🛒")
        
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

if st.session_state.carrinho:
    if st.button(f"🛒 Ver Meu Carrinho ({len(st.session_state.carrinho)} itens)", type="primary"):
        st.switch_page("pages/3_pedidos.py")

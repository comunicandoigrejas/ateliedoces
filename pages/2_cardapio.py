import streamlit as st

st.set_page_config(
    page_title="Cardápio - Ateliê Denise Borges",
    page_icon="🍰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== CSS ULTRA LIMPO ======================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none !important;}
    .stApp { background-color: #FFF0F5; }
    
    h1, h2, h3, p, label, .stMarkdown { color: #1a1a1a !important; }

    /* Remove TODOS os espaços em branco no topo e entre colunas */
    div[data-testid="stVerticalBlock"] > div:first-child,
    div[data-testid="column"] > div:first-child,
    .element-container:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
        display: block !important;
    }

    /* Força remoção de caixas vazias */
    div[data-testid="stVerticalBlock"] > div > div > div:empty {
        display: none !important;
    }

    .card-doces {
        background-color: white;
        padding: 16px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        text-align: center;
        margin: 12px 0 25px 0;
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

    /* Toast */
    .stToast {
        background-color: #28a745 !important;
        color: white !important;
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

# Abordagem com container + columns mais controlada
container = st.container()

with container:
    for i in range(0, len(produtos), 2):
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            if i < len(produtos):
                p = produtos[i]
                st.markdown('<div class="card-doces">', unsafe_allow_html=True)
                try:
                    st.image(p["imagem"], width=205)
                except:
                    st.warning("Imagem não encontrada")
                st.subheader(p['nome'])
                st.markdown(f"**R$ {p['preco']:.2f}**")
                
                if st.button(f"Adicionar {p['nome']}", key=f"add_{i}"):
                    st.session_state.carrinho.append({"item": p["nome"], "preco": p["preco"]})
                    st.toast(f"✅ {p['nome']} adicionado ao carrinho!", icon="🛒")
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            if i + 1 < len(produtos):
                p = produtos[i+1]
                st.markdown('<div class="card-doces">', unsafe_allow_html=True)
                try:
                    st.image(p["imagem"], width=205)
                except:
                    st.warning("Imagem não encontrada")
                st.subheader(p['nome'])
                st.markdown(f"**R$ {p['preco']:.2f}**")
                
                if st.button(f"Adicionar {p['nome']}", key=f"add_{i+1}"):
                    st.session_state.carrinho.append({"item": p["nome"], "preco": p["preco"]})
                    st.toast(f"✅ {p['nome']} adicionado ao carrinho!", icon="🛒")
                st.markdown('</div>', unsafe_allow_html=True)

st.divider()

if st.session_state.carrinho:
    if st.button(f"🛒 Ver Meu Carrinho ({len(st.session_state.carrinho)} itens)", type="primary"):
        st.switch_page("pages/3_pedidos.py")

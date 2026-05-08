import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import urllib.parse
import requests

# URL do Apps Script ATUALIZADA
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbxR9RW2jX24bq48KUySXHQOQIe3l5hd-tAlNpTL3yD0Mjyy3vhdzjrskR6zjOop3RO9qQ/exec"

def salvar_na_planilha(nome, whatsapp, pedido, total):
    dados = {
        "nome": nome,
        "whatsapp": whatsapp,
        "pedido": pedido,
        "total": float(total)
    }
    try:
        requests.post(URL_PLANILHA, json=dados)
        return True
    except:
        return False

def buscar_dados_planilha():
    try:
        resposta = requests.get(URL_PLANILHA)
        if resposta.status_code == 200:
            return resposta.json()
        return []
    except:
        return []

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Ateliê Doces Denise Borges", page_icon="🧁", layout="centered")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #4B0082 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    div.stButton > button, div.stButton > button p, div.stButton > button span,
    .stLinkButton a, .stLinkButton a p, .stLinkButton a span {
        color: white !important;
    }
    div.stButton > button { background-color: #8E44AD; border-radius: 15px; font-weight: bold; }
    div.stButton > button:hover { background-color: #2980B9; }
    .stTextInput input { color: #4B0082 !important; }
    </style>
    """, unsafe_allow_html=True)

def exibir_imagem(caminho, largura):
    if os.path.exists(caminho):
        st.image(caminho, width=largura)
    else:
        st.image("https://via.placeholder.com/400x400?text=Doce+Abençoado", width=largura)

if 'carrinho' not in st.session_state: st.session_state.carrinho = []

# --- MENU ---
selected = option_menu(
    menu_title=None,
    options=["Início", "Cardápio", "Pedidos & Pontos", "Rastreio", "Contato", "Admin"],
    icons=["house", "book", "cart4", "truck", "chat-dots", "shield-lock"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff"},
        "nav-link": {"color": "#4B0082", "font-size": "13px"},
        "nav-link-selected": {"background-color": "#FFB6C1", "color": "black"},
    }
)

lista_doces = [
    {"nome": "Trufas", "preco": 4.00, "img": "assets/trufas1.png"},
    {"nome": "Cone Trufado", "preco": 8.00, "img": "assets/conetrufado1.png"},
    {"nome": "Pão de Mel", "preco": 8.00, "img": "assets/paodemel1.png"},
    {"nome": "Trufas (4 unidades)", "preco": 15.00, "img": "assets/trufas4unidades1.png"}
]

if selected == "Início":
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c: exibir_imagem("assets/logo.png", 220) 
    st.markdown("<h1 style='text-align: center;'>Ateliê Doces Denise Borges</h1>", unsafe_allow_html=True)
    st.info("📖 'Provai e vede que o Senhor é bom; bem-aventurado o homem que nele se refugia.' - Salmos 34:8 (ARA)")

elif selected == "Cardápio":
    st.header("🍰 Nossas Delícias")
    for doce in lista_doces:
        c1, c2 = st.columns([1, 2])
        with c1: exibir_imagem(doce["img"], 140) 
        with c2:
            st.subheader(doce["nome"])
            st.write(f"Valor: **R$ {doce['preco']:.2f}**")
            if st.button(f"Adicionar {doce['nome']}", key=doce['nome']):
                st.session_state.carrinho.append(doce)
                st.toast(f"{doce['nome']} adicionado!")

elif selected == "Pedidos & Pontos":
    st.header("🛒 Seu Pedido")
    id_cliente = st.text_input("WhatsApp (apenas números)")
    if id_cliente:
        dados = buscar_dados_planilha()
        total_pontos = sum(float(item['total']) for item in dados if item['whatsapp'] == id_cliente)
        st.write(f"✨ **Seus Pontos Acumulados:** {int(total_pontos)}")

    if not st.session_state.carrinho:
        st.warning("O carrinho está vazio, irmão.")
    else:
        df_cart = pd.DataFrame(st.session_state.carrinho)
        resumo = df_cart.groupby('nome').agg({'preco': ['count', 'sum']})
        resumo.columns = ['Qtd', 'Subtotal']
        st.table(resumo)
        total_geral = resumo['Subtotal'].sum()
        st.markdown(f"### **Total: R$ {total_geral:.2f}**")
        
        nome_contato = st.text_input("Seu Nome")
        if st.button("💬 Finalizar Pedido"):
            if nome_contato and id_cliente:
                sucesso = salvar_na_planilha(nome_contato, id_cliente, str(resumo.index.tolist()), total_geral)
                if sucesso:
                    texto_pedido = urllib.parse.quote(f"A Paz do Senhor, Denise! Pedido de *{nome_contato}* no valor de *R$ {total_geral:.2f}*.")
                    link_zap = f"https://api.whatsapp.com/send?phone=5519992709717&text={texto_pedido}"
                    st.markdown(f'<a href="{link_zap}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white !important;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">ENVIAR PARA WHATSAPP</div></a>', unsafe_allow_html=True)
                    st.success("Pedido registrado! Clique no botão acima.")
                else:
                    st.error("Erro ao salvar. Verifique se o Apps Script permite acesso 'Anyone'.")
            else:
                st.error("Preencha nome e WhatsApp, benção!")

elif selected == "Rastreio":
    st.header("🚚 Rastreio")
    busca = st.text_input("Seu WhatsApp:")
    if busca:
        dados = buscar_dados_planilha()
        pedido = next((item for item in reversed(dados) if item['whatsapp'] == busca), None)
        if pedido:
            st.success(f"Status do Pedido: **{pedido['status']}**")
        else:
            st.warning("Nenhum pedido encontrado para este número.")

elif selected == "Contato":
    st.header("📞 Fale Conosco")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("WhatsApp")
        link_w = "https://api.whatsapp.com/send?phone=5519992709717&text=Vim%20pelo%20App"
        st.markdown(f'<a href="{link_w}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white !important; padding:10px; text-align:center; border-radius:10px; font-weight:bold;">ABRIR WHATSAPP</div></a>', unsafe_allow_html=True)
    with col2:
        st.subheader("Instagram")
        st.link_button("Seguir no Instagram", "https://www.instagram.com/deniseborges.doces")
    exibir_imagem("assets/logo.png", 180)

elif selected == "Admin":
    st.header("🔐 Painel Admin")
    if st.text_input("Senha", type="password") == "denise123":
        dados = buscar_dados_planilha()
        if not dados:
            st.info("Nenhum pedido na planilha ainda.")
        else:
            for item in dados:
                st.write(f"**Cliente:** {item['nome']} ({item['whatsapp']})")
                st.write(f"Status Atual: {item['status']}")
                st.write("---")

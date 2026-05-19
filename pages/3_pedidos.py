import streamlit as st
import requests
import urllib.parse

st.set_page_config(
    page_title="Finalizar Pedido - Ateliê Denise Borges", 
    page_icon="🛒", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ====================== CONFIGURAÇÕES ======================
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"
WHATSAPP_ADMIN = "19992009129"

# ====================== CSS ======================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 4em;
        width: 100%;
        font-size: 1.1em;
    }
    .whatsapp-btn {
        background-color: #25D366 !important;
        color: white !important;
        padding: 18px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Cardápio"):
    st.switch_page("pages/2_cardapio.py")

st.title("🛒 Finalizar Pedido")

if 'usuario' not in st.session_state or st.session_state.usuario is None:
    st.warning("Faça o login para continuar.")
    st.stop()

if not st.session_state.carrinho:
    st.info("Seu carrinho está vazio!")
    if st.button("Voltar ao Cardápio"):
        st.switch_page("pages/2_cardapio.py")
else:
    total = sum(item['preco'] for item in st.session_state.carrinho)
    resumo_itens = "\n".join([f"• {item['item']} (R$ {item['preco']:.2f})" for item in st.session_state.carrinho])

    st.subheader("Resumo do Pedido")
    for item in st.session_state.carrinho:
        st.write(f"✅ {item['item']} - **R$ {item['preco']:.2f}**")

    st.divider()
    st.markdown(f"### Total: **R$ {total:.2f}**")

    if 'pedido_enviado' not in st.session_state:
        st.session_state.pedido_enviado = False

    if not st.session_state.pedido_enviado:
        if st.button("🚀 SALVAR PEDIDO E PREPARAR WHATSAPP", type="primary"):
            with st.spinner("Registrando pedido..."):
                payload = {
                    "action": "create",
                    "nome": st.session_state.usuario['nome'],
                    "whatsapp": st.session_state.usuario['zap'],
                    "pedido": resumo_itens.replace("\n", ", "),
                    "total": total
                }
                
                try:
                    res = requests.post(URL_PLANILHA, json=payload)
                    if res.status_code == 200:
                        st.session_state.pedido_enviado = True
                        st.rerun()
                    else:
                        st.error("Erro ao salvar pedido. Tente novamente.")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
    else:
        st.success("✅ Pedido salvo com sucesso na planilha!")
        st.balloons()

        # Mensagem para WhatsApp
        quebra = "%0A"
        msg = f"Olá Denise! Novo pedido:{quebra}{quebra}"
        msg += f"*Cliente:* {st.session_state.usuario['nome']}{quebra}"
        msg += f"*Itens:*{quebra}{resumo_itens.replace('\n', quebra)}{quebra}"
        msg += f"*Total:* R$ {total:.2f}"

        link_zap = f"https://api.whatsapp.com/send?phone=55{WHATSAPP_ADMIN}&text={urllib.parse.quote(msg)}"

        st.markdown(f"""
            <div style="text-align: center; background-color: #e8f5e9; padding: 25px; border-radius: 15px; border: 3px solid #25D366;">
                <p style="color: #1b5e20; font-weight: bold; font-size: 18px;">
                    🙏 Clique abaixo para enviar o pedido para Denise:
                </p>
                <a href="{link_zap}" target="_blank" style="text-decoration: none;">
                    <div class="whatsapp-btn">
                        🟢 ENVIAR PARA O WHATSAPP
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🛒 Fazer outro pedido"):
            st.session_state.carrinho = []
            st.session_state.pedido_enviado = False
            st.switch_page("pages/2_cardapio.py")

st.divider()
st.caption("Ateliê Doces Denise Borges")

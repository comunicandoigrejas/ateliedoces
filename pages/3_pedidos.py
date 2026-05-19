import streamlit as st
import requests
import urllib.parse

st.set_page_config(
    page_title="Finalizar Pedido - Ateliê Denise Borges", 
    page_icon="🛒", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"
WHATSAPP_ADMIN = "19992009129"

st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Cardápio"):
    st.switch_page("pages/2_cardapio.py")

st.title("🛒 Finalizar Pedido")

if 'usuario' not in st.session_state or st.session_state.usuario is None:
    st.warning("Faça o login para continuar.")
    st.stop()

if not st.session_state.get('carrinho'):
    st.info("Seu carrinho está vazio!")
else:
    total = sum(item['preco'] for item in st.session_state.carrinho)
    resumo_itens = "\n".join([f"• {item['item']} (R$ {item['preco']:.2f})" for item in st.session_state.carrinho])

    st.subheader("Resumo do Pedido")
    for item in st.session_state.carrinho:
        st.write(f"✅ {item['item']} — R$ {item['preco']:.2f}")

    st.divider()
    st.markdown(f"### Total: **R$ {total:.2f}**")

    if 'pedido_enviado' not in st.session_state:
        st.session_state.pedido_enviado = False

    if not st.session_state.pedido_enviado:
        if st.button("🚀 SALVAR PEDIDO E PREPARAR WHATSAPP", type="primary"):
            with st.spinner("Registrando na planilha..."):
                payload = {
                    "action": "create",
                    "nome": st.session_state.usuario.get('nome', ''),
                    "whatsapp": st.session_state.usuario.get('zap', ''),
                    "pedido": resumo_itens.replace("\n", ", "),
                    "total": float(total)
                }
                
                try:
                    res = requests.post(URL_PLANILHA, json=payload, timeout=20)
                    
                    if res.status_code == 200:
                        st.session_state.pedido_enviado = True
                        st.success("✅ Pedido salvo com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Falha ao salvar (código {res.status_code})")
                        st.write(res.text)
                except Exception as e:
                    st.error(f"Erro de conexão: {str(e)}")
    else:
        # ... (parte do WhatsApp permanece igual)
        st.success("✅ Pedido salvo com sucesso na planilha!")
        st.balloons()
        
        # (código do link do WhatsApp continua igual ao anterior)

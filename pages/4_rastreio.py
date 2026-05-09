import streamlit as st
import requests

st.set_page_config(page_title="Página - Ateliê", initial_sidebar_state="collapsed")

# Esconde a barra lateral via CSS
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar para o Menu Inicial"):
    st.switch_page("app.py")

st.divider()
# ... restante do código da página ...
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbxnjSSBOgQEre9jk58xmIOsdPok70-NCooPk0L4WiPWFHjfmxSRGUicYvQTp5tYRjXqyw/exec"

st.set_page_config(page_title="Rastreio - Ateliê", page_icon="🚚")

st.header("🚚 Onde está meu pedido?")
busca = st.text_input("Digite seu WhatsApp:")

if busca:
    try:
        dados = requests.get(URL_PLANILHA).json()
        pedido = next((item for item in reversed(dados) if str(item.get('whatsapp')) == busca), None)
        if pedido:
            st.success(f"Status: **{pedido.get('status')}**")
        else:
            st.warning("Nenhum pedido encontrado.")
    except:
        st.error("Erro ao buscar dados.")

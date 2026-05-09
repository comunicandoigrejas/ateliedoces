import streamlit as st
import requests

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

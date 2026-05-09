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

st.set_page_config(page_title="Cadastro - Ateliê", page_icon="👤")

st.header("👤 Cadastro de Cliente")
st.write("Cadastre-se para garantir seus pontos e facilitar seus pedidos!")

with st.form("meu_cadastro"):
    nome = st.text_input("Seu Nome Completo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    endereco = st.text_area("Endereço para Entrega")
    
    if st.form_submit_button("Finalizar Cadastro"):
        if nome and whatsapp:
            # Enviamos uma 'action' diferente para o Google salvar em outra aba se quiser
            dados = {"action": "create_user", "nome": nome, "whatsapp": whatsapp, "endereco": endereco}
            requests.post(URL_PLANILHA, json=dados)
            st.success(f"Benção, {nome}! Você já pode fazer seus pedidos.")
        else:
            st.error("Preencha os campos obrigatórios.")

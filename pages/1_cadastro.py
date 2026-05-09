import streamlit as st
import requests

st.set_page_config(page_title="Cadastro - Ateliê", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("👤 Cadastro de Cliente")
st.write("Seus dados estão seguros conosco para fins de entrega e fidelidade.")

with st.form("form_cadastro"):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    endereco = st.text_area("Endereço Completo para Entrega")
    
    if st.form_submit_button("Finalizar Cadastro"):
        if nome and whatsapp:
            # Enviamos para a planilha
            dados = {"action": "create_user", "nome": nome, "whatsapp": whatsapp, "endereco": endereco}
            requests.post("https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec", json=dados)
            st.success("Cadastro realizado com sucesso, varão/varoa!")
        else:
            st.warning("Preencha o nome e o WhatsApp.")

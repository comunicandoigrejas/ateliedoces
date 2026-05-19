import streamlit as st
import requests

st.set_page_config(page_title="Cadastro - Ateliê", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("👤 Cadastro de Cliente")
st.write("Seus dados estão seguros conosco.")

with st.form("form_cadastro"):
    nome = st.text_input("Nome Completo *")
    whatsapp = st.text_input("WhatsApp (com DDD) *", placeholder="19988776655")
    endereco = st.text_area("Endereço Completo para Entrega")
    
    if st.form_submit_button("Finalizar Cadastro", type="primary"):
        if nome and whatsapp:
            dados = {
                "action": "create_user", 
                "nome": nome, 
                "whatsapp": whatsapp, 
                "endereco": endereco
            }
            try:
                requests.post(
                    "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec", 
                    json=dados
                )
                st.success("Cadastro realizado com sucesso! 🎉")
                st.info("Você já pode fazer login com seu WhatsApp.")
            except:
                st.error("Erro ao salvar cadastro. Tente novamente.")
        else:
            st.warning("Nome e WhatsApp são obrigatórios.")

st.caption("Ateliê Doces Denise Borges")

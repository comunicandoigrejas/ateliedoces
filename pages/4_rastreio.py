import streamlit as st
import requests

st.set_page_config(
    page_title="Rastreio - Ateliê Denise Borges", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("🚚 Consultar Meus Pedidos")

zap_logado = st.session_state.usuario['zap'] if 'usuario' in st.session_state and st.session_state.usuario else ""
zap_busca = st.text_input("WhatsApp (apenas números):", value=zap_logado, placeholder="19988776655")

if st.button("🔍 Buscar Pedidos", type="primary") or (zap_busca and st.session_state.get('usuario')):
    if zap_busca:
        with st.spinner("Buscando seus pedidos..."):
            try:
                res = requests.get(URL_PLANILHA)
                dados = res.json()
                
                todos_pedidos = dados.get('pedidos', [])
                zap_alvo = str(zap_busca).strip().replace(".0", "")

                meus_pedidos = []
                for p in todos_pedidos:
                    if len(p) >= 6:
                        zap_linha = str(p[2]).strip().replace(".0", "")
                        if zap_linha == zap_alvo:
                            meus_pedidos.append(p)

                if meus_pedidos:
                    st.success(f"Encontramos {len(meus_pedidos)} pedido(s) para você!")
                    for p in reversed(meus_pedidos):
                        with st.expander(f"📦 Pedido - {p[0]}"):
                            st.write(f"**Data:** {p[0]}")
                            st.write(f"**Detalhes:** {p[3]}")
                            st.write(f"**Valor:** R$ {p[4]}")
                            st.info(f"**Status:** {p[5]}")
                else:
                    st.info("Nenhum pedido encontrado para este número.")

            except Exception as e:
                st.error(f"Erro ao buscar pedidos: {e}")
    else:
        st.warning("Informe seu WhatsApp.")

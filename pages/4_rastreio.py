import streamlit as st
import requests

st.set_page_config(page_title="Meus Pedidos", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("🚚 Consultar Meus Pedidos")
zap_busca = st.text_input("Digite seu WhatsApp cadastrado:")

if zap_busca:
    try:
        # Busca os pedidos na planilha
        resposta = requests.get("https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec").json()
        # Filtra apenas os pedidos desse WhatsApp
        meus_pedidos = [p for p in resposta if str(p.get('whatsapp')) == zap_busca]
        
        if meus_pedidos:
            for p in reversed(meus_pedidos):
                with st.container():
                    st.write(f"📅 **Data:** {p.get('data')}")
                    st.write(f"📦 **Pedido:** {p.get('pedido')}")
                    st.write(f"✅ **Status:** {p.get('status')}")
                    st.divider()
        else:
            st.info("Nenhum pedido encontrado para este número.")
    except:
        st.error("Não foi possível carregar os dados agora.")

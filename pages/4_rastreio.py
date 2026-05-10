import streamlit as st
import requests

# 1. Configuração da Página
st.set_page_config(page_title="Rastreio - Ateliê Denise Borges", layout="centered", initial_sidebar_state="collapsed")

# 2. O Link que você atualizou
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

# Esconder menu lateral para ficar limpo
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("🚚 Consultar Meus Pedidos")

# Pega o Zap do login automaticamente para facilitar para o irmão
zap_logado = st.session_state.usuario['zap'] if 'usuario' in st.session_state and st.session_state.usuario else ""
zap_busca = st.text_input("Confirme seu WhatsApp (apenas números):", value=zap_logado)

if st.button("Buscar Pedidos") or (zap_busca and zap_logado):
    if zap_busca:
        try:
            with st.spinner("Buscando informações na planilha..."):
                # Busca os dados no Google
                resposta = requests.get(URL_PLANILHA).json()
                
                # IMPORTANTE: Pegamos a lista dentro de 'pedidos'
                todos_pedidos = resposta.get('pedidos', [])
                
                # Filtra os pedidos: O Zap é a 3ª coluna (índice 2)
                # Limpamos o .0 caso o Google tenha formatado como número
                meus_pedidos = [
                    p for p in todos_pedidos 
                    if str(p[2]).strip().replace(".0", "") == str(zap_busca).strip()
                ]
                
                if meus_pedidos:
                    st.success(f"Encontramos {len(meus_pedidos)} pedido(s)!")
                    # Mostra do mais novo para o mais velho
                    for p in reversed(meus_pedidos):
                        with st.expander(f"📦 Pedido de {p[0]}"): # p[0] é a Data
                            st.write(f"📝 **Itens:** {p[3]}")
                            st.write(f"💰 **Total:** R$ {p[4]}")
                            st.info(f"🚩 **Status:** {p[5]}")
                else:
                    st.info("Nenhum pedido encontrado para este número.")
        except Exception as e:
            st.error(f"Erro ao acessar os dados. Verifique se o link do Google Script está correto e publicado.")
    else:
        st.warning("Por favor, digite o número do WhatsApp.")

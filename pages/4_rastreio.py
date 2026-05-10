import streamlit as st
import requests

st.set_page_config(page_title="Meus Pedidos", initial_sidebar_state="collapsed")

# Esconde o menu lateral
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

# Usa a URL correta definida no seu app principal
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("🚚 Consultar Meus Pedidos")

# Tenta pegar o zap automaticamente se o usuário estiver logado
zap_usuario = st.session_state.usuario['zap'] if 'usuario' in st.session_state and st.session_state.usuario else ""
zap_busca = st.text_input("Confirme seu WhatsApp cadastrado (apenas números):", value=zap_usuario)

if st.button("Buscar Pedidos") or zap_busca:
    if zap_busca:
        try:
            with st.spinner("Buscando informações..."):
                # 1. Faz a requisição para o Google
                resposta = requests.get(URL_PLANILHA).json()
                
                # 2. Acessa a lista de pedidos dentro do JSON (pulando o cabeçalho se existir)
                todos_pedidos = resposta.get('pedidos', [])
                
                # 3. Filtra os pedidos comparando o WhatsApp (coluna índice 2 na planilha)
                # O formato vindo do Apps Script geralmente é uma lista de listas: [Data, Nome, Zap, Pedido, Total, Status]
                meus_pedidos = [p for p in todos_pedidos if str(p[2]).strip().replace(".0", "") == str(zap_busca).strip()]
                
                if meus_pedidos:
                    st.success(f"Encontramos {len(meus_pedidos)} pedido(s) para você!")
                    # Mostra do mais recente para o mais antigo
                    for p in reversed(meus_pedidos):
                        with st.expander(f"📦 Pedido de {p[0]}"): # p[0] é a Data
                            st.write(f"📝 **Itens:** {p[3]}")
                            st.write(f"💰 **Valor:** R$ {p[4]}")
                            st.info(f"🚩 **Status Atual:** {p[5]}")
                else:
                    st.info("Nenhum pedido encontrado para este número. Verifique se digitou corretamente.")
        except Exception as e:
            st.error("Não foi possível carregar os dados agora. Verifique a conexão com a planilha.")
    else:
        st.warning("Por favor, informe o número do WhatsApp.")

import streamlit as st
import requests

# 1. Configuração da Página
st.set_page_config(page_title="Rastreio - Ateliê Denise Borges", layout="centered", initial_sidebar_state="collapsed")

# 2. O seu link atualizado
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

# Esconder menus
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu"):
    st.switch_page("app.py")

st.header("🚚 Consultar Meus Pedidos")

# Pega o Zap do login para facilitar
zap_logado = st.session_state.usuario['zap'] if 'usuario' in st.session_state and st.session_state.usuario else ""
zap_busca = st.text_input("Confirme seu WhatsApp (apenas números):", value=zap_logado)

if st.button("Buscar Pedidos") or (zap_busca and zap_logado):
    if zap_busca:
        try:
            with st.spinner("Buscando informações..."):
                # Faz a requisição
                res = requests.get(URL_PLANILHA)
                
                # Se a resposta não for um JSON válido, o erro 'char 0' acontece aqui
                # Vamos tratar isso:
                try:
                    dados = res.json()
                except:
                    st.error("O Google retornou um formato inválido. Verifique se a Implantação está como 'Qualquer pessoa'.")
                    st.stop()

                # Pegamos a lista dentro da chave 'pedidos'
                todos_pedidos = dados.get('pedidos', [])
                
                # Filtramos os pedidos (WhatsApp está na Coluna C, índice 2)
                # Removemos espaços e o ".0" que o Excel/Google às vezes coloca
                zap_alvo = str(zap_busca).strip().replace(".0", "")
                
                meus_pedidos = []
                for p in todos_pedidos:
                    # Verifica se a linha tem colunas suficientes e se o zap bate
                    if len(p) >= 3:
                        zap_linha = str(p[2]).strip().replace(".0", "")
                        if zap_linha == zap_alvo:
                            meus_pedidos.append(p)
                
                if meus_pedidos:
                    st.success(f"Irmão, encontramos {len(meus_pedidos)} pedido(s)!")
                    # Inverte para mostrar o mais recente primeiro
                    for p in reversed(meus_pedidos):
                        with st.expander(f"📦 Pedido de {p[0]}"):
                            st.write(f"📝 **Detalhes:** {p[3]}")
                            st.write(f"💰 **Valor:** R$ {p[4]}")
                            st.info(f"🚩 **Status Atual:** {p[5]}")
                else:
                    st.info("Nenhum pedido encontrado para este número na base de dados.")
        
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
    else:
        st.warning("Por favor, informe o WhatsApp para busca.")

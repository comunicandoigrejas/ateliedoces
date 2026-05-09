import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Gestão Ateliê", layout="centered", initial_sidebar_state="collapsed")

# URL do seu Apps Script (a mesma que você usou no app.py)
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

# Esconder menu lateral
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

# Botão para voltar ao menu inicial
if st.button("⬅️ Voltar ao Menu Inicial"):
    st.switch_page("app.py")

st.title("📊 Gestão de Pedidos")

# Verificação de segurança (garantir que só Admin acesse)
if 'usuario' not in st.session_state or st.session_state.usuario['tipo'] != "admin":
    st.error("Acesso restrito à administração.")
    st.stop()

# Função para buscar dados
def buscar_dados():
    try:
        response = requests.get(URL_PLANILHA)
        return response.json()
    except:
        return None

dados = buscar_dados()

if dados:
    # Pegamos os pedidos (ignorando o cabeçalho)
    # Estrutura esperada: [Data, Nome, WhatsApp, Pedido, Total, Status]
    lista_pedidos = dados.get('pedidos', [])[1:]
    
    if not lista_pedidos:
        st.info("Nenhum pedido encontrado na planilha.")
    else:
        st.subheader("Pedidos Ativos")
        
        # Invertemos a lista para mostrar os mais recentes primeiro
        for i, pedido in enumerate(reversed(lista_pedidos)):
            # Criamos um identificador único para cada pedido
            data_hora = pedido[0]
            nome_cliente = pedido[1]
            zap_cliente = pedido[2]
            detalhes = pedido[3]
            total_venda = pedido[4]
            status_atual = pedido[5]

            # Só mostra se não estiver "Entregue" ou "Cancelado" (se você quiser filtrar)
            with st.expander(f"📦 {nome_cliente} - {status_atual}"):
                st.write(f"**Data:** {data_hora}")
                st.write(f"**WhatsApp:** {zap_cliente}")
                st.write(f"**Pedido:** {detalhes}")
                st.write(f"**Valor Total:** R$ {total_venda}")
                
                # Opções de Status
                opcoes_status = ["Aguardando Confirmação", "Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue", "Cancelado"]
                
                # Tenta encontrar o índice do status atual para o selectbox
                try:
                    index_atual = opcoes_status.index(status_atual)
                except:
                    index_atual = 0

                novo_status = st.selectbox(
                    "Atualizar Status:", 
                    opcoes_status, 
                    index=index_atual, 
                    key=f"status_{i}"
                )

                if st.button("Atualizar Pedido", key=f"btn_{i}"):
                    with st.spinner("Atualizando na planilha..."):
                        payload = {
                            "action": "update",
                            "whatsapp": str(zap_cliente),
                            "status": novo_status
                        }
                        res = requests.post(URL_PLANILHA, json=payload)
                        
                        if res.status_code == 200:
                            st.success(f"Status de {nome_cliente} atualizado para: {novo_status}")
                            st.rerun() # Recarrega a página para mostrar o novo status
                        else:
                            st.error("Erro ao atualizar. Tente novamente.")

else:
    st.error("Não foi possível carregar os dados da planilha. Verifique a conexão.")

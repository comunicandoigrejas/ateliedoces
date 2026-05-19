import streamlit as st
import requests

st.set_page_config(page_title="Gestão Ateliê", layout="centered", initial_sidebar_state="collapsed")

URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Menu Inicial"):
    st.switch_page("app.py")

st.title("📊 Gestão de Pedidos")

if 'usuario' not in st.session_state or st.session_state.usuario['tipo'] != "admin":
    st.error("Acesso restrito à administração.")
    st.stop()

def buscar_dados():
    try:
        response = requests.get(URL_PLANILHA)
        return response.json()
    except:
        return None

dados = buscar_dados()

if dados:
    lista_pedidos = dados.get('pedidos', [])[1:]  # Ignora cabeçalho
    
    if not lista_pedidos:
        st.info("Nenhum pedido encontrado.")
    else:
        st.subheader(f"Pedidos Ativos ({len(lista_pedidos)})")
        
        for i, pedido in enumerate(reversed(lista_pedidos)):
            data_hora = pedido[0]
            nome_cliente = pedido[1]
            zap_cliente = pedido[2]
            detalhes = pedido[3]
            total_venda = pedido[4]
            status_atual = pedido[5]

            with st.expander(f"📦 {nome_cliente} - {status_atual}"):
                st.write(f"**Data:** {data_hora}")
                st.write(f"**WhatsApp:** {zap_cliente}")
                st.write(f"**Pedido:** {detalhes}")
                st.write(f"**Valor Total:** R$ {total_venda}")

                opcoes_status = ["Aguardando Confirmação", "Confirmado", "Em Preparo", "Saiu para Entrega", "Entregue", "Cancelado"]
                
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

                if st.button("💾 Atualizar Pedido", key=f"btn_{i}", type="primary"):
                    with st.spinner("Atualizando..."):
                        payload = {
                            "action": "update",
                            "whatsapp": str(zap_cliente),
                            "status": novo_status
                        }
                        res = requests.post(URL_PLANILHA, json=payload)
                        
                        if res.status_code == 200:
                            st.success(f"Status atualizado para: **{novo_status}**")
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar.")
else:
    st.error("Não foi possível carregar os dados da planilha.")

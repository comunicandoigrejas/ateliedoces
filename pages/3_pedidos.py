import streamlit as st
import requests

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Meu Carrinho - Ateliê Denise Borges", 
    page_icon="🛒", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÕES DE ACESSO ---
# Certifique-se de que esta URL seja a da sua última implantação (Nova Versão)
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"

# --- ESTILIZAÇÃO CSS (Esconder Menu Lateral) ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    div.stButton > button { 
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 3.5em;
        width: 100%;
    }
    h1, h2, h3 { color: #4B0082 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Botão para voltar
if st.button("⬅️ Voltar ao Cardápio"):
    st.switch_page("pages/2_cardapio.py")

st.title("🛒 Seu Carrinho")

# VERIFICAÇÃO DE LOGIN
if 'usuario' not in st.session_state or st.session_state.usuario is None:
    st.warning("Por favor, faça login na página inicial para finalizar o pedido.")
    if st.button("Ir para Login"):
        st.switch_page("app.py")
    st.stop()

# VERIFICAÇÃO DE CARRINHO VAZIO
if not st.session_state.carrinho:
    st.info("Irmão, o seu carrinho ainda está vazio. Escolha uma benção no cardápio!")
    if st.button("🍰 Ver Cardápio"):
        st.switch_page("pages/2_cardapio.py")
else:
    st.subheader("Resumo da sua encomenda:")
    
    total = 0
    texto_pedido = ""
    
    # Listar itens do carrinho
    for i, item in enumerate(st.session_state.carrinho):
        col_item, col_preco, col_remover = st.columns([3, 1, 1])
        with col_item:
            st.write(f"✅ {item['item']}")
        with col_preco:
            st.write(f"R$ {item['preco']:.2f}")
        with col_remover:
            if st.button("❌", key=f"rem_{i}"):
                st.session_state.carrinho.pop(i)
                st.rerun()
        
        total += item['preco']
        texto_pedido += f"{item['item']} (R$ {item['preco']:.2f}), "

    st.divider()
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"### Total: R$ {total:.2f}")
    with col_t2:
        pontos = int(total)
        st.markdown(f"### ✨ Pontos: {pontos}")

    st.write("---")
    
    # BOTÃO PARA FINALIZAR
    if st.button("🚀 ENVIAR PEDIDO PARA O ATELIÊ"):
        with st.spinner("Registrando seu pedido no céu e na planilha..."):
            # Preparar dados para o Google Sheets
            payload = {
                "action": "create",
                "nome": st.session_state.usuario['nome'],
                "whatsapp": st.session_state.usuario['zap'],
                "pedido": texto_pedido[:-2], # Remove a última vírgula e espaço
                "total": total
            }
            
            try:
                # Envia para o Google Apps Script
                res = requests.post(URL_PLANILHA, json=payload)
                
                # Se o Google responder com sucesso (JSON)
                if res.status_code == 200:
                    try:
                        resultado = res.json()
                        if resultado.get("status") == "sucesso":
                            st.success("Glória a Deus! Seu pedido foi recebido com sucesso.")
                            st.balloons()
                            # Limpa o carrinho
                            st.session_state.carrinho = []
                            st.info("Você já pode acompanhar o status em 'Rastrear Pedidos'.")
                        else:
                            st.error(f"Erro no servidor: {resultado.get('message')}")
                    except:
                        # Caso o Google responda Sucesso mas não em formato JSON
                        if "Sucesso" in res.text or "OK" in res.text:
                            st.success("Pedido enviado com sucesso!")
                            st.session_state.carrinho = []
                        else:
                            st.error("Resposta inesperada do servidor. Verifique a planilha.")
                            st.code(res.text[:100])
                else:
                    st.error(f"Erro de conexão (Status {res.status_code}).")
            
            except Exception as e:
                st.error(f"Falha técnica ao enviar: {e}")

    if st.button("➕ Adicionar mais itens"):
        st.switch_page("pages/2_cardapio.py")

st.divider()
st.caption("Ateliê Doces Denise Borges - Feito com amor e oração.")

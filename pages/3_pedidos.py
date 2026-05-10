import streamlit as st
import requests
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Meu Carrinho - Ateliê Denise Borges", 
    page_icon="🛒", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÕES ---
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"
WHATSAPP_ADMIN = "19992709717" # Número da Denise

# --- ESTILIZAÇÃO CSS ---
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
    texto_pedido_planilha = ""
    texto_whatsapp = "Olá Denise! Gostaria de confirmar meu pedido:\n\n"
    
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
        texto_pedido_planilha += f"{item['item']}, "
        texto_whatsapp += f"• {item['item']} - R$ {item['preco']:.2f}\n"

    st.divider()
    st.markdown(f"### Total: R$ {total:.2f}")

    # BOTÃO PARA FINALIZAR
    if st.button("🚀 CONFIRMAR PEDIDO"):
        with st.spinner("Registrando na planilha..."):
            payload = {
                "action": "create",
                "nome": st.session_state.usuario['nome'],
                "whatsapp": st.session_state.usuario['zap'],
                "pedido": texto_pedido_planilha[:-2],
                "total": total
            }
            
            try:
                res = requests.post(URL_PLANILHA, json=payload)
                
                if res.status_code == 200:
                    st.success("✅ Pedido registrado com sucesso!")
                    
                    # PREPARAÇÃO DA MENSAGEM WHATSAPP
                    texto_final = texto_whatsapp + f"\n*Total: R$ {total:.2f}*\n*Cliente:* {st.session_state.usuario['nome']}"
                    texto_codificado = urllib.parse.quote(texto_final)
                    link_zap = f"https://wa.me/5519992709717?text={texto_codificado}"
                    
                    st.balloons()
                    
                    # BOTÃO DO WHATSAPP ESTILIZADO
                    st.markdown(f"""
                        <a href="{link_zap}" target="_blank" style="text-decoration: none;">
                            <div style="
                                background-color: #25D366; 
                                color: white; 
                                text-align: center; 
                                padding: 15px; 
                                border-radius: 15px; 
                                font-weight: bold; 
                                font-size: 18px;
                                margin-top: 10px;">
                                🟢 ENVIAR PEDIDO NO WHATSAPP DA DENISE
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.info("⚠️ **Atenção:** Para que a Denise veja seu pedido agora, clique no botão verde acima!")
                    
                    # Limpa o carrinho
                    st.session_state.carrinho = []
                else:
                    st.error("Erro ao salvar na planilha. Tente novamente.")
            except Exception as e:
                st.error(f"Falha técnica: {e}")

    if st.button("➕ Adicionar mais itens"):
        st.switch_page("pages/2_cardapio.py")

st.divider()
st.caption("Ateliê Doces Denise Borges - Feito com amor e oração.")

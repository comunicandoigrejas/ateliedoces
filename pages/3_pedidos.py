import streamlit as st
import requests
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Finalizar Pedido - Ateliê Denise Borges", 
    page_icon="🛒", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÕES ---
URL_PLANILHA = "https://script.google.com/macros/s/AKfycbwgRjd6uakrLSiry3hg4Uu43GUymgS-2Cm1x5sD8yXvp38W799MoG7XBnZT9JzGq2tViA/exec"
WHATSAPP_ADMIN = "19992709717"

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] {display: none;}
    .stApp { background-color: #FFF0F5; }
    div.stButton > button { 
        background-color: #25D366 !important; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 4em;
        width: 100%;
        font-size: 1.2em;
        border: none;
    }
    h1, h2, h3 { color: #4B0082 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if st.button("⬅️ Voltar ao Cardápio"):
    st.switch_page("pages/2_cardapio.py")

st.title("🛒 Finalizar Pedido")

if 'usuario' not in st.session_state or st.session_state.usuario is None:
    st.warning("Irmão, faça o login para continuar.")
    st.stop()

if not st.session_state.carrinho:
    st.info("Seu carrinho está vazio!")
else:
    total = 0
    texto_resumo = ""
    for item in st.session_state.carrinho:
        st.write(f"✅ {item['item']} - R$ {item['preco']:.2f}")
        total += item['preco']
        texto_resumo += f"• {item['item']} (R$ {item['preco']:.2f})\\n"

    st.divider()
    st.markdown(f"### Total: R$ {total:.2f}")

    # --- O BOTÃO MÁGICO DE UM CLIQUE ---
    if st.button("🟢 ENVIAR PEDIDO AGORA"):
        with st.spinner("Registrando e preparando WhatsApp..."):
            # 1. Registra na Planilha
            payload = {
                "action": "create",
                "nome": st.session_state.usuario['nome'],
                "whatsapp": st.session_state.usuario['zap'],
                "pedido": texto_resumo.replace("\\n", ", "),
                "total": total
            }
            
            try:
                res = requests.post(URL_PLANILHA, json=payload)
                
                if res.status_code == 200:
                    # 2. Prepara a mensagem do WhatsApp
                    msg = f"Olá Denise! Novo pedido:*\\n\\n"
                    msg += f"*Cliente:* {st.session_state.usuario['nome']}\\n"
                    msg += f"*Pedido:*\\n{texto_resumo}\\n"
                    msg += f"*Total:* R$ {total:.2f}"
                    
                    link_zap = f"https://api.whatsapp.com/send?phone=5519992709717&text={msg}"
                    
                    # 3. TRUQUE: JavaScript para abrir o link automaticamente
                    js = f"window.open('{link_zap}', '_blank');"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
                    
                    st.success("Glória a Deus! Pedido salvo e WhatsApp abrindo...")
                    st.balloons()
                    
                    # Limpa o carrinho
                    st.session_state.carrinho = []
                    
                    st.info("Se o WhatsApp não abrir automaticamente, clique no botão que apareceu na sua barra de endereços ou tente novamente.")
                else:
                    st.error("Erro ao salvar na planilha.")
            except Exception as e:
                st.error(f"Erro: {e}")

st.divider()
st.caption("Ateliê Doces Denise Borges")

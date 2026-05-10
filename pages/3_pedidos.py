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
        background-color: #8E44AD; 
        color: white !important; 
        border-radius: 15px; 
        font-weight: bold; 
        height: 4em;
        width: 100%;
        font-size: 1.1em;
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
    resumo_itens = ""
    for item in st.session_state.carrinho:
        st.write(f"✅ {item['item']} - R$ {item['preco']:.2f}")
        total += item['preco']
        resumo_itens += f"• {item['item']} (R$ {item['preco']:.2f})\n"

    st.divider()
    st.markdown(f"### Total: R$ {total:.2f}")

    # --- ESTADO DE CONFIRMAÇÃO ---
    if 'pedido_enviado' not in st.session_state:
        st.session_state.pedido_enviado = False

    if not st.session_state.pedido_enviado:
        if st.button("🚀 SALVAR PEDIDO E PREPARAR WHATSAPP"):
            with st.spinner("Registrando sua benção..."):
                payload = {
                    "action": "create",
                    "nome": st.session_state.usuario['nome'],
                    "whatsapp": st.session_state.usuario['zap'],
                    "pedido": resumo_itens.replace("\n", ", "),
                    "total": total
                }
                
                try:
                    res = requests.post(URL_PLANILHA, json=payload)
                    if res.status_code == 200:
                        st.session_state.pedido_enviado = True
                        st.rerun()
                    else:
                        st.error("Erro ao salvar na planilha. Tente novamente.")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
    else:
        # Após salvar, mostramos o botão VERDE que abre o WhatsApp sem bloqueio
        st.success("✅ Pedido salvo com sucesso na planilha!")
        st.balloons()
        
        # Prepara a mensagem
        quebra = "%0A"
        msg = f"Olá Denise! Novo pedido:* {quebra}{quebra}"
        msg += f"*Cliente:* {st.session_state.usuario['nome']}{quebra}"
        msg += f"*Itens:* {quebra}{resumo_itens.replace('\n', quebra)}"
        msg += f"*Total:* R$ {total:.2f}"
        
        link_zap = f"https://api.whatsapp.com/send?phone=55{WHATSAPP_ADMIN}&text={msg}"

        st.markdown(f"""
            <div style="text-align: center; background-color: #e8f5e9; padding: 20px; border-radius: 15px; border: 2px solid #25D366;">
                <p style="color: #1b5e20; font-weight: bold; font-size: 18px;">
                    🙏 Agora, clique abaixo para enviar à Denise:
                </p>
                <a href="{link_zap}" target="_blank" style="text-decoration: none;">
                    <div style="
                        background-color: #25D366; 
                        color: white; 
                        padding: 18px; 
                        border-radius: 12px; 
                        font-weight: bold; 
                        font-size: 20px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        🟢 ENVIAR PARA O WHATSAPP
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛒 Fazer outro pedido"):
            st.session_state.carrinho = []
            st.session_state.pedido_enviado = False
            st.switch_page("pages/2_cardapio.py")

st.divider()
st.caption("Ateliê Doces Denise Borges")

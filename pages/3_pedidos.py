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
                    st.success("✅ Pedido registrado na planilha!")
                    
                    # 1. Preparar a mensagem de forma limpa
                    quebra_linha = "%0A" # Código para pular linha no WhatsApp
                    texto_zap = f"Olá Denise! Novo pedido realizado:*%0A%0A"
                    texto_zap += f"*Cliente:* {st.session_state.usuario['nome']}{quebra_linha}"
                    texto_zap += f"*Pedido:* {texto_pedido_planilha[:-2]}{quebra_linha}"
                    texto_zap += f"*Total:* R$ {total:.2f}{quebra_linha}{quebra_linha}"
                    texto_zap += f"Aguardando sua confirmação! 🙌"

                    # 2. Criar o link direto
                    # O link api.whatsapp.com é mais universal que o wa.me em alguns navegadores
                    link_final = f"https://api.whatsapp.com/send?phone=55{WHATSAPP_ADMIN}&text={texto_zap}"

                    st.balloons()
                    
                    # 3. Botão com "Gatilho Automático" via HTML
                    st.markdown(f"""
                        <div style="text-align: center; margin-top: 20px;">
                            <a href="{link_final}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #25D366; 
                                    color: white; 
                                    border: none; 
                                    padding: 20px; 
                                    border-radius: 15px; 
                                    font-weight: bold; 
                                    font-size: 20px; 
                                    cursor: pointer;
                                    width: 100%;
                                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                                    🟢 CLIQUE AQUI PARA ENVIAR NO WHATSAPP
                                </button>
                            </a>
                            <p style="color: #666; font-size: 14px; margin-top: 10px;">
                                (Ao clicar, o seu WhatsApp abrirá com a mensagem pronta)
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Limpa o carrinho para evitar pedidos duplicados
                    st.session_state.carrinho = []
                    
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

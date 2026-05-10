import streamlit as st
import requests

if st.button("🚀 Confirmar e Enviar Pedido"):
    with st.spinner("Enviando pedido..."):
        payload = {
            "action": "create",
            "nome": st.session_state.usuario['nome'],
            "whatsapp": st.session_state.usuario['zap'],
            "pedido": texto_pedido[:-2],
            "total": total
        }
        
        try:
            res = requests.post(URL_PLANILHA, json=payload)
            # Verifica se a resposta não está vazia
            if res.text:
                resultado = res.json()
                if resultado.get("status") == "sucesso":
                    st.success("Pedido registrado na planilha!")
                    st.session_state.carrinho = []
                else:
                    st.error(f"Erro no Google: {resultado.get('message')}")
            else:
                st.error("O servidor do Google respondeu vazio.")
        except Exception as e:
            st.error(f"Erro ao processar resposta: {e}")
            # Se der erro de JSON, mostra o que veio do Google para você ler
            st.code(res.text[:200])

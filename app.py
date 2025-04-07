import google.generativeai as gemini
import streamlit as st
import time

st.title("Chatbot com Gemini")

# Sidebar
with st.sidebar:
    st.title("Configurações")
    st.markdown("---")

    # Link para documentação
    st.markdown("### Como obter a API KEY")
    st.markdown(
        """
    Para gerar sua API KEY, acesse a [Documentação oficial do Gemini](https://ai.google.dev/tutorials/setup).
    """
    )

    # Configurações do modelo
    st.markdown("### Configurações do Modelo")
    model_name = st.selectbox("Selecione o modelo", ["gemini-2.0-flash", "gemini-pro"])

    # Configuração da API KEY
    st.markdown("### Insira a sua API KEY")
    API_KEY = st.text_input(
        "API KEY", help="Cole aqui sua API KEY do Gemini"
    )

    if not API_KEY:
        st.error("Por favor, insira a sua API KEY")
        st.stop()

    try:
        gemini.configure(api_key=API_KEY)

    except Exception as e:
        st.error(f"Erro ao configurar a API: {str(e)}")
        st.stop()

# Inicializar o histórico de mensagens no session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "Gemini", "content": "Olá! como posso ajudar você hoje?"}
    ]

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua pergunta..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibir mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar e exibir resposta do assistente
    with st.chat_message("assistant"):
        try:
            with st.spinner("Gerando resposta..."):
                model = gemini.GenerativeModel(model_name)

                response = model.generate_content(prompt)

                st.markdown(response.text)

                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar a resposta: {str(e)}")
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Desculpe, ocorreu um erro: {str(e)}"}
            )

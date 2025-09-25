import streamlit as st
import requests

def render_chatbot(api_base_url):
    st.subheader("Ask the Crypto AI Agent")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask about crypto staking or trading"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query backend agent
        response = requests.post(f"{api_base_url}/agents/query", json={"query": prompt})
        if response.status_code == 200:
            answer = response.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            st.error("Failed to get response from AI agent")
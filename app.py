"""
Based off demo in https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
"""

import streamlit as st
from prompts import get_system_prompt, stream_model_response

st.title("Wildfire demo assessment")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

first_message = False
if "messages" not in st.session_state:
    messages = []
    st.session_state.messages = get_system_prompt(messages)
    first_message = True

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type response here"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

if prompt or first_message:
    model = st.session_state["openai_model"]
    messages = st.session_state.messages
    with st.chat_message("assistant"):
        messages = stream_model_response(messages, st.write_stream, model)
    st.session_state.messages = messages

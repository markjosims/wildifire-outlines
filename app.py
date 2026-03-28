"""
Based off demo in https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
"""

import streamlit as st
from chat import get_system_prompt, get_model_response, QuestionServer

st.title("Wildfire demo assessment")


@st.cache_resource
def get_question_server():
    return QuestionServer()


question_server = get_question_server()

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
    messages = st.session_state.messages
    with st.chat_message("assistant"):
        messages = get_model_response(messages, question_server, st.write)
    st.session_state.messages = messages

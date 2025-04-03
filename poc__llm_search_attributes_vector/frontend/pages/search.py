import json
import streamlit as st
import requests

from components.sidebar import sidebar
from components.chat_functions import stream_data


st.set_page_config(layout="wide")


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]


sidebar()
with st.sidebar:
    st.markdown("To reset chat history")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


with st.container():
    st.markdown(
        f'<h3 style="color:#F63366;">Vector Search</h3>',
        unsafe_allow_html=True
    )
    with st.expander(label="Utilities", expanded=True):
        col1, col3 = st.columns(2, gap="large")
        with col1:
            option = st.selectbox(
                    label="Which model would you like to choose?",
                    options=("bedrock/aws-titan", "bedrock/cohere-embed-english", "openai/text-embedding"),
                    index=None,
                    placeholder="Select model..."
                )

        with col3: 
            no_results = st.slider('Select number of results', min_value=1, max_value=10, value=3, step=1)



st.markdown("---")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if option is None:
        st.toast('Ensure you have selected a model!', icon="⚠️")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write_stream(stream_data(prompt))

    input = {
        "prompt" : prompt,
        "llm_name" : str(option),
        "llm_kwargs" : str({}),
        "no_results" : no_results
    }

    resp = requests.get(url="http://api:8000/v1/search/sim_search", data=json.dumps(input))

    msg = resp.json()["message"]

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write_stream(stream_data(msg))
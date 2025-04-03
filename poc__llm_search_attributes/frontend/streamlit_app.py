import streamlit as st
import requests
import json


with st.sidebar:
   st.markdown("---")
   st.markdown("# About")
   st.markdown(
       "This tool serves for demonstration purposes only. "
       "It allows you to write a query prompt to ask for candidates that have certain features."
   )
   st.markdown(
      "## Implemented Attributes"
   )
   st.markdown("- hair stryle")
   st.markdown("- hair color")
   st.markdown("- eye color")
   st.markdown("- height (cm / imperial)")
   st.markdown("- weight (kg / lbs)")
   st.markdown("- playable age (min / max)")
   st.markdown("- gender")
   st.markdown("- ethnicity")

   st.markdown("---")
   "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
   "[View the source code](https://github.com/castingnetworks/data-ml-pocs/tree/main/poc__llm_search_attributes)"

st.title("💬 Search Attribute Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
   st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
   st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
   st.session_state.messages.append({"role": "user", "content": prompt})
   st.chat_message("user").write(prompt)

   input = {"prompt" : prompt}
   resp = requests.get(url="http://api:8000/search", data=json.dumps(input))

   msg = resp.json()["message"]

   st.session_state.messages.append({"role": "assistant", "content": msg})
   st.chat_message("assistant").write(msg)
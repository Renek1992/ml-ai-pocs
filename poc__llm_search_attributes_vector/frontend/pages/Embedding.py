import streamlit as st
import polars as pl
import json
from components.sidebar import sidebar
import requests

st.set_page_config(layout="wide")

sidebar()


with st.container():
    st.markdown(
        f'<h3 style="color:#F63366;">Vector Embedding</h3>',
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
            no_profiles = st.selectbox(
                    label="How many profiles would you like to embed?",
                    options=(1, 10, 50, 100, 500, 1000),
                    index=None,
                    placeholder="Select a number..."
                )

with st.container():
    input = {
            "no_profiles" : no_profiles,
            "llm_name" : str(option),
            "llm_kwargs" : str({})
        }
    st.markdown("---")
    if st.button(label='Run', use_container_width=True, type="primary"):
        if option is None:
            st.toast('Ensure you have selected a model!', icon="⚠️")
        elif no_profiles is None:
            st.toast('Ensure you have selected the number of profiles to embed!', icon="⚠️")
        else:
            with st.spinner('Wait for it...'):
                resp = requests.post(url="http://api:8000/v1/embed/vector_embed", data=json.dumps(input))
                
                msg = json.loads(resp.text)['message']['result']
                data_preview = json.loads(resp.text)['message']['data_preview']
                df = pl.DataFrame(data_preview)
            if resp.status_code == 200:
                st.success(f"Done! {msg}")
                st.write(df)
                
                





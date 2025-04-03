import streamlit as st
import requests
import json

from components.sidebar import sidebar
from components.utilities import show_popup


st.set_page_config(layout="wide")

sidebar()

with st.sidebar:
        st.markdown("# About")
        st.markdown("It allows you to write a query prompt to ask for candidates that have certain features.")
        st.markdown("[View the source code](https://github.com/castingnetworks/data-ml-pocs/tree/main/poc__llm_search_attributes_vector)")

st.markdown(
        f'<h3 style="color:#F63366;">Project Info</h3>',
        unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Description", "Implemented Attributes"])

with tab1:
    st.markdown("""
        This project serves the demonstration of AI-generated vector embeddings performing a similar search (KNN) to retrieve suitable profiles given a prompt. The dataset used for embedding contains a total of 9 attributes reaching from hair color the gender. These attributes are being used to create a dossier for each profile which are being used for text embedding. Embeddings can be managed within the `Embedding` tab of this project. The generateed vector is stored in a sateless vector db and queried through a similarity search method.
    """)
    st. markdown("""The resulats are being stored within a chat window which can be found in the `Search` tab of this project.""")
    st.image("static/images/application_structure.svg", caption="Application Structure")

with tab2:
    # Example prompts
    box_texts = [
        "Text for Box 1",
        "Text for Box 2",
        "Text for Box 3",
        "Text for Box 4",
        "Text for Box 5",
        "Text for Box 6"
    ]

    # Arrange the boxes in a 3x2 grid
    col1, col2, col3 = st.columns(3)
    resp = ""
    with col1:
        if st.button("Hair Style"):
            resp = box_texts[0]

        if st.button("Hair Color"):
            resp = box_texts[1]

        if st.button("Gender"):
            resp = box_texts[3]
            


    with col2:
        if st.button("Eye Color"):
            resp = box_texts[3]

        if st.button("Height (cm / imperial)"):
            resp = box_texts[3]

        if st.button("Ethnicity"):
            resp = box_texts[3]


    with col3:
        if st.button("Weight (kg / lbs)"):
            resp = box_texts[3]

        if st.button("Playable age (min / max)"):
            resp = box_texts[3]

        if st.button("Skills & Willingness"):
            resp = box_texts[3]



    st.divider()
    show_popup(resp)
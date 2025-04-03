import streamlit as st
import time


def stream_data(input: str):
    for word in input.split(" "):
        yield word + " "
        time.sleep(0.025)
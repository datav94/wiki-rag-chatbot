# LOAD LIBRARIES
###########################################################################################
import streamlit as st
import os

import json
import requests
import itertools

import pandas as pd
import numpy as np

import logging
import sys
###########################################################################################

# LOGGER MODULE
###########################################################################################
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('llm-logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
###########################################################################################
def call_model(prompt):
    url = "http://localhost:8000/chat/"
    resp = requests.post(url, data=json.dumps(prompt))
    if resp.status_code == 200:
        return resp.json()
    else:
        return resp.text

################################## STREAMLIT APP ##########################################
###########################################################################################
# App title
st.set_page_config(page_title="⌛💬 RAG Wikipedia assistant")

st.markdown(
""" <style>     
    [data-testid=stSidebar] 
    {         background-color: #1d0638;     } 
</style> 
"""
, unsafe_allow_html=True)

#clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Questions about Turing machine, Graph theory or AI only"}]


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Questions about Turing machine, Graph theory or AI only"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def generate_model_response(prompt_input):
    prompt = {
        "messages": st.session_state.messages
    }
    response_data = call_model(prompt)
    output = response_data["response"]
    print(output)
    return output

# Replicate Credentials
with st.sidebar:
    logo_path = r"C:\Users\WMD8P34\rag_app\logo.jpg"
    st.image(logo_path, use_column_width="auto") # side bar logo
    with st.container(height=680):
        st.empty()

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_model_response(prompt)
            response = response["response"]
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)


    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
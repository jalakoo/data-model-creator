# Retrieve from streamlit secrets or .env
import streamlit as st
import logging

OPENAI_API_KEY = None
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    logging.info(f'No OPENAI API key found in Streamlit secrets')

# TODO: if not found in secrets, try .env
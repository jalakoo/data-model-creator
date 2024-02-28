# Retrieve from streamlit secrets or .env
import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# TODO: if not found in secrets, try .env
from llm_manager import update_openai_key, DEFAULT_PROMPT_TEMPLATE,SAMPLE_PROMPT
from secrets_manager import OPENAI_API_KEY
import streamlit as st

def llm_config_ui():

    # Check if OpenAI Key already available
    start_open = False
    if OPENAI_API_KEY is None or OPENAI_API_KEY == "":
        start_open = True

    # st.markdown("Variation of Varun Shenoy's original [GraphGPT](https://graphgpt.vercel.app) to convert a natural language description into a graph data model")

    with st.expander("LLM Configuration", expanded = start_open):

        # OPENAI TEXTFIELD
        new_open_ai_key = st.text_input(f'OpenAI KEY', type="password", value=OPENAI_API_KEY)

        if new_open_ai_key is None or new_open_ai_key == "":
            st.warning(f'OpenAI API Key required to use this app')
            st.stop()
            return
        
        update_openai_key(new_open_ai_key)
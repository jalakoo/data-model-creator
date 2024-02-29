from llm_manager import DEFAULT_PROMPT_TEMPLATE,SAMPLE_PROMPT
import streamlit as st
import logging

def prompt_ui():

    column_height = 340
    c1, c2 = st.columns(2)

    with c1:

        # Template
        if "PROMPT_TEMPLATE" not in st.session_state:
            st.session_state["PROMPT_TEMPLATE"] = DEFAULT_PROMPT_TEMPLATE

        def update_template(value):                    
            st.session_state.template_textarea = value

        if st.button("Load Default Template", on_click=update_template, args=[DEFAULT_PROMPT_TEMPLATE]):
            pass
        
        template = st.text_area(
            "Template", 
            key="template_textarea",
            value=st.session_state["PROMPT_TEMPLATE"],height = column_height)
        st.session_state["TEMPLATE"] = template
        

    with c2:

        # Prompt
        if "SAMPLE_PROMPT" not in st.session_state:
            st.session_state["SAMPLE_PROMPT"] = ""

        if st.button('Load Sample', key="graphgpt_sample"):
            # Will only load once. Any edits to prompt will not reload sample
            st.session_state.SAMPLE_PROMPT = SAMPLE_PROMPT

        prompt = st.text_area("Prompt", 
                              value=st.session_state.SAMPLE_PROMPT,
                              height = column_height)
        
        st.session_state["PROMPT"] = prompt
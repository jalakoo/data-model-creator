from arrows_ui import arrows_ui
from config_ui import llm_config_ui
from prompt_ui import prompt_ui
from graph_ui import graph_ui
import streamlit as st
import logging

# Heavy import support
# Needed in cloud hosted instances such as Google Cloud
from pathlib import Path
from streamlit.config import on_config_parsed
from streamlit.web import cli
import sys

# Logging config
logging.getLogger().setLevel(logging.DEBUG)

# noinspection PyUnresolvedReferences
def heavy_imports() -> None:
    """For an explanation, please refer to this thread -
    https://discuss.streamlit.io/t/any-ideas-on-your-app-is-having-trouble-loading-the-
    st-aggrid-aggrid-component/10176/19?u=vovavili"""
    from streamlit_agraph import agraph, Node, Edge, Config

def main()-> None:

    # Heavy import support
    on_config_parsed(heavy_imports)
    sys.argv.extend(
        [
            "run",
            str(Path(__file__).resolve().parent / "app.py"),
            "--server.port=8080",
            "--server.address=0.0.0.0",
        ]
    )

    # SETUP
    st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

    # UI
    llm_config_ui()
    prompt_ui()
    graph_ui()
    arrows_ui()

if __name__ == "__main__":
    main()
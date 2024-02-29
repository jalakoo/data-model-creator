import streamlit as st
import streamlit.components.v1 as components
import logging
            
def arrows_ui():
    with st.expander("Arrows - Graph Data Model Editor"):
        
        st.markdown(
            """
            Embedded [arrows.app](https://arrows.app/)
            """
        )

        uri = "https://arrows.app"

        # Load prior arrows uri - if there is one
        if "ARROWS_URI" in st.session_state:
            prior_uri = st.session_state["ARROWS_URI"]
            logging.info(f'Previously saved arrows uri: {prior_uri}')
            if prior_uri is not None:
                uri = prior_uri
                logging.info(f'Previously saved arrows uri should have loaded')
        else:
            logging.info(f'No prior arrows uri found. Uri: {uri}')

        # Load arrows into an iframe
        components.html(
            f"""
            <iframe src="{uri}"
                width=100% height="600">
            </iframe>
            """, height=600, scrolling=False
            )
        
        logging.info(f'Arrows source URI rendered: {uri}')

        # st.session_state["ARROWS_URI"] = None
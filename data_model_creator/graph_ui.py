from arrows_utils import arrows_dictionary, arrows_uri
from llm_manager import generate_openai_response
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import json
import logging
import ast

# Original version using openai model that DOES NOT support json output
def agraph_nodes_edges(response: str | list) -> tuple[list[Node], list[Edge]]:
    """
    Converts an openai response into agraph nodes and relationships

    Args:
        response: String or list in the format of [["node_id_string", "edge_id_string", "another_node_id_string"],...]
    
    Returns:
        A tuple of agraph nodes in a list and agraph edges in a list

    Raises:
        ...
    """
    logging.debug(f'agraph_nodes_edges() response recieved: {response}')
    # Response will be a list of 3 item tuples

    answers = None

    # Convert to list of lists - if needed
    if isinstance(response, str):
        try:
            answers = json.loads(response)
            logging.info(f'JSON parsed response: {answers}')
        except:
            logging.debug(f'Unable to parse string to list with json.loads. Attempting ast...')
            try: 
                answers = ast.literal_eval(response)
            except:
                logging.debug(f'Unable to parse string to list with ast.literal_eval. String format was unexpected.')
    else:
        answers = response
    
    if isinstance(answers, dict):
        # Sometimes openai will return answers with single key dict (that key could be relationships, data, etc)
        key = list(answers.keys())[0]
        answers = answers.get(key, None)

    logging.debug(f'Processing answers: {answers}')

    if isinstance(answers, list) is False:
        raise Exception(f'Answers is not a list: {answers}')

    nodes = set()
    result_edges = []

    answers_dedupped = [t for t in {tuple(r) for r in answers}]

    logging.debug(f'Answers dedupped: {answers_dedupped}')

    for item in answers_dedupped:
        # Each should be a tuple of 3 items, node-edge-node
        n1 = item[0]
        r = item[1]
        n2 = item[2]

        # Standardize casing
        r = r.upper()
        n1 = n1.title()
        n2 = n2.title()

        nodes.add(n1)
        nodes.add(n2) 

        edge = Edge(source=n1, target=n2, label=r)
        result_edges.append(edge)

    result_nodes = []
    for node_label in list(nodes):
        node = Node(id=node_label, label=node_label)
        result_nodes.append(node)

    logging.debug(f'Nodes returning: {result_nodes}')
    logging.debug(f'Edges returning: {result_edges}')

    return result_nodes, result_edges
    
def agraph_from_sample(prompt: str):
    # TODO: Pull from a file of samples
    openai_response = '[["Sharks", "eat", "big fish"], ["Big fish", "eat", "small fish"], ["Small fish", "eat", "bugs"]]'
    nodes, edges = agraph_nodes_edges(openai_response)
    config = Config(height=400, width=1000, directed=True)

    if nodes is not None:
        agraph(nodes=nodes, 
            edges=edges, 
            config=config) 
        
def graph_ui():

    template = st.session_state.get("PROMPT_TEMPLATE", "")

    prompt = st.session_state.get("PROMPT", None)
    if prompt is None or prompt == "":
        st.stop()
        return
    
    nodes = None
    edges = None

    # Send completion request to openAI
    full_prompt = template + prompt
    response = generate_openai_response(full_prompt)

    # Convert response to agraph nodes and edges
    try:
        nodes, edges = agraph_nodes_edges(response)
    except Exception as e:
        logging.error(f'Problem converting response to agraph nodes and edges. Error: {e}')
        st.error(f'Problem converting prompt to graph. Please try again or rephrase the prompt')

    # Configure and display agraph
    config = Config(width=1000, height=400, directed=True)
    if nodes is None:
        return
    
    # Display data
    st.write('Graph Viewer')
    agraph(nodes=nodes,
        edges=edges,
        config=config)
    
    # For displaying JSON schema. This can be quite long though
    # st.write('JSON Representation')
    # arrows_str = json.dumps(arrows_dict, indent=4)
    # st.code(arrows_str)

    # Prep arrows compatible dictioary for button options


    if st.button("Edit in Arrows"):

        arrows_dict = arrows_dictionary(nodes, edges)

        # Prep arrows compatible json
        uri = arrows_uri(arrows_dict)

        logging.info(f'Arrows URI generated: {uri}')

        st.session_state["ARROWS_URI"] = uri

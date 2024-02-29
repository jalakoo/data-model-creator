from streamlit_agraph import agraph, Node, Edge, Config
import json
import logging
import random
import base64

def arrows_uri(input: str | dict) -> str:
    """
    Generates a URI for an arrows app visualization from a json object. WARNING! May overwrite existing arrows drawing.

    Args:
        input: A dictionary or string representing an arrows compatible .json configuration

    Returns:
        A string URI for an arrows app visualization
    """

    # Convert dict to string if needed
    if isinstance(input, dict):
        input = json.dumps(input, default=str)

    # Convert the diction object into a base 64 json string
    b = input.encode('utf-8')
    base64_str = base64.b64encode(b).decode('utf-8')

    result = f"https://arrows.app/#/import/json={base64_str}"

    # logging.debug(f'\n\nOutput arrows uri from {input} with base64 JSON: \n{result}')

    return result


def arrows_dictionary(nodes: list[Node], edges: list[Edge], name: str = "GraphGPT Generated Model") -> dict:
    """
    Generates an arrows.app compatible .json file from agraph nodes and edges

    Args:
        nodes: List of agraph Nodes
        edges: List of agraph Edges

    Returns:
        A dictionary matching arrows .json schema
    """
    result_nodes = []
    result_relationships = []
    for n in nodes:
        random_x = round(random.uniform(-600, 600), 14)
        random_y = round(random.uniform(-600, 600), 14)
        result_nodes.append({
            "id": n.id,
            "position":{
                "x" : random_x,
                "y": random_y
            },
            "caption": n.label,
            "style":{},
            "labels":[],
            "properties":{}
        })
    for idx, e in enumerate(edges):
        logging.debug(f'Processing edge to relationships: {e.__dict__}')
        ns = e.source
        nt = e.to
        type = e.label.replace(" ", "_")
        result_relationships.append(
            {
                "id":f"n{idx}",
                "type":type,
                "fromId":ns,
                "toId":nt,
                "style":{},
                "properties":{}
            }
        )
    result = {
        "graph": {
            "style": {
            "font-family": "sans-serif",
            "background-color": "#ffffff",
            "background-image": "",
            "background-size": "100%",
            "node-color": "#ffffff",
            "border-width": 4,
            "border-color": "#000000",
            "radius": 50,
            "node-padding": 5,
            "node-margin": 2,
            "outside-position": "auto",
            "node-icon-image": "",
            "node-background-image": "",
            "icon-position": "inside",
            "icon-size": 64,
            "caption-position": "inside",
            "caption-max-width": 200,
            "caption-color": "#000000",
            "caption-font-size": 50,
            "caption-font-weight": "normal",
            "label-position": "inside",
            "label-display": "pill",
            "label-color": "#000000",
            "label-background-color": "#ffffff",
            "label-border-color": "#000000",
            "label-border-width": 4,
            "label-font-size": 40,
            "label-padding": 5,
            "label-margin": 4,
            "directionality": "directed",
            "detail-position": "inline",
            "detail-orientation": "parallel",
            "arrow-width": 5,
            "arrow-color": "#000000",
            "margin-start": 5,
            "margin-end": 5,
            "margin-peer": 20,
            "attachment-start": "normal",
            "attachment-end": "normal",
            "relationship-icon-image": "",
            "type-color": "#000000",
            "type-background-color": "#ffffff",
            "type-border-color": "#000000",
            "type-border-width": 0,
            "type-font-size": 16,
            "type-padding": 5,
            "property-position": "outside",
            "property-alignment": "colon",
            "property-color": "#000000",
            "property-font-size": 16,
            "property-font-weight": "normal"
            },
            "nodes":result_nodes,
            "relationships":result_relationships,
            "diagramName": name
        }
    }

    logging.debug(f'\n\nProcessed incoming nodes: {nodes}, edges: {edges} to:\n {result}')
    
    return result


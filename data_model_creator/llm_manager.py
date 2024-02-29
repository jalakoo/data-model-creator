
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from secrets_manager import OPENAI_API_KEY
import logging
import openai
import os
import streamlit as st

# TODO: secrets/.env flag to swith between LLM options

# Using GPT4All
# from gpt4all import GPT4All
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.chains import LLMChain
# from langchain_community.llms import GPT4All
# from langchain_community.embeddings import GPT4AllEmbeddings
# local_gpt4all_path = (
#     # "mistral-7b-instruct-v0.1.Q4_0.gguf"
#     "gpt4all-falcon-newbpe-q4_0.gguf"
# )
# # Callbacks support token-wise streaming
# CALLBACKS = [StreamingStdOutCallbackHandler()]
# # Verbose is required to pass to the callback manager
# LLM = GPT4All(model=local_gpt4all_path, callbacks=CALLBACKS, verbose=True)
# EMBEDDINGS = GPT4AllEmbeddings()


# Using OpenAI
 
# LLM = ChatOpenAI(temperature=0)
# EMBEDDINGS = OpenAIEmbeddings()

# Variation of Varun Shenoy's original [GraphGPT](https://graphgpt.vercel.app) to convert a natural language description into a graph data model
DEFAULT_PROMPT_TEMPLATE = f"""
    Given a prompt, extrapolate the most important Relationships. 

    Each Relationship must connect 2 Entities represented as an item list like ["ENTITY 1", "RELATIONSHIP", "ENTITY 2"]. The Relationship is directed, so the order matters.

    Use singular nouns for Entities.

    For example; the prompt: `All birds like to eat seeds` should return: ["Bird", "EATS", "Seed"]

    Limit the list to a maximum of 12 relationships. Prioritize item lists with Entities in multiple item lists. Remove duplicates.

    prompt:
    
    """

SAMPLE_PROMPT = "Sharks eat big fish. Big fish eat small fish. Small fish eat bugs."

def update_openai_key(key: str):
    os.environ["OPENAI_API_KEY"] = key
    openai.api_key = OPENAI_API_KEY # This may not work in a Google Cloud Run instance


@st.cache_data
def generate_openai_response(prompt)-> str:
    # TODO: Make this configurable
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-4",
        response_format={"type":"json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON"},
            {"role": "user", "content": prompt}
            ]
    )
    # TODO: Validate reponse
    content = response.choices[0].message.content
    logging.debug(f'OpenAI Response: {response}, type: {type(content)}')
    return content
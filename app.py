from enum import Enum
import streamlit as st
from langchain.chains import RetrievalQA

from second_brain_assistant.vectorstore import vector_client
from second_brain_assistant.llm import llm_client


class ChainType(str, Enum):
    stuff = 'stuff'
    map_reduce = 'map_reduce'
    map_rerank = 'map_rerank'
    refine = 'refine'


def generate_response(query, chain_type=ChainType.refine):
    # Create retriever interface
    retriever = vector_client.as_retriever()
    # Create QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm_client,
        chain_type=chain_type,
        retriever=retriever
    )
    return qa.run(query)


# Page title
title = '🧠 Second Brain Assistant App'
st.set_page_config(page_title=title)
st.title(title)

chain_type = st.selectbox(
    'Select a chain type:',
    options=[e.value for e in ChainType]
)

# Query text
query = st.text_input(
    'Enter your question:', placeholder='Please provide a short summary.')

# Form input and query
result = []
response = ''
with st.form('myform', clear_on_submit=True):
    submitted = st.form_submit_button(
        'Submit', disabled=not query)
    if submitted:
        with st.spinner('Calculating...'):
            response = generate_response(query, ChainType(chain_type))
            result.append(response)

if len(result):
    st.info(response)

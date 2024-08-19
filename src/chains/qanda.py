"""
This module defines the question answering logic for the RAG chatbot, including prompt templates and chain definitions.
"""
import os
import torch

from typing import List
from operator import itemgetter

from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnableBranch
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever

from .retrieval import get_retriever
from .extractors import extract_history, extract_question, format_context
from .gptcache_utils import get_hashed_name, GPTCache, init_gptcache, set_llm_cache
from .models_loader import tokenizer, model, embeddings_model, vector_store, pipe, chat_model

set_llm_cache(GPTCache(init_gptcache))


## All prompt strings
is_question_about_wikipedia_docs = """
You are estimating if the question is related with provided wikipedia documents or docs that are about Turing Machine, Graph Theory and Artificial Intelligence or something from a very different field. 

Here are some examples:

Question: Knowing this followup history: What is a turing machine ?, classify this question: what is a turing test ?
Expected Response: Yes

Question: Knowing this followup history: Provide information on Graph theory. , classify this question: Who are the applications of Graph theory ?
Expected Response: Yes

Question: Knowing this followup history: What is AI ?, classify this question: give me more details
Expected Response: Yes

Question: Knowing this followup history: What is AI ?, classify this question: Tell me a story about Germany.
Expected Response: No

Question: Knowing this followup history: Who invented Turing machine ?, classify this question: Write me a song.
Expected Response: No

Only answer with "yes" or "no". 

Knowing this followup history: {chat_history}, classify this question: {question}
"""


generate_query_to_retrieve_context_template = """
Based on the question below
generate a query for an vector search to retrieve relevant documents so that we can better answer the question.
The query should be in natual language. The external data source uses similarity search to search for relevant documents in a vector space. 
So the query should be similar to the relevant documents semantically. Answer with only the query. Do not add explanation.

Question: {question}
"""


question_with_history_and_context_str = """
You are a trustful assistant for wikipedia documents on Turing Machine, Graph Theory and Artificial Intelligence. 
The users are students, professionals, college professors and other education providers and receivers.
You are only allowed to answer questions wikipedia documents on Turing Machine, Graph Theory and Artificial Intelligence that will be provided as context. 
If you do not know the answer to a question, you truthfully say you do not know. Read the discussion to get the context of the previous conversation. 
In the chat discussion, you are referred to as "assistant". The user is referred to as "user".

Discussion: {chat_history}

Here's some context which might or might not help you answer: {context}

based on above answer the question: {question}
"""

## All prompt templates
is_question_about_wikipedia_docs_prompt = PromptTemplate(
  input_variables= ["chat_history", "question"],
  template = is_question_about_wikipedia_docs
)

generate_query_to_retrieve_context_prompt = PromptTemplate(
  input_variables= ["question"],
  template = generate_query_to_retrieve_context_template
)

question_with_history_and_context_prompt = PromptTemplate(
  input_variables= ["chat_history", "context", "question"],
  template = question_with_history_and_context_str
)


## Chains
retriever = get_retriever()

is_about_wiki_docs_chain = (
    {
        "question": itemgetter("messages") | RunnableLambda(extract_question),
        "chat_history": itemgetter("messages") | RunnableLambda(extract_history),
    }
    | is_question_about_wikipedia_docs_prompt
    | chat_model
    | StrOutputParser()
)


relevant_question_chain = (
  RunnablePassthrough() |
  {
    "relevant_docs": generate_query_to_retrieve_context_prompt | chat_model | StrOutputParser() | retriever,
    "chat_history": itemgetter("chat_history"), 
    "question": itemgetter("question")
  }
  |
  {
    "context": itemgetter("relevant_docs"),
    "chat_history": itemgetter("chat_history"), 
    "question": itemgetter("question")
  }
  |
  {
    "prompt": question_with_history_and_context_prompt,
  }
  |
  {
    "result": itemgetter("prompt") | chat_model | StrOutputParser(),
  }
)

irrelevant_question_chain = (
  RunnableLambda(lambda x: {"result": 'I cannot answer questions that are not about Turing Machine, Graph Theory or AI'})
)
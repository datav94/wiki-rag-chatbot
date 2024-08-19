"""
This module defines the retrieval logic for the RAG chatbot, utilizing the MultiQueryRetriever.
"""

from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from .config import (
    MODEL_ID,
    MODEL_CACHE_DIR,
    EMBEDDINGS_MODEL_ID,
    ACCESS_TOKEN,
    CHROMA_PERSIST_DIRECTORY,
    SEARCH_K
)
from .gptcache_utils import get_hashed_name, GPTCache, init_gptcache, set_llm_cache
from .models_loader import tokenizer, model, embeddings_model, vector_store, chat_model

set_llm_cache(GPTCache(init_gptcache))



multi_query_str = """
You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents based on the question as well as the chat history from a vector
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search.
Provide these alternative questions separated by newlines.

Original question: {question}
"""

multi_query_prompt = PromptTemplate(
    input_variables=["question"],
    template=multi_query_str,
)

# Chain
multi_query_chain = multi_query_prompt | chat_model | StrOutputParser()

def get_retriever():
    """
    Sets up and returns the MultiQueryRetriever for document retrieval.

    Returns:
        MultiQueryRetriever: The configured retriever instance.
    """

    retriever = MultiQueryRetriever(
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        llm_chain=multi_query_chain,
        parser_key="lines"
    )

    return retriever
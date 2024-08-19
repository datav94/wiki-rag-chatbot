"""
This module orchestrates the entire flow of the RAG chatbot, from question classification to final response generation.
"""
from operator import itemgetter
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnableBranch
from langchain.schema.runnable import RunnablePassthrough
from .qanda import (
  is_about_wiki_docs_chain,
  relevant_question_chain,
  irrelevant_question_chain,
  extract_question,
  extract_history
)

branch_node = RunnableBranch(
  (lambda x: "yes" in x["question_is_relevant"].lower(), relevant_question_chain),
  (lambda x: "no" in x["question_is_relevant"].lower(), irrelevant_question_chain),
  irrelevant_question_chain
)

full_chain = (
  {
    "question_is_relevant": is_about_wiki_docs_chain,
    "question": itemgetter("messages") | RunnableLambda(extract_question),
    "chat_history": itemgetter("messages") | RunnableLambda(extract_history),    
  }
  | branch_node
)
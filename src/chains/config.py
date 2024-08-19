"""
This module centralizes configuration settings for the RAG chatbot application.
"""

import os
from dotenv import load_dotenv

load_dotenv("./src/secrets.env")

# Model-related settings
MODEL_ID = "google/flan-t5-large"
EMBEDDINGS_MODEL_ID = "BAAI/bge-small-en-v1.5"
ACCESS_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Retrieve from environment variable

# Paths and directories
MODEL_CACHE_DIR = "./model_cache_dir"
CHROMA_PERSIST_DIRECTORY = "./chroma_langchain_db"

# Other settings
SEARCH_K = 3  # Number of documents to retrieve from Chroma

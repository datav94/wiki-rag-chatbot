from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_chroma import Chroma
from langchain_community.llms import HuggingFaceHub
from .config import (
    MODEL_ID,
    MODEL_CACHE_DIR,
    EMBEDDINGS_MODEL_ID,
    ACCESS_TOKEN,
    CHROMA_PERSIST_DIRECTORY,
    SEARCH_K
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID, 
    cache_dir=MODEL_CACHE_DIR + "\\tokenizer", 
    token=ACCESS_TOKEN,
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_ID, 
    load_in_8bit=False, 
    cache_dir=MODEL_CACHE_DIR + "\\chatmodel", 
    token=ACCESS_TOKEN
)

embeddings_model = HuggingFaceEmbeddings(
    model_name = EMBEDDINGS_MODEL_ID,
    model_kwargs = {'device': 'cpu'},
    cache_folder = MODEL_CACHE_DIR + "\\embeddings"
)

vector_store = Chroma(
    collection_name="wikipedia_collection",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PERSIST_DIRECTORY,
)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

chat_model = HuggingFacePipeline(pipeline=pipe)
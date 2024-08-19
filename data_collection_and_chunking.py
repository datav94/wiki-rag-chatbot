from uuid import uuid4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

model_cache_dir = r"C:\Users\WMD8P34\langchain-complete\model_cache_dir"

embeddings_model_id = "BAAI/bge-small-en-v1.5"
embeddings_model = HuggingFaceEmbeddings(
    model_name = embeddings_model_id,
    model_kwargs = {'device': 'cpu'},
    cache_folder = model_cache_dir + "\\embeddings"
)

vector_store = Chroma(
    collection_name="wikipedia_collection",
    embedding_function=embeddings_model,
    persist_directory="./chroma_langchain_db",
)

def download_wikipedia_pages(page_title):
  documents = WikipediaLoader(
    query=page_title, 
    load_max_docs=10,
    lang="en",
    ).load()
  return documents
    

def chunk_and_embed_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=300, 
      chunk_overlap=50
    )

    texts = text_splitter.split_documents(documents)

    embeddings = embeddings_model
    uuids = [str(uuid4()) for _ in range(len(texts))]
    vector_store.add_documents(texts, ids=uuids)

page_titles = ["Turing machine", "Graph Theory", "Artificial Intelligence"]
docs = [download_wikipedia_pages(page_title) for page_title in page_titles]

for doc in docs:
  chunk_and_embed_documents(doc)
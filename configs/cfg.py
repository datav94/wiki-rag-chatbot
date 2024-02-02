import os

NUM_REPLICAS = os.getenv('NUM_REPLICAS', 1)
NUM_CPUS = os.getenv('NUM_CPUS', 2)
NUM_GPUS = os.getenv('NUM_GPUS', 1)
MODEL_NAME = os.getenv('MODEL_NAME', 'nsql_ggml-model-q8_0.gguf')
MODEL_URL = os.getenv('MODEL_URL', 'https://storagenlisasho.blob.core.windows.net/container-nli-sasho/nsql_ggml-model-q8_0.gguf?sp=r&st=2023-12-27T16:19:56Z&se=2024-01-31T00:19:56Z&sv=2022-11-02&sr=c&sig=LnqivTmZvd7G3Sse4bCHyvdcm6hc4qh%2FmYDB5YQ1d5s%3D')
VECTOR_DB_URL = os.getenv('VECTOR_DB_URL', 'http://51.105.198.59:6333/')
VECTOR_DB_COLLECTION_NAME = os.getenv('VECTOR_DB_COLLECTION_NAME', 'SQLtables')
VECTOR_DB_LIMIT = os.getenv('VECTOR_DB_LIMIT', 5)
SCHEMA_PATH = os.getenv('SCHEMA_PATH', 'db/schema_example.txt')
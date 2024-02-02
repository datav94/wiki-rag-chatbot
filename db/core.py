from qdrant_client import QdrantClient
from db.utils import read_tables, responses_to_str
import logging

logger = logging.getLogger("ude-nli." + __name__)

class VectorDB:
    def __init__(self, url: str) -> None:
        self.client = QdrantClient(url)

    def update(self, schema_path: str, collection_name: str) -> None:
        """
        The function updates a collection in a database with documents read from a schema file.
        
        :param schema_path: The `schema_path` parameter is a string that represents the path to the
        schema file. This file contains the structure and definition of the tables or documents that
        need to be added to the collection
        :type schema_path: str
        :param collection_name: The `collection_name` parameter is a string that represents the name of
        the collection where the documents will be added
        :type collection_name: str
        """
        docs = read_tables(schema_path)        
        self.client.add(
            collection_name=collection_name,
            documents=docs
        )
    
    def search(self, query_text: str, collection_name: str, limit: int) -> str:
        """
        The function takes a query text, collection name, and limit as input, and returns the query
        responses as a string.
        
        :param query_text: The query text is the text that you want to search for in the collection. It
        can be a single word, a phrase, or a combination of words
        :type query_text: str
        :param collection_name: The collection_name parameter is the name of the collection in which you
        want to search for the query_text. It is the name of the database table or collection where the
        data is stored
        :type collection_name: str
        :param limit: The "limit" parameter specifies the maximum number of results that should be
        returned by the search query. It determines how many documents will be included in the response
        :type limit: int
        :return: a string.
        """
        query_responses = self.client.query(collection_name=collection_name, query_text=query_text, limit=limit)
        return responses_to_str(query_responses=query_responses)

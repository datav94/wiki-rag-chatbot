import logging

logger = logging.getLogger("ude-nli." + __name__)


def read_tables(path: str) -> list:
    """
    The function `read_tables` reads the content of a file at the given path, splits it into separate
    entries based on double line breaks, and returns a list of the entries.
    
    :param path: The `path` parameter is a string that represents the file path of the file you want to
    read. It should include the file name and extension. For example, if the file is located in the same
    directory as your Python script and its name is "data.txt", the `path` parameter would
    :return: The function `read_tables` returns a list of entries. Each entry is a string representing a
    table read from the file at the specified path.
    """

    with open(path, "r") as file:
        file_content = file.read()
    entries = file_content.split("\n\n")
    entries = [entry.strip() for entry in entries]
    return entries


def responses_to_str(query_responses: list) -> str:
    """
    The function "responses_to_str" takes a list of query responses and returns a string containing the
    documents from each response, separated by newlines.
    
    :param query_responses: A list of objects representing the responses to a query. Each object has a
    "document" attribute that contains the text of the response
    :type query_responses: list
    :return: a string that contains all the documents from the list of query responses. Each document is
    separated by a new line character.
    """
    return '\n'.join([i.document for i in query_responses])
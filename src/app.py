"""
This module defines a FastAPI-based API for serving the RAG chatbot's full_chain.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from chains.full_chain import full_chain

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list 

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Handles chat requests and generates responses using the full_chain.

    Args:
        request (ChatRequest): The chat request containing the message history.

    Returns:
        dict: A dictionary containing the generated response.
    """
    response = full_chain.invoke(request.dict())
    return {"response": response['result']} 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
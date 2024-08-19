"""
This module provides utilities for initializing and working with GPTCache.
"""

import hashlib
from langchain.globals import set_llm_cache
from gptcache import Cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from langchain_community.cache import GPTCache

def get_hashed_name(name):
    """
    Generates a hashed name for a given string using SHA-256.

    Args:
        name (str): The string to hash.

    Returns:
        str: The hexadecimal representation of the SHA-256 hash.
    """
    return hashlib.sha256(name.encode()).hexdigest()

def init_gptcache(cache_obj: Cache, llm: str):
    """
    Initializes a GPTCache instance with the specified LLM and cache settings.

    Args:
        cache_obj (Cache): The GPTCache object to initialize.
        llm (str): The name or identifier of the LLM being used.
    """
    hashed_llm = get_hashed_name(llm)
    cache_obj.init(
        pre_embedding_func=get_prompt,
        data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
    )

set_llm_cache(GPTCache(init_gptcache))
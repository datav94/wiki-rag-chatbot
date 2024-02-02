import logging

logger = logging.getLogger("ude-nli." + __name__)


def nlp_to_sql_prompt(query: str, schema: str) -> str:
    if not query:
        logger.error("The 'query' arugment is empty")
        raise ValueError("The 'query' argument must not be empty")
    if not schema:
        logger.warning("The 'schema' arugment is empty")
        # not raising an error since the LLM can return a valid statement in some cases even without schema
    prompt = f"""{schema}
    
-- Using valid SQLite, answer the following questions for the tables provided above.

-- {query}

SELECT"""
    return prompt

"""
Chat session management functionality for LLM interactions.
"""

import logging
from google import genai
from google.api_core import retry

# Set up logging
logger = logging.getLogger(__name__)

def create_chat_session(
    client = None,
    model_name: str = 'gemini-2.0-flash'
):
    """
    Creates a new chat session with the specified model.
    
    Args:
        client: The Google Generative AI client
        model_name (str): Name of the model to use
        
    Returns:
        ChatSession: Initialized chat session
    """
    try:
        is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

        if not hasattr(genai.models.Models.generate_content, '__wrapped__'):
          genai.models.Models.generate_content = retry.Retry(
              predicate=is_retriable)(genai.models.Models.generate_content)

        chat = client.chats.create(model=model_name)
        return chat
    
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        raise 
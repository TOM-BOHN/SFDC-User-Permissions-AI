"""
Functions for evaluating permissions using LLM models.
"""

#!pip install -Uq "google-genai==1.7.0"

from google import genai
from google.genai import types
from google.api_core import retry

from IPython.display import Markdown, display

genai.__version__

import enum
from typing import Tuple, Optional
import logging
import json

from .chat_session import create_chat_session

# Set up logging
logger = logging.getLogger(__name__)

class RiskRating(enum.Enum):
    """
    Enumeration of risk rating levels for permissions.
    """
    MISSION_CRITICAL = '5'
    RESTRICTED = '4'
    SENSITIVE = '3'
    CONTROLLED = '2'
    GENERAL = '1'

    @classmethod
    def from_string(cls, value: str) -> 'RiskRating':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid risk rating value: {value}. Defaulting to GENERAL.")
            return cls.GENERAL

def risk_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
    expanded_description: str,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None

) -> Tuple[str, RiskRating]:
    """
    Evaluates a permission using an LLM to determine its risk rating.
    
    Args:
        prompt (str): Template prompt for evaluation
        name (str): Permission name
        api_name (str): API name of the permission
        description (str): Description of the permission
        expanded_description (str): Expanded description of the permission
        model_name (str): Name of the LLM model to use
        client (Optional[GenerativeModel]): The Google Generative AI client
        chat_session (Optional[ChatSession]): Existing chat session to use
        
    Returns:
        Tuple[str, RiskRating]: Detailed evaluation text and structured risk rating
        
    Example:
        >>> text, rating = risk_eval_summary(
        ...     prompt="Evaluate risk for: {permission_name}",
        ...     name="View All Data",
        ...     api_name="ViewAllData",
        ...     description="Can view all data",
        ...     expanded_description="Can view all data in the organization"
        ... )
    
    Raises:
        ValueError: If neither client nor chat_session is provided
    """
    if client is None and chat_session is None:
        raise ValueError("Either client or chat_session must be provided")

    try:
        # Use existing chat session or create new one
        chat = chat_session or create_chat_session(client, model_name)
        
        # Generate detailed evaluation
        try:
            response = chat.send_message(
                      message=prompt.format(
                      permission_name = name
                    , permission_api_name = api_name
                    , permission_description = description
                    , permission_expanded_description = expanded_description
                )
            )
            verbose_eval = response.text
        except Exception as e:
            logger.error(f"Error generating evaluation: {str(e)}")
            raise
            
        # Generate structured output
        try:
            structured_output_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=RiskRating,
            )
            response = chat.send_message(
              message="Convert the final score.",
              config=structured_output_config,
            )
            structured_eval = response.parsed
            
            # Validate structured output
            if not isinstance(structured_eval, RiskRating):
                logger.warning(f"Invalid structured output type: {type(structured_eval)}")
                structured_eval = RiskRating.from_string(str(structured_eval))
                
        except Exception as e:
            logger.error(f"Error generating structured output: {str(e)}")
            # Attempt to extract rating from verbose evaluation
            structured_eval = _extract_fallback_rating(verbose_eval)
            
        return verbose_eval, structured_eval
        
    except Exception as e:
        logger.error(f"Error in eval_summary: {str(e)}")
        return f"Error evaluating permission: {str(e)}", RiskRating.GENERAL

def _extract_fallback_rating(eval_text: str) -> RiskRating:
    """
    Attempts to extract a risk rating from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse
        
    Returns:
        RiskRating: Extracted rating or GENERAL as default
    """
    try:
        # Look for rating keywords in the text
        text_lower = eval_text.lower()
        if "mission critical" in text_lower or "mission_critical" in text_lower:
            return RiskRating.MISSION_CRITICAL
        elif "restricted" in text_lower:
            return RiskRating.RESTRICTED
        elif "sensitive" in text_lower:
            return RiskRating.SENSITIVE
        elif "controlled" in text_lower:
            return RiskRating.CONTROLLED
        else:
            return RiskRating.GENERAL
    except Exception:
        return RiskRating.GENERAL 
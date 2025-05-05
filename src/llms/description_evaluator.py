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

class QualityRating(enum.Enum):
    """
    Enumeration of quality rating levels for permissions.
    """
    PERFECT_QUALITY = '5'
    HIGH_QUALITY = '4'
    MODERATE_QUALITY = '3'
    LOW_QUALITY = '2'
    NO_QUALITY = '1'
    UNKNOWN = '99'

    @classmethod
    def from_string(cls, value: str) -> 'QualityRating':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid quality rating value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN

def description_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None
) -> Tuple[str, QualityRating]:
    """
    Evaluates a permission using an LLM to determine its quality rating.
    
    Args:
        prompt (str): Template prompt for evaluation
        name (str): Permission name
        api_name (str): API name of the permission
        description (str): Description of the permission
        model_name (str): Name of the LLM model to use
        client (Optional[GenerativeModel]): The Google Generative AI client
        chat_session (Optional[ChatSession]): Existing chat session to use
        
    Returns:
        Tuple[str, QualityRating]: Detailed evaluation text and structured quality rating
        
    Example:
        >>> text, rating = description_eval_summary(
        ...     prompt="Evaluate description for: {permission_name}",
        ...     name="View All Data",
        ...     api_name="ViewAllData",
        ...     description="Can view all data"
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
            config_with_search = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.0,
            )

            response = chat.send_message(
                      message=prompt.format(
                      permission_name = name
                    , permission_api_name = api_name
                    , permission_description = description
                ),
                config=config_with_search,
            ).candidates[0]
            verbose_eval = response.text
        except Exception as e:
            logger.error(f"Error generating evaluation: {str(e)}")
            raise
            
        # Generate structured output for rating
        try:
            structured_output_rating_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=QualityRating,
            )
            response_rating = chat.send_message(
              message="Convert the final Match Rating to a QualityRating.",
              config=structured_output_rating_config,
            )
            structured_rating = response_rating.parsed

            # Validate structured output
            if not isinstance(structured_rating, QualityRating):
                logger.warning(f"Invalid structured output type: {type(structured_rating)}")
                structured_rating = QualityRating.from_string(str(structured_rating))
            
        
        except Exception as e:
            logger.error(f"Error generating structured output for rating: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_rating = _extract_fallback_rating(verbose_eval)
        
    except Exception as e:
        logger.error(f"Error in eval_summary: {str(e)}")
        return f"Error evaluating permission: {str(e)}", QualityRating.UNKNOWN

def _extract_fallback_rating(eval_text: str) -> QualityRating:
    """
    Attempts to extract a quality rating from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse
        
    Returns:
        RiskRating: Extracted rating or GENERAL as default
    """
    try:
        # Look for rating keywords in the text
        text_lower = eval_text.lower()
        if "perfect quality" in text_lower or "perfect_quality" in text_lower:
            return QualityRating.PERFECT_QUALITY
        elif "high quality" in text_lower or "high_quality" in text_lower:
            return QualityRating.HIGH_QUALITY
        elif "moderate quality" in text_lower or "moderate_quality" in text_lower:
            return QualityRating.MODERATE_QUALITY
        elif "low quality" in text_lower or "low_quality" in text_lower:
            return QualityRating.LOW_QUALITY
        elif "no quality" in text_lower or "no_quality" in text_lower:
            return QualityRating.NO_QUALITY
        else:
            return QualityRating.UNKNOWN
    except Exception:
        return QualityRating.UNKNOWN 

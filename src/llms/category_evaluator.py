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

class CategoryRating(enum.Enum):
    """
    Enumeration of category rating levels for permissions.
    """
    EXACT_MATCH = '5'
    HIGH_MATCH = '4'
    MODERATE_MATCH = '3'
    LOW_MATCH = '2'
    NO_MATCH = '1'
    UNKNOWN = '99'

    @classmethod
    def from_string(cls, value: str) -> 'CategoryRating':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid category rating value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN

class CategoryLabel(enum.Enum):
    """
    Enumeration of permission category names for permissions.
    """
    GENERAL_ADMIN = '1'
    SECURITY_ADMIN = '2'
    USER_MANAGEMENT_ADMIN = '3'
    DATA_ADMIN = '4'
    IMPORT_AND_EXPORT = '5'
    AGENTFORCE = '6'
    EINSTEIN = '7'
    REPORT_AND_DASHBOARD = '8'
    DEVELOPER = '9'
    USER_INTERFACE = '10'  
    OBJECT_ACCESS = '11'
    DATA_CLOUD = '12'
    CRM_ANALYTICS = '13'
    CHATTER_AND_COMMUNITIES = '14'
    SHIELD_AND_EVENT_MONITORING = '15'
    UNKNOWN = '99'
    
    @classmethod
    def from_string(cls, value: str) -> 'CategoryLabel':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid category label value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN

def category_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
    expanded_description: str,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None
) -> Tuple[str, CategoryRating, CategoryLabel]:
    """
    Evaluates a permission using an LLM to determine its category rating and label.
    
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
        Tuple[str, CategoryRating, CategoryLabel]: Detailed evaluation text and structured category rating and label
        
    Example:
        >>> text, rating, label = category_eval_summary(
        ...     prompt="Evaluate category for: {permission_name}",
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
            
        # Generate structured output for rating
        try:
            structured_output_rating_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=CategoryRating,
            )
            response_rating = chat.send_message(
              message="Convert the final Match Rating to a CategoryRating.",
              config=structured_output_rating_config,
            )
            structured_rating = response_rating.parsed

            # Validate structured output
            if not isinstance(structured_rating, CategoryRating):
                logger.warning(f"Invalid structured output type: {type(structured_rating)}")
                structured_rating = CategoryRating.from_string(str(structured_rating))
            
        
        except Exception as e:
            logger.error(f"Error generating structured output for rating: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_rating = _extract_fallback_rating(verbose_eval)

        # Generate structured output for label
        try:
            structured_output_label_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=CategoryLabel,
            )
            response_label = chat.send_message(
              message="Convert the final Permission Category to a CategoryLabel.",
              config=structured_output_label_config,
            )
            structured_label = response_label.parsed

            
            # Validate structured output
            if not isinstance(structured_label, CategoryLabel):
                logger.warning(f"Invalid structured output type: {type(structured_label)}")
                structured_label = CategoryLabel.from_string(str(structured_label))

        except Exception as e:
            logger.error(f"Error generating structured output for category label: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_label = _extract_fallback_label(verbose_eval)
            
        return verbose_eval, structured_rating, structured_label
        
    except Exception as e:
        logger.error(f"Error in eval_summary: {str(e)}")
        return f"Error evaluating permission: {str(e)}", CategoryRating.UNKNOWN, CategoryLabel.UNKNOWN

def _extract_fallback_rating(eval_text: str) -> CategoryRating:
    """
    Attempts to extract a category rating from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse
        
    Returns:
        RiskRating: Extracted rating or GENERAL as default
    """
    try:
        # Look for rating keywords in the text
        text_lower = eval_text.lower()
        if "exact match" in text_lower or "exact_match" in text_lower:
            return CategoryRating.EXACT_MATCH
        elif "high match" in text_lower or "high_match" in text_lower:
            return CategoryRating.HIGH_MATCH
        elif "moderate match" in text_lower or "moderate_match" in text_lower:
            return CategoryRating.MODERATE_MATCH
        elif "low match" in text_lower or "low_match" in text_lower:
            return CategoryRating.LOW_MATCH
        elif "no match" in text_lower or "no_match" in text_lower:
            return CategoryRating.NO_MATCH
        else:
            return CategoryRating.UNKNOWN
    except Exception:
        return CategoryRating.UNKNOWN 
    
def _extract_fallback_label(eval_text: str) -> CategoryLabel:
    """
    Attempts to extract a category label from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse

    Returns:
        CategoryLabel: Extracted label or UNKNOWN as default
    """
    try:
        # Look for label keywords in the text
        text_lower = eval_text.lower()
        
        # Core Platform Categories
        if "general admin" in text_lower or "general_admin" in text_lower:
            return CategoryLabel.GENERAL_ADMIN
        elif "security admin" in text_lower or "security_admin" in text_lower:
            return CategoryLabel.SECURITY_ADMIN
        elif "user management admin" in text_lower or "user_management_admin" in text_lower:
            return CategoryLabel.USER_MANAGEMENT_ADMIN
        elif "data admin" in text_lower or "data_admin" in text_lower:
            return CategoryLabel.DATA_ADMIN
        elif "import and export" in text_lower or "import_and_export" in text_lower:
            return CategoryLabel.IMPORT_AND_EXPORT
        elif "agentforce" in text_lower:
            return CategoryLabel.AGENTFORCE
        elif "einstein and ai" in text_lower or "einstein_and_ai" in text_lower:
            return CategoryLabel.EINSTEIN_AND_AI
        elif "report and dashboard" in text_lower or "report_and_dashboard" in text_lower:
            return CategoryLabel.REPORT_AND_DASHBOARD
        elif "developer" in text_lower:
            return CategoryLabel.DEVELOPER
        elif "user interface" in text_lower or "user_interface" in text_lower:
            return CategoryLabel.USER_INTERFACE
        elif "object access" in text_lower or "object_access" in text_lower:
            return CategoryLabel.OBJECT_ACCESS

        # Core Platform Add-Ons
        elif "data cloud" in text_lower or "data_cloud" in text_lower:
            return CategoryLabel.DATA_CLOUD
        elif "crm analytics" in text_lower or "crm_analytics" in text_lower:
            return CategoryLabel.CRM_ANALYTICS
        elif "chatter and communities" in text_lower or "chatter_and_communities" in text_lower:
            return CategoryLabel.CHATTER_AND_COMMUNITIES
        elif "shield and event monitoring" in text_lower or "shield_and_event_monitoring" in text_lower:
            return CategoryLabel.SHIELD_AND_EVENT_MONITORING

        # Other
        elif "other" in text_lower:
            return CategoryLabel.UNKNOWN
        else:
            return CategoryLabel.UNKNOWN
    except Exception:
        return CategoryLabel.UNKNOWN

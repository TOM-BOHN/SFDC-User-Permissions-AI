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
    UNKNOWN = '0'

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
    USER_MANAGEMENT = '3'
    DATA_ADMIN = '4'
    IMPORT_AND_EXPORT = '5'
    AGENTFORCE_AND_EINSTEIN = '6'
    REPORT_AND_DASHBOARD = '7'
    DEVELOPER = '8'
    USER_INTERFACE = '9'
    OBJECT = '10'
    SHIELD_AND_EVENT_MONITORING = '11'
    CHATTER_AND_COMMUNITIES = '12'
    DATA_CLOUD = '13'
    CRM_ANALYTICS = '14'
    SLACK_AND_QUIP = '15'
    COMMERCE = '16'
    FIELD_SERVICE = '17'
    MARKETING_CLOUD_AND_PARDOT = '18'
    CPQ = '19'
    INDUSTRY_CLOUD = '20'
    UNKNOWN = '0'
    
    @classmethod
    def from_string(cls, value: str) -> 'CategoryLabel':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid category label value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN


def risk_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
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
            response = chat.send_message(
                      message=prompt.format(
                      permission_name = name
                    , permission_api_name = api_name
                    , permission_description = description
                )
            )
            verbose_eval = response.text
        except Exception as e:
            logger.error(f"Error generating evaluation: {str(e)}")
            raise
            
        # Generate structured output
        try:
            structured_output_rating_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=CategoryRating,
            )
            structured_output_label_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=CategoryLabel,
            )
            response_rating = chat.send_message(
              message="Convert the final category rating.",
              config=structured_output_rating_config,
            )
            response_label = chat.send_message(
              message="Convert the final category label.",
              config=structured_output_label_config,
            )
            
            # Validate structured output
            if not isinstance(response_rating, CategoryRating):
                logger.warning(f"Invalid structured output type: {type(response_rating)}")
                response_rating = CategoryRating.from_string(str(response_rating))
            if not isinstance(response_label, CategoryLabel):
                logger.warning(f"Invalid structured output type: {type(response_label)}")
                response_label = CategoryLabel.from_string(str(response_label))
        except Exception as e:
            logger.error(f"Error generating structured output: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_rating = _extract_fallback_rating(verbose_eval)
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
        if "exact match" in text_lower or "exact-match" in text_lower:
            return CategoryRating.EXACT_MATCH
        elif "high match" in text_lower or "high-match" in text_lower:
            return CategoryRating.HIGH_MATCH
        elif "moderate match" in text_lower or "moderate-match" in text_lower:
            return CategoryRating.MODERATE_MATCH
        elif "low match" in text_lower or "low-match" in text_lower:
            return CategoryRating.LOW_MATCH
        elif "no match" in text_lower or "no-match" in text_lower:
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
        if "general admin" in text_lower or "general-admin" in text_lower:
            return CategoryLabel.GENERAL_ADMIN
        elif "security admin" in text_lower or "security-admin" in text_lower:
            return CategoryLabel.SECURITY_ADMIN
        elif "user management" in text_lower or "user-management" in text_lower:
            return CategoryLabel.USER_MANAGEMENT
        elif "data admin" in text_lower or "data-admin" in text_lower:
            return CategoryLabel.DATA_ADMIN
        elif "import and export" in text_lower or "import-and-export" in text_lower:
            return CategoryLabel.IMPORT_AND_EXPORT
        elif "agentforce and einstein" in text_lower or "agentforce-and-einstein" in text_lower:
            return CategoryLabel.AGENTFORCE_AND_EINSTEIN
        elif "report and dashboard" in text_lower or "report-and-dashboard" in text_lower:
            return CategoryLabel.REPORT_AND_DASHBOARD
        elif "developer" in text_lower or "developer" in text_lower:
            return CategoryLabel.DEVELOPER
        elif "user interface" in text_lower or "user-interface" in text_lower:
            return CategoryLabel.USER_INTERFACE 
        elif "object" in text_lower or "object" in text_lower:
            return CategoryLabel.OBJECT
        elif "shield and event monitoring" in text_lower or "shield-and-event-monitoring" in text_lower:
            return CategoryLabel.SHIELD_AND_EVENT_MONITORING
        elif "chatter and communities" in text_lower or "chatter-and-communities" in text_lower:
            return CategoryLabel.CHATTER_AND_COMMUNITIES
        elif "data cloud" in text_lower or "data-cloud" in text_lower:
            return CategoryLabel.DATA_CLOUD
        elif "crm analytics" in text_lower or "crm-analytics" in text_lower:
            return CategoryLabel.CRM_ANALYTICS
        elif "slack and quip" in text_lower or "slack-and-quip" in text_lower:
            return CategoryLabel.SLACK_AND_QUIP
        elif "commerce" in text_lower or "commerce" in text_lower:
            return CategoryLabel.COMMERCE
        elif "field service" in text_lower or "field-service" in text_lower:
            return CategoryLabel.FIELD_SERVICE
        elif "marketing cloud and pardot" in text_lower or "marketing-cloud-and-pardot" in text_lower:
            return CategoryLabel.MARKETING_CLOUD_AND_PARDOT
        elif "cpq" in text_lower or "cpq" in text_lower:
            return CategoryLabel.CPQ
        elif "industry cloud" in text_lower or "industry-cloud" in text_lower:
            return CategoryLabel.INDUSTRY_CLOUD
        else:
            return CategoryLabel.UNKNOWN
    except Exception:
        return CategoryLabel.UNKNOWN

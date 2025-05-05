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

class CloudRating(enum.Enum):
    """
    Enumeration of cloud rating levels for permissions.
    """
    EXACT_MATCH = '5'
    HIGH_MATCH = '4'
    MODERATE_MATCH = '3'
    LOW_MATCH = '2'
    NO_MATCH = '1'
    UNKNOWN = '99'

    @classmethod
    def from_string(cls, value: str) -> 'CloudRating':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid cloud rating value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN

class CloudLabel(enum.Enum):
    """
    Enumeration of permission cloud names for permissions.
    """
    SALES_CLOUD = '1'
    SERVICE_CLOUD = '2'
    MARKETING_CLOUD_AND_PARDOT = '3'
    COMMERCE_CLOUD = '4'
    SLACK_AND_QUIP = '5'
    CPQ = '6'
    FIELD_SERVICE = '7'
    FINANCIAL_SERVICES_CLOUD = '8'
    HEALTHCARE_AND_LIFE_SCIENCES_CLOUD = '9'
    CONSUMER_GOODS_CLOUD = '10'
    COMMUNICATIONS_CLOUD = '11'
    MANUFACTURING_CLOUD = '12'
    NONPROFIT_CLOUD = '13'
    GENERAL_INDUSTRIES_CLOUD = '14'
    UNKNOWN = '99'
    
    @classmethod
    def from_string(cls, value: str) -> 'CloudLabel':
        """Convert string to enum value, with error handling."""
        try:
            return cls(value)
        except ValueError:
            logger.warning(f"Invalid cloud label value: {value}. Defaulting to UNKNOWN.")
            return cls.UNKNOWN

def cloud_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
    expanded_description: str,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None
) -> Tuple[str, CloudRating, CloudLabel]:
    """
    Evaluates a permission using an LLM to determine its cloud rating and label.
    
    Args:
        prompt (str): Template prompt for evaluation
        name (str): Permission name
        api_name (str): API name of the permission
        description (str): Description of the permission
        model_name (str): Name of the LLM model to use
        client (Optional[GenerativeModel]): The Google Generative AI client
        chat_session (Optional[ChatSession]): Existing chat session to use
        
    Returns:
        Tuple[str, CloudRating, CloudLabel]: Detailed evaluation text and structured cloud rating and label
        
    Example:
        >>> text, rating, label = cloud_eval_summary(
        ...     prompt="Evaluate cloud for: {permission_name}",
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
                response_schema=CloudRating,
            )
            response_rating = chat.send_message(
              message="Convert the final Match Rating to a CloudRating.",
              config=structured_output_rating_config,
            )
            structured_rating = response_rating.parsed

            # Validate structured output
            if not isinstance(structured_rating, CloudRating):
                logger.warning(f"Invalid structured output type: {type(structured_rating)}")
                structured_rating = CloudRating.from_string(str(structured_rating))
            
        
        except Exception as e:
            logger.error(f"Error generating structured output for rating: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_rating = _extract_fallback_rating(verbose_eval)

        # Generate structured output for label
        try:
            structured_output_label_config = types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=CloudLabel,
            )
            response_label = chat.send_message(
              message="Convert the final Permission Cloud to a CloudLabel.",
              config=structured_output_label_config,
            )
            structured_label = response_label.parsed

            
            # Validate structured output    
            if not isinstance(structured_label, CloudLabel):
                logger.warning(f"Invalid structured output type: {type(structured_label)}")
                structured_label = CloudLabel.from_string(str(structured_label))

        except Exception as e:
            logger.error(f"Error generating structured output for cloud label: {str(e)}") 
            # Attempt to extract rating from verbose evaluation
            structured_label = _extract_fallback_label(verbose_eval)
            
        return verbose_eval, structured_rating, structured_label
        
    except Exception as e:
        logger.error(f"Error in eval_summary: {str(e)}")
        return f"Error evaluating permission: {str(e)}", CloudRating.UNKNOWN, CloudLabel.UNKNOWN

def _extract_fallback_rating(eval_text: str) -> CloudRating:
    """
    Attempts to extract a cloud rating from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse
        
    Returns:
        RiskRating: Extracted rating or GENERAL as default
    """
    try:
        # Look for rating keywords in the text
        text_lower = eval_text.lower()
        if "exact match" in text_lower or "exact_match" in text_lower:
            return CloudRating.EXACT_MATCH
        elif "high match" in text_lower or "high_match" in text_lower:
            return CloudRating.HIGH_MATCH
        elif "moderate match" in text_lower or "moderate_match" in text_lower:
            return CloudRating.MODERATE_MATCH
        elif "low match" in text_lower or "low_match" in text_lower:
            return CloudRating.LOW_MATCH
        elif "no match" in text_lower or "no_match" in text_lower:
            return CloudRating.NO_MATCH
        else:
            return CloudRating.UNKNOWN
    except Exception:
        return CloudRating.UNKNOWN 
    
def _extract_fallback_label(eval_text: str) -> CloudLabel:
    """
    Attempts to extract a cloud label from evaluation text as fallback.
    
    Args:
        eval_text (str): The evaluation text to parse

    Returns:
        CloudLabel: Extracted label or UNKNOWN as default
    """
    try:
        # Look for label keywords in the text
        text_lower = eval_text.lower()

        # Cloud
        if "sales cloud" in text_lower or "sales_cloud" in text_lower:
            return CloudLabel.SALES_CLOUD
        elif "service cloud" in text_lower or "service_cloud" in text_lower:
            return CloudLabel.SERVICE_CLOUD
        elif "marketing cloud and pardot" in text_lower or "marketing_cloud_and_pardot" in text_lower:
            return CloudLabel.MARKETING_CLOUD_AND_PARDOT
        elif "commerce cloud" in text_lower or "commerce_cloud" in text_lower:
            return CloudLabel.COMMERCE_CLOUD
        elif "slack and quip" in text_lower or "slack_and_quip" in text_lower:
            return CloudLabel.SLACK_AND_QUIP

        # Cloud Add-Ons
        elif "cpq" in text_lower:
            return CloudLabel.CPQ
        elif "field service" in text_lower or "field_service" in text_lower:
            return CloudLabel.FIELD_SERVICE

        # Industries
        elif "financial services cloud" in text_lower or "financial_services_cloud" in text_lower:
            return CloudLabel.FINANCIAL_SERVICES_CLOUD
        elif "healthcare & life sciences cloud" in text_lower or "healthcare_and_life_sciences_cloud" in text_lower:
            return CloudLabel.HEALTHCARE_AND_LIFE_SCIENCES_CLOUD
        elif "consumer goods cloud" in text_lower or "consumer_goods_cloud" in text_lower:
            return CloudLabel.CONSUMER_GOODS_CLOUD
        elif "communications cloud" in text_lower or "communications_cloud" in text_lower:
            return CloudLabel.COMMUNICATIONS_CLOUD
        elif "manufacturing cloud" in text_lower or "manufacturing_cloud" in text_lower:
            return CloudLabel.MANUFACTURING_CLOUD
        elif "nonprofit cloud" in text_lower or "nonprofit_cloud" in text_lower:
            return CloudLabel.NONPROFIT_CLOUD
        elif "general industries cloud" in text_lower or "general_industries_cloud" in text_lower:
            return CloudLabel.GENERAL_INDUSTRIES_CLOUD

        # Other
        elif "other" in text_lower:
            return CloudLabel.UNKNOWN
        else:
            return CloudLabel.UNKNOWN
    except Exception:
        return CloudLabel.UNKNOWN

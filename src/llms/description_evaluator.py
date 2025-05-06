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

import io
from pprint import pprint

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
        

def write_markdown_output(response, debug: bool = False):
    """
    Writes a markdown buffer to a file.
    """
    # Extract the chunks and supports and the verbose evaluation
    chunks = response.grounding_metadata.grounding_chunks
    supports = response.grounding_metadata.grounding_supports
    verbose_eval = response.content.parts[0].text

    if debug:
        print('\n################\n')
        # Print the verbose evaluation
        print(f"Verbose Evaluation: {verbose_eval}")
        # Print the chunks
        for chunk in chunks:
            print(f'{chunk.web.title}: {chunk.web.uri}')
        # Print the Support
        for support in supports:
            pprint(support.to_json_dict())
        print('\n################\n')

    # Start the buffer
    markdown_buffer = io.StringIO()
    # Add a Break
    markdown_buffer.write('\n----\n')
    # Print the content
    markdown_buffer.write(response.content.parts[0].text)
    # Add a Break
    markdown_buffer.write('\n----\n')
    # Print the text with footnote markers.
    markdown_buffer.write("Supported text:\n\n")
    for support in supports:
        markdown_buffer.write(" * ")
        markdown_buffer.write(
            response.content.parts[0].text[support.segment.start_index : support.segment.end_index]
        )

        for i in support.grounding_chunk_indices:
            chunk = chunks[i].web
            markdown_buffer.write(f"<sup>[{i+1}]</sup>")

        markdown_buffer.write("\n\n")
    # Add a Break
    markdown_buffer.write('\n----\n')
    # And print the footnotes.
    markdown_buffer.write("Citations:\n\n")
    for i, chunk in enumerate(chunks, start=1):
        markdown_buffer.write(f"{i}. [{chunk.web.title}]({chunk.web.uri})\n")
    # Add a Break
    markdown_buffer.write('\n----\n')

    # Display all the markdown
    return(markdown_buffer.getvalue())

def description_eval_summary(
    prompt: str,
    name: str,
    api_name: str,
    description: str,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None,
    debug: bool = False
) -> Tuple[str, QualityRating, str]:
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
        Tuple[str, QualityRating, str]: Detailed evaluation text, structured quality rating, and full fidelity evaluation
        
    Example:
        >>> text, rating, full_fidelity_eval = description_eval_summary(
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

            def query_with_grounding(chat_session, prompt, config_with_search):
                response = chat.send_message(
                        message=prompt.format(
                        permission_name = name
                        , permission_api_name = api_name
                        , permission_description = description
                    ),
                    config=config_with_search,
                )
                
                return response.candidates[0]
            
            response = query_with_grounding(chat_session = chat, prompt = prompt, config_with_search = config_with_search)

            # Retry the query if the grounding metadata is incomplete.
            # This ensures that both 'grounding_supports' and 'grounding_chunks' are present before proceeding.
            while not response.grounding_metadata.grounding_supports or not response.grounding_metadata.grounding_chunks:
                # If incomplete grounding data was returned, retry.
                response = query_with_grounding(chat_session = chat, prompt = prompt, config_with_search = config_with_search)

            if debug:
                print(f"Response: {response}")

            # Extract the verbose evaluation
            verbose_eval = response.content.parts[0].text

            if debug:
                print('\n################\n')
                # Print the verbose evaluation
                print(f"Verbose Evaluation: {verbose_eval}")
                print('\n################\n')

            # Write the markdown buffer to a file
            full_fidelity_eval = write_markdown_output(response=response, debug=debug)

            if debug:
                print(f"Full Fidelity Evaluation:")
                display(Markdown(full_fidelity_eval))
                
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

            if debug:
                print(f"Response Rating: {response_rating}")

            structured_rating = response_rating.parsed

            if debug:
                print(f"Structured Rating: {structured_rating}")

            # Validate structured output
            if not isinstance(structured_rating, QualityRating):
                logger.warning(f"Invalid structured output type: {type(structured_rating)}")
                structured_rating = QualityRating.from_string(str(structured_rating))
            
        except Exception as e:
            logger.error(f"Error generating structured output for rating: {str(e)}") 
            if debug:
                print(f"Error generating structured output for rating: {str(e)}")
            # Attempt to extract rating from verbose evaluation
            structured_rating = _extract_fallback_rating(verbose_eval)
            if debug:
                print(f"Structured Rating: {structured_rating}")
        
        return verbose_eval, structured_rating, full_fidelity_eval
    
    except Exception as e:
        logger.error(f"Error in eval_summary: {str(e)}")
        if debug:
            print(f"Error in eval_summary: {str(e)}")
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

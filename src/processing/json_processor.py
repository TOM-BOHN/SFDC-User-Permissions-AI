"""
Functions for processing and extracting data from JSON fields in DataFrames.
"""

import json
import pandas as pd
import logging
from typing import Optional, List, Union

# Set up logging
logger = logging.getLogger(__name__)

def clean_json_string(json_string: str) -> str:
    """
    Cleans a JSON string by removing markdown code blocks and newlines.
    
    Args:
        json_string (str): The JSON string to clean
        
    Returns:
        str: Cleaned JSON string
    """
    replacements = [
        ("```json\n", ""),
        ("\n```", ""),
        ("```", ""),
        ("\n", "")
    ]
    
    for old, new in replacements:
        json_string = json_string.replace(old, new)
    return json_string

def clean_expanded_description_column(df):
    if 'Expanded Description' in df.columns:
        df['Expanded Description'] = df['Expanded Description'].str.replace(r'\s*\[\d+(?:\s*,\s*\d+)*\]', '', regex=True)

    return df

def extract_json_fields(
    df: pd.DataFrame,
    json_column: str = 'Evaluation',
    fields: Optional[List[str]] = None,
    debug: bool = True
) -> pd.DataFrame:
    """
    Extracts fields from a JSON column in a DataFrame and adds them as new columns.

    Args:
        df (pd.DataFrame): The input DataFrame containing the JSON column
        json_column (str): The name of the column containing the JSON data
        fields (List[str], optional): List of fields to extract. If None, uses default fields
        debug (bool): Whether to print debug information

    Returns:
        pd.DataFrame: DataFrame with extracted JSON fields as new columns

    Example:
        >>> df = pd.DataFrame({'Evaluation': ['{"risk_tier": "High", "score": 0.8}']})
        >>> result = extract_json_fields(df, json_column='Evaluation')
    """
    # Make a copy to avoid modifying the original DataFrame
    results_df = df.copy()
    
    # Default fields to extract if none provided
    default_fields = {
        'risk_rating_tier': 'Risk Rating Tier',
        'risk_rating_score': 'Risk Rating Score',
        'weighted_score': 'Weighted Score',
        'scores': 'Scores',
        'rationale': 'Rationale',
        'confidence': 'Confidence'
    }
    
    # Use provided fields or defaults
    fields_map = fields if fields else default_fields
    
    # Initialize new columns
    for column in fields_map.values():
        if column not in results_df.columns:
            results_df[column] = None
    
    # Clean and process JSON
    results_df[json_column] = results_df[json_column].apply(clean_json_string)
    
    # Process each row
    for index, row in results_df.iterrows():
        try:
            # Skip empty or null values
            if pd.isna(row[json_column]) or not row[json_column].strip():
                logger.warning(f"Empty or null JSON at index {index}")
                continue
                
            eval_data = json.loads(row[json_column])
            
            # Extract each field
            for json_key, df_column in fields_map.items():
                value = eval_data.get(json_key, '')
                # Convert lists/dicts to strings for storage
                if isinstance(value, (list, dict)):
                    value = str(value)
                results_df.loc[index, df_column] = value

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON at index {index}: {str(e)}")
            logger.debug(f"Problematic JSON: {row[json_column]}")
        except Exception as e:
            logger.error(f"Unexpected error processing row {index}: {str(e)}")

    results_df = clean_expanded_description_column(results_df)
    
    if debug:
        logger.info("Sample output of results:")
        print("\nFirst 5 rows of processed data:")
        display(results_df.head())
        print("\nColumns added:", list(fields_map.values()))
    
    return results_df 






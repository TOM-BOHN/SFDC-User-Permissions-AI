"""
Utility functions for data handling and I/O operations.
"""

import os
import pandas as pd
from pathlib import Path
import yaml
from typing import Union, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str = "config/environment.yml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path (str): Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.warning(f"Config file not found at {config_path}. Using default paths.")
        return {
            "paths": {
                "output": "data/output",
                "processed_data": "data/processed",
                "raw_data": "data/raw"
            }
        }

def save_data(
    data: Union[pd.DataFrame, dict, list],
    filename: str,
    data_type: str = "output",
    format: str = "csv",
    subdirectory: Optional[str] = None,
    index: bool = False
) -> str:
    """
    Save data to the appropriate directory based on data type.
    
    Args:
        data: Data to save (DataFrame, dict, or list)
        filename: Name of the file (without extension)
        data_type: Type of data ('raw', 'processed', or 'output')
        format: File format ('csv', 'json', 'pickle')
        subdirectory: Optional subdirectory within the data type directory
        index: Whether to save DataFrame index
    
    Returns:
        str: Path to the saved file
    
    Example:
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        >>> save_data(df, 'results', data_type='output', format='csv')
        'data/output/results.csv'
    """
    # Load configuration
    config = load_config()
    base_path = config["paths"].get(f"{data_type}_data", f"data/{data_type}")
    
    # Create full path
    if subdirectory:
        save_path = Path(base_path) / subdirectory
    else:
        save_path = Path(base_path)
    
    # Create directory if it doesn't exist
    save_path.mkdir(parents=True, exist_ok=True)
    
    # Add extension if not present
    if not filename.endswith(f".{format}"):
        filename = f"{filename}.{format}"
    
    full_path = save_path / filename
    
    try:
        if isinstance(data, pd.DataFrame):
            if format == 'csv':
                data.to_csv(full_path, index=index)
            elif format == 'json':
                data.to_json(full_path, orient='records')
            elif format == 'pickle':
                data.to_pickle(full_path)
            else:
                raise ValueError(f"Unsupported format for DataFrame: {format}")
        
        elif isinstance(data, (dict, list)):
            if format == 'json':
                import json
                with open(full_path, 'w') as f:
                    json.dump(data, f, indent=2)
            elif format == 'pickle':
                import pickle
                with open(full_path, 'wb') as f:
                    pickle.dump(data, f)
            else:
                raise ValueError(f"Unsupported format for dict/list: {format}")
        
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
        
        logger.info(f"Successfully saved data to {full_path}")
        return str(full_path)
    
    except Exception as e:
        logger.error(f"Error saving data to {full_path}: {str(e)}")
        raise 
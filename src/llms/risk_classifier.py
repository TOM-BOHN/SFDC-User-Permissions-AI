"""
Functions for classifying and analyzing risk in permissions data.
"""

import pandas as pd
import time
import logging
from typing import Optional, Tuple, Callable
from datetime import datetime

from .evaluator import eval_summary, RiskRating, create_chat_session

# Set up logging
logger = logging.getLogger(__name__)

def classify_risk_rating(
    input_df: pd.DataFrame,
    prompt: str,
    chat_session  = None,
    total_records: Optional[int] = None,
    checkin_interval: int = 60,
    debug: bool = True
) -> pd.DataFrame:
    """
    Classifies risk ratings for permissions based on their descriptions.

    Args:
        input_df (pd.DataFrame): Input DataFrame containing permission details
        prompt (str): Prompt template for evaluation
        chat_session (Optional[Chat]): Chat session to reuse for evaluations
        total_records (int, optional): Number of records to process. If None, processes all records
        checkin_interval (int): Seconds between progress updates (default: 60)
        debug (bool): Whether to print debug information (default: True)

    Returns:
        pd.DataFrame: Results DataFrame with risk classifications

    Example:
        >>> df = pd.DataFrame({
        ...     'Permission Name': ['View All Data'],
        ...     'API Name': ['ViewAllData'],
        ...     'Description': ['Can view all data']
        ... })
        >>> results = classify_risk_rating(df, prompt)
    """
    # Input validation
    required_columns = ['Permission Name', 'API Name', 'Description']
    missing_columns = [col for col in required_columns if col not in input_df.columns]
    if missing_columns:
        raise ValueError(f"Input DataFrame missing required columns: {missing_columns}")

    # Set total records
    total_records = total_records or len(input_df)
    if total_records > len(input_df):
        logger.warning(f"Requested {total_records} records but only {len(input_df)} available")
        total_records = len(input_df)

    # Initialize results DataFrame
    results_df = pd.DataFrame(columns=[
        'Permission Name',
        'API Name',
        'Description',
        'Risk Rating',
        'Evaluation',
        'Processing Time'
    ])

    # Start tracking time
    start_time = time.time()
    last_checkin = start_time
    
    logger.info(f"Starting job to process {total_records} records at {datetime.now()}")
    if debug:
        print(f"Starting job to process {total_records} records.")
        print('####################\n')

    # Process records
    for i in range(total_records):
        record_start_time = time.time()
        
        try:
            # Progress update
            current_time = time.time()
            if current_time - last_checkin >= checkin_interval:
                elapsed = current_time - start_time
                rate = (i + 1) / elapsed
                remaining = (total_records - (i + 1)) / rate if rate > 0 else 0
                logger.info(
                    f"Progress: {i+1}/{total_records} records "
                    f"({(i+1)/total_records*100:.1f}%). "
                    f"Est. time remaining: {remaining/60:.1f} minutes"
                )
                last_checkin = current_time

            # Debug output
            if debug:
                print(f'Analyzing Permission {i+1} of {total_records}...')
                print('Name:       ', input_df['Permission Name'].iloc[i])
                print('API Name:   ', input_df['API Name'].iloc[i])
                print('Description:', input_df['Description'].iloc[i])
                print('--------------------')

            # Evaluate permission
            try:
                text_eval, struct_eval = eval_summary(
                    prompt=prompt,
                    name=input_df['Permission Name'].iloc[i],
                    api_name=input_df['API Name'].iloc[i],
                    description=input_df['Description'].iloc[i],
                    chat_session=chat_session  # Reuse the same session
                )
            except Exception as e:
                logger.error(f"Error evaluating permission at index {i}: {str(e)}")
                text_eval = f"Error: {str(e)}"
                struct_eval = "ERROR"

            # Calculate processing time for this record
            record_time = time.time() - record_start_time

            # Append results
            results_df.loc[len(results_df)] = [
                input_df['Permission Name'].iloc[i],
                input_df['API Name'].iloc[i],
                input_df['Description'].iloc[i],
                struct_eval,
                text_eval,
                record_time
            ]

            if debug:
                print('Risk Rating:', struct_eval)
                print('####################\n')

        except Exception as e:
            logger.error(f"Error processing record {i}: {str(e)}")
            continue

    # Final statistics
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / total_records
    
    logger.info(
        f"Processing completed at {datetime.now()}. "
        f"Total time: {total_time:.2f}s. "
        f"Average per record: {avg_time:.2f}s"
    )

    if debug:
        print('\n####################')
        print(f"Total time taken: {total_time:.2f} seconds to process {total_records} records.")
        print(f"Average time per record: {avg_time:.2f} seconds")
        print('\nSample Output of Results:')
        print(results_df.head())
        print()

    return results_df 
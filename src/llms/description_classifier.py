"""
Functions for classifying and analyzing risk in permissions data.
"""

import pandas as pd
import time
import logging
import json
import os
from pathlib import Path
from typing import Optional, Tuple, Dict
from datetime import datetime

from .description_evaluator import description_eval_summary, QualityRating
from .chat_session import create_chat_session

# Set up logging
logger = logging.getLogger(__name__)

def classify_description(
    input_df: pd.DataFrame,
    prompt: str,
    checkpoint_dir: str = "data/checkpoints",
    job_id: Optional[str] = None,
    resume_from_checkpoint: bool = False,
    model_name: str = 'gemini-2.0-flash',
    client = None,
    chat_session = None,
    total_records: Optional[int] = None,
    checkin_interval: int = 120,
    checkpoint_interval: int = 10,
    debug: bool = True,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Classifies descriptions for permissions based on their descriptions.
    Includes checkpoint/recovery logic for long-running jobs.
    Args:
        input_df (pd.DataFrame): Input DataFrame containing permission details
        prompt (str): Prompt template for evaluation
        checkpoint_dir (str): Directory to store checkpoint files
        job_id (Optional[str]): Unique identifier for this job run. If None, uses timestamp
        resume_from_checkpoint (bool): Whether to attempt to resume from last checkpoint
        chat_session: Chat session to reuse for evaluations
        total_records (int, optional): Number of records to process. If None, processes all records
        checkin_interval (int): Seconds between progress updates (default: 60)
        checkpoint_interval (int): Number of records between checkpoints (default: 10)
        debug (bool): Whether to print debug information (default: True)

    Returns:
        pd.DataFrame: Results DataFrame with category classifications

    Example:
        >>> df = pd.DataFrame({
        ...     'Permission Name': ['View All Data'],
        ...     'API Name': ['ViewAllData'],
        ...     'Description': ['Can view all data'],]
        ... })
        >>> results = classify_description(
        ...     df, 
        ...     prompt,
        ...     checkpoint_dir='data/checkpoints',
        ...     resume_from_checkpoint=True
        ... )
    Raises:
        ValueError: If neither client nor chat_session is provided
    """
    if client is None and chat_session is None:
        raise ValueError("Either client or chat_session must be provided")
    
    # Input validation
    required_columns = ['Permission Name', 'API Name', 'Description']
    missing_columns = [col for col in required_columns if col not in input_df.columns]
    if missing_columns:
        raise ValueError(f"Input DataFrame missing required columns: {missing_columns}")

    # Setup checkpoint directory
    checkpoint_dir = Path(checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate or load job ID and metadata
    if job_id is None:
        job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    checkpoint_file = checkpoint_dir / f"description_classification_{job_id}.json"
    results_file = checkpoint_dir / f"description_classification_{job_id}.csv"
    
    # Initialize or load checkpoint data
    start_index = 0
    results_df = pd.DataFrame(columns=[
        'Permission Name',
        'API Name',
        'Description',
        'Quality Rating',
        'Evaluation',
        'Full Fidelity Evaluation'
        'Processing Time'
    ])

    if resume_from_checkpoint and checkpoint_file.exists() and results_file.exists():
        try:
            # Load checkpoint metadata
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
                start_index = checkpoint_data['last_processed_index'] + 1
                
            # Load previous results
            results_df = pd.read_csv(results_file)
            logger.info(f"Resuming from checkpoint at index {start_index}")
            if debug:
                print(f"Resuming from checkpoint at index {start_index}")
        except Exception as e:
            logger.error(f"Error loading checkpoint: {str(e)}. Starting from beginning.")
            start_index = 0
    
    # Set total records
    total_records = total_records or len(input_df)
    if total_records > len(input_df):
        logger.warning(f"Requested {total_records} records but only {len(input_df)} available")
        total_records = len(input_df)

    # Start tracking time
    start_time = time.time()
    last_checkin = start_time
    last_checkpoint = start_time
    
    logger.info(f"Starting job {job_id} to process {total_records} records at {datetime.now()}")

    #Share the start of the job
    if debug:
        print(f"Starting job {job_id} to process {total_records} records.")
        print('####################\n')

    # Process records
    for i in range(start_index, total_records):
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
                if debug:
                    print(f"Progress: ({(i+1)/total_records*100:.1f}%) {i+1}/{total_records} records ---> Est. time remaining: {remaining/60:.1f} minutes.")

                last_checkin = current_time

            # Debug output
            if debug and verbose:
                print(f'Analyzing Permission {i+1} of {total_records}...')
                print('Name:       ', input_df['Permission Name'].iloc[i])
                print('API Name:   ', input_df['API Name'].iloc[i])
                print('Description:', input_df['Description'].iloc[i])
                print('--------------------')

            # Evaluate permission
            try:
                text_eval, rating, full_fidelity_eval = description_eval_summary(
                    prompt=prompt,
                    name=input_df['Permission Name'].iloc[i],
                    api_name=input_df['API Name'].iloc[i],
                    description=input_df['Description'].iloc[i],
                    model_name=model_name,
                    client=client,
                    chat_session=chat_session,
                    debug=debug
                )
            except Exception as e:
                logger.error(f"Error evaluating permission at index {i}: {str(e)}")
                text_eval = f"Error: {str(e)}"
                rating = "ERROR"

            # Calculate processing time for this record
            record_time = round(time.time() - record_start_time, 2)

            # Append results
            new_row = pd.DataFrame([{
                'Permission Name': input_df['Permission Name'].iloc[i],
                'API Name': input_df['API Name'].iloc[i],
                'Description': input_df['Description'].iloc[i],
                'Quality Rating': rating,
                'Evaluation': text_eval,
                'Full Fidelity Evaluation': full_fidelity_eval,
                'Processing Time': record_time
            }])
            results_df = pd.concat([results_df, new_row], ignore_index=True)

            if debug and verbose:
                print('Quality Rating:', rating)
                print('####################\n')

            # Checkpoint if needed
            if (i + 1) % checkpoint_interval == 0:
                _save_checkpoint(
                    checkpoint_file=checkpoint_file,
                    results_file=results_file,
                    results_df=results_df,
                    last_index=i,
                    job_id=job_id
                )
                last_checkpoint = current_time

        except Exception as e:
            logger.error(f"Error processing record {i}: {str(e)}")
            # Save checkpoint on error
            _save_checkpoint(
                checkpoint_file=checkpoint_file,
                results_file=results_file,
                results_df=results_df,
                last_index=i-1,
                job_id=job_id
            )
            continue
    
    # Final statistics
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / (total_records - start_index)
    
    logger.info(
        f"Processing completed at {datetime.now()}. "
        f"Total time: {total_time:.2f}s. "
        f"Average per record: {avg_time:.2f}s"
    )

    if debug:
        print('\n####################')
        print(f"Total time taken: {total_time:.2f} seconds to process {total_records - start_index} records.")
        print(f"Average time per record: {avg_time:.2f} seconds")
        if verbose:
            print('\nSample Output of Results:')
            print(results_df.head())
            print()
    
    # Save final results
    _save_checkpoint(
        checkpoint_file=checkpoint_file,
        results_file=results_file,
        results_df=results_df,
        last_index=total_records-1,
        job_id=job_id,
        is_final=True
    )

    return results_df

def _save_checkpoint(
    checkpoint_file: Path,
    results_file: Path,
    results_df: pd.DataFrame,
    last_index: int,
    job_id: str,
    is_final: bool = False
) -> None:
    """
    Saves a checkpoint of the current processing state.
    
    Args:
        checkpoint_file (Path): Path to save checkpoint metadata
        results_file (Path): Path to save results DataFrame
        results_df (pd.DataFrame): Current results
        last_index (int): Index of last processed record
        job_id (str): Unique job identifier
        is_final (bool): Whether this is the final checkpoint
    """
    try:
        # Save checkpoint metadata
        checkpoint_data = {
            'job_id': job_id,
            'last_processed_index': last_index,
            'timestamp': datetime.now().isoformat(),
            'is_final': is_final
        }
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f)
            
        # Save results DataFrame
        results_df.to_csv(results_file, index=False)
        
        logger.debug(f"Checkpoint saved at index {last_index}")
    except Exception as e:
        logger.error(f"Error saving checkpoint: {str(e)}") 
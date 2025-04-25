import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List
import os

def extract_permission_data(html_content: str) -> pd.DataFrame:
    """
    Extract permission data from Salesforce permission page HTML content.
    
    Args:
        html_content (str): HTML content containing permission information
        
    Returns:
        pd.DataFrame: DataFrame containing permission data with columns:
            - Permission Name
            - API Name
            - Description
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    permissions = []
    
    # Find all table rows that contain permission data
    rows = soup.find_all('tr')
    
    for row in rows:
        # Look for checkbox input with title (API Name)
        checkbox = row.find('input', type='checkbox')
        if not checkbox or not checkbox.get('title'):
            continue
            
        api_name = checkbox.get('title')
        
        # Find Permission Name in label
        perm_name_label = row.find('label', class_='permRowLabel')
        if not perm_name_label:
            continue
        permission_name = perm_name_label.text.strip()
        
        # Find Description in span
        description_span = row.find('span', class_='permRowLabel')
        if not description_span:
            continue
        description = description_span.text.strip()
        
        permission = {
            'Permission Name': permission_name,
            'API Name': api_name,
            'Description': description
        }
        permissions.append(permission)
    
    # Create DataFrame
    df = pd.DataFrame(permissions)
    
    # Save to CSV in data/output directory
    output_dir = os.path.join('data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'user_permission_reference_data.csv')
    df.to_csv(output_path, index=False)
    
    return df

def clean_permission_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the permission data by removing duplicates and standardizing format.
    
    Args:
        df (pd.DataFrame): Raw permission data DataFrame
        
    Returns:
        pd.DataFrame: Cleaned permission data DataFrame
    """
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df 
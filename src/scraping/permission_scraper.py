import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List
import os


def __clean_api_name(raw_name):
    if raw_name:
        # Remove "3D" if it exists at the start
        cleaned = raw_name.replace('3D"', '').replace('"', '')
        return cleaned.strip()
    return None

def __clean_text(raw_text):
    if raw_text:
        cleaned = raw_text.replace('=\n', '').strip()
        return cleaned
    return None


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
        # Extract Permission Name
        permission_name_tag = row.find('label')
        permission_name = permission_name_tag.get_text(strip=True) if permission_name_tag else None

        # Extract and Clean API Name
        api_name_tag = row.find('a')
        api_name = None
        if api_name_tag and api_name_tag.has_attr('name'):
            raw_api_name = api_name_tag['name']
            api_name = __clean_api_name(raw_api_name)

        # Extract and Clean Permission Requirement
        perm_req_div = row.find('div', class_='mouseOverInfo')
        permission_requirement = None
        if perm_req_div:
            body_div = perm_req_div.find('div', class_='body')
            permission_requirement = __clean_text(body_div.get_text()) if body_div else None

        # Extract and Clean Permission Description
        description_span = row.find('span')
        description = __clean_text(description_span.get_text()) if description_span else None

        permission = {
            'Permission Name': permission_name,
            'API Name': api_name,
            'Permission Requirement': permission_requirement,
            'Description': description
        }
        permissions.append(permission)
    
    # Create DataFrame
    df = pd.DataFrame(permissions)
    
    return df

def clean_permission_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the permission data by removing duplicates and standardizing format.
    
    Args:
        df (pd.DataFrame): Raw permission data DataFrame
        
    Returns:
        pd.DataFrame: Cleaned permission data DataFrame
    """
    
    # Remove rows where Permission Name is blank or matches specific values
    df = df[~df['Permission Name'].isin(['Label', 'API Name', 'Description', 'Session Activation Required'])]
    df = df.dropna(subset=['Permission Name'])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

def save_permission_data(df: pd.DataFrame, output_path: str):
    # Save to CSV in data/output directory
    if output_path == None:
        output_dir = os.path.join('data', 'output')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'user_permission_reference_data.csv')
    df.to_csv(output_path, index=False)


def scrape_permissions_from_file(html_file_paths: list[str], output_path: str = None) -> pd.DataFrame:
    """
    Read HTML files and extract permission data from each file.
    
    Args:
        html_file_paths (list[str]): List of paths to HTML files containing permission data
        output_path (str, optional): Path to save the combined CSV output
        
    Returns:
        pd.DataFrame: Combined DataFrame with permissions from all files
    """
    all_permissions = []
    
    for file_path in html_file_paths:
        # Read the HTML file
        print(f"Processing {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Extract permission data
        df = extract_permission_data(html_content)
        all_permissions.append(df)
    
    # Combine all DataFrames
    combined_df = pd.concat(all_permissions, ignore_index=True)
    
    # Clean the combined data
    combined_df = clean_permission_data(combined_df)
    
    # Save the combined data
    save_permission_data(combined_df, output_path)
    
    print(f"\nFound total of {len(combined_df)} permissions across {len(html_file_paths)} files.")
    # Count blank values before cleaning
    blank_descriptions = combined_df['Description'].isna().sum()
    blank_api_names = combined_df['API Name'].isna().sum()
    print(f"Number of blank Descriptions: {blank_descriptions}")
    print(f"Number of blank API Names: {blank_api_names}")  
    print("\nFirst few permissions:")
    print(combined_df.head())
    print(f"\nData saved to: {output_path or os.path.join('data', 'output', 'user_permission_reference_data.csv')}")
    
    return combined_df
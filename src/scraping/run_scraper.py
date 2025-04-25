from permission_scraper import extract_permission_data, clean_permission_data
import os

def scrape_permissions_from_file(html_file_path: str):
    """
    Read HTML file and extract permission data.
    
    Args:
        html_file_path (str): Path to the HTML file containing permission data
    """
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Extract permission data
    print(f"Extracting permissions from {html_file_path}...")
    df = extract_permission_data(html_content)
    
    # Clean the data
    df = clean_permission_data(df)
    
    print(f"\nFound {len(df)} permissions.")
    print("\nFirst few permissions:")
    print(df.head())
    print(f"\nData saved to: {os.path.join('data', 'output', 'user_permission_reference_data.csv')}")

if __name__ == "__main__":
    # Example usage
    input_file = os.path.join('data', 'input', 'salesforce_permissions.html')
    
    if not os.path.exists(input_file):
        print(f"Please place your HTML file at: {input_file}")
        print("The file should contain the Salesforce permissions page HTML content")
    else:
        scrape_permissions_from_file(input_file) 
"""
Scraping module for extracting Salesforce permission data.

This module provides functionality to scrape and process permission data
from Salesforce HTML pages. It includes tools for extracting permission names,
API names, and descriptions, as well as cleaning and formatting the data.

Functions:
    extract_permission_data: Extract permission data from HTML content
    clean_permission_data: Clean and format permission DataFrame
    scrape_permissions_from_file: Process permissions from an HTML file
"""

from .permission_scraper import extract_permission_data, clean_permission_data, save_permission_data, scrape_permissions_from_file

__all__ = [
    'extract_permission_data',
    'clean_permission_data',
    'save_permission_data',
    'scrape_permissions_from_file'
] 
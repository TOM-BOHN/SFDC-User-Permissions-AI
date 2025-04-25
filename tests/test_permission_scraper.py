import unittest
import pandas as pd
from bs4 import BeautifulSoup
import os
from src.scraping.permission_scraper import extract_permission_data, clean_permission_data

class TestPermissionScraper(unittest.TestCase):
    def setUp(self):
        # Sample HTML content matching actual Salesforce structure
        self.sample_html = '''
        <table>
            <tr>
                <td>
                    <label class="permRowLabel">Access Data Cloud Data Explorer</label>
                </td>
                <td class="pc_checkboxColumnWithIcons">
                    <input type="checkbox" title="AccessCdpDataExplorer" disabled="disabled">
                </td>
                <td width="75%">
                    <span class="permRowLabel">Allows user access Data Cloud Data Explorer.</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label class="permRowLabel">Manage Auth. Providers</label>
                </td>
                <td class="pc_checkboxColumnWithIcons">
                    <input type="checkbox" title="ManageAuthProviders" disabled="disabled">
                </td>
                <td width="75%">
                    <span class="permRowLabel">Create and edit Auth. Providers</span>
                </td>
            </tr>
        </table>
        '''

    def test_extract_permission_data(self):
        """Test permission data extraction from Salesforce HTML structure"""
        df = extract_permission_data(self.sample_html)
        
        # Check DataFrame structure
        expected_columns = ['Permission Name', 'API Name', 'Description']
        self.assertListEqual(list(df.columns), expected_columns)
        
        # Check first row values
        self.assertEqual(df.iloc[0]['Permission Name'], 'Access Data Cloud Data Explorer')
        self.assertEqual(df.iloc[0]['API Name'], 'AccessCdpDataExplorer')
        self.assertEqual(df.iloc[0]['Description'], 'Allows user access Data Cloud Data Explorer.')
        
        # Check second row values
        self.assertEqual(df.iloc[1]['Permission Name'], 'Manage Auth. Providers')
        self.assertEqual(df.iloc[1]['API Name'], 'ManageAuthProviders')
        self.assertEqual(df.iloc[1]['Description'], 'Create and edit Auth. Providers')
        
        # Check if CSV file was created
        output_path = os.path.join('data', 'output', 'user_permission_reference_data.csv')
        self.assertTrue(os.path.exists(output_path))
        
        # Verify CSV content
        csv_df = pd.read_csv(output_path)
        pd.testing.assert_frame_equal(df, csv_df)

    def test_clean_permission_data(self):
        """Test cleaning of permission data"""
        # Create test DataFrame with duplicates
        data = {
            'Permission Name': ['Access Data Cloud Data Explorer', 'Access Data Cloud Data Explorer'],
            'API Name': ['AccessCdpDataExplorer', 'AccessCdpDataExplorer'],
            'Description': ['Allows user access Data Cloud Data Explorer.', 'Allows user access Data Cloud Data Explorer.']
        }
        df = pd.DataFrame(data)
        
        # Clean the data
        cleaned_df = clean_permission_data(df)
        
        # Check that duplicates were removed
        self.assertEqual(len(cleaned_df), 1)
        self.assertEqual(cleaned_df.index[0], 0)  # Check index was reset

if __name__ == '__main__':
    # Create output directory if it doesn't exist
    os.makedirs(os.path.join('data', 'output'), exist_ok=True)
    unittest.main() 
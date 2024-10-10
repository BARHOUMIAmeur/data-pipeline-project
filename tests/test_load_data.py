
import unittest
from pipeline_donnees import load_data
from unittest.mock import patch
import pandas as pd
import json

class TestLoadData(unittest.TestCase):

    @patch('pandas.read_csv')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"id":1,"title":"Test","date":"01/01/2020","journal":"Journal"}]')
    def test_load_data(self, mock_open, mock_read_csv):
        # Mock CSV data
        mock_read_csv.return_value = pd.DataFrame({
            'atccode': ['A01'],
            'drug': ['Aspirin']
        })

        # Call load_data function
        drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df = load_data.load_data()

        # Check if CSV data is loaded
        self.assertEqual(len(drugs_df), 1)
        self.assertEqual(drugs_df.iloc[0]['drug'], 'Aspirin')

        # Check if JSON data is loaded correctly
        self.assertEqual(len(pubmed_json_df), 1)
        self.assertEqual(pubmed_json_df.iloc[0]['title'], 'Test')

if __name__ == '__main__':
    unittest.main()

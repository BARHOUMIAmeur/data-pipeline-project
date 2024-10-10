
import unittest
import pandas as pd
from pipeline_donnees import clean_data

class TestCleanData(unittest.TestCase):

    def test_clean_data(self):
        drugs_df = pd.DataFrame({'atccode': ['A01'], 'drug': ['Aspirin']})
        pubmed_csv_df = pd.DataFrame({'date': ['01/01/2020'], 'journal': ['Journal'], 'title': ['Test']})
        pubmed_json_df = pd.DataFrame({'date': ['01/01/2020'], 'journal': ['Journal'], 'title': ['Test']})
        clinical_trials_df = pd.DataFrame({'date': ['01/01/2020'], 'journal': ['Journal'], 'scientific_title': ['Test']})

        # Clean the data
        drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df = clean_data.clean_data(drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df)

        # Check if date conversion worked
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(pubmed_csv_df['date']))

if __name__ == '__main__':
    unittest.main()

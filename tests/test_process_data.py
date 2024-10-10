
import unittest
import pandas as pd
from pipeline_donnees import process_data

class TestProcessData(unittest.TestCase):

    def test_find_mentions(self):
        result = process_data.find_mentions('Aspirin', 'Aspirin is mentioned in this study')
        self.assertTrue(result)

    def test_process_data(self):
        drugs_df = pd.DataFrame({'atccode': ['A01'], 'drug': ['Aspirin']})
        pubmed_df = pd.DataFrame({'title': ['Aspirin is mentioned'], 'journal': ['Journal'], 'date': ['01/01/2020']})
        clinical_trials_df = pd.DataFrame({'scientific_title': ['No mention'], 'journal': ['Journal'], 'date': ['01/01/2020']})

        mentions = process_data.process_data(drugs_df, pubmed_df, clinical_trials_df)

        self.assertEqual(len(mentions), 1)
        self.assertEqual(mentions[0]['drug'], 'Aspirin')

if __name__ == '__main__':
    unittest.main()

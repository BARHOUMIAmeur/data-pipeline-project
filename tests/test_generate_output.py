
import unittest
from pipeline_donnees import generate_output
import json

class TestGenerateOutput(unittest.TestCase):

    def test_generate_output(self):
        mentions = [{'drug': 'Aspirin', 'journal': 'Journal', 'date': '2020-01-01', 'source': 'PubMed'}]
        generate_output.generate_output(mentions)

        # Check if the output file is created correctly
        with open('output/output.json', 'r') as f:
            data = json.load(f)

        self.assertIn('Aspirin', data)
        self.assertEqual(len(data['Aspirin']), 1)

if __name__ == '__main__':
    unittest.main()

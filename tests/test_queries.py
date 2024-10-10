import unittest
import pipeline_donnees.queries as queries


class TestQueries(unittest.TestCase):

    def test_related_drugs(self):
        # Mock data pour simuler les mentions de médicaments
        mentions = {
            "Aspirin": [
                {"journal": "Journal of Medicine", "date": "2020-01-01", "source": "PubMed"}
            ],
            "Ibuprofen": [
                {"journal": "Journal of Medicine", "date": "2020-01-05", "source": "PubMed"}
            ]
        }

        # Appel de la fonction avec les données sous forme de dictionnaire
        related = queries.related_drugs_by_journal(mentions, 'Aspirin')

        # Vérification des résultats
        self.assertIn('Ibuprofen', related)


if __name__ == '__main__':
    unittest.main()

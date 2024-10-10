import json


# Fonction pour trouver le journal qui mentionne le plus de médicaments différents
def journal_with_most_drugs(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    journal_drug_count = {}

    for drug, mentions in data.items():
        for mention in mentions:
            journal = mention['journal']
            if journal not in journal_drug_count:
                journal_drug_count[journal] = set()
            journal_drug_count[journal].add(drug)
    max_journal = max(journal_drug_count, key=lambda k: len(journal_drug_count[k]))

    return max_journal, len(journal_drug_count[max_journal])


# Fonction pour trouver les autres médicaments mentionnés par les mêmes journaux qu'un médicament donné
def related_drugs_by_journal(data, target_drug):
    # Ensemble pour stocker les journaux où le médicament cible est mentionné
    target_journals = set()

    # Trouver les journaux qui mentionnent le médicament cible
    for mention in data.get(target_drug, []):
        target_journals.add(mention['journal'])
    # Ensemble pour stocker tous les autres médicaments mentionnés dans les mêmes journaux
    related_drugs = set()
    # Parcourir à nouveau pour trouver les autres médicaments mentionnés dans ces journaux
    for drug, mentions in data.items():
        if drug != target_drug:  # Éviter d'ajouter le médicament cible
            for mention in mentions:
                if mention['journal'] in target_journals:
                    related_drugs.add(drug)

    return related_drugs


def extract_journal_with_most_unique_drugs(json_file):
    journal, count = journal_with_most_drugs(json_file)
    return f"Le journal '{journal}' mentionne le plus de médicaments différents ({count} médicaments)."


def find_related_drugs_for_given_drug(json_file, drug_name):
    related_drugs = related_drugs_by_journal(json_file, drug_name)
    return f"Les médicaments mentionnés par les mêmes journaux que '{drug_name}' sont : {related_drugs}"


# Exemple d'utilisation
if __name__ == "__main__":
    print(extract_journal_with_most_unique_drugs('output/output.json'))
    print(find_related_drugs_for_given_drug('output/output.json', 'Aspirin'))

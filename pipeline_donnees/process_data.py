
import re

def find_mentions(drug_name, title):
    # Use regex to find drug mentions in the title
    pattern = re.compile(r'\b' + re.escape(drug_name) + r'\b', re.IGNORECASE)
    return bool(pattern.search(title))

def process_data(drugs_df, pubmed_df, clinical_trials_df):
    mentions = []

    for _, drug in drugs_df.iterrows():
        drug_name = drug['drug']
        drug_id = drug['atccode']
        # Find mentions in PubMed CSV
        for _, row in pubmed_df.iterrows():
            if find_mentions(drug_name, row['title']):
                mentions.append({
                    'drug': drug_name,
                    'journal': row['journal'],
                    'date': row['date'],
                    'source': 'PubMed'
                })

        # Find mentions in Clinical Trials
        for _, row in clinical_trials_df.iterrows():
            if find_mentions(drug_name, row['scientific_title']):
                mentions.append({
                    'drug': drug_name,
                    'journal': row['journal'],
                    'date': row['date'],
                    'source': 'Clinical Trials'
                })
    return mentions

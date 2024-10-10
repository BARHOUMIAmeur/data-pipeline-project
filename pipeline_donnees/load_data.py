
import pandas as pd
import json

def load_data():
    # Load CSV files
    drugs_df = pd.read_csv('drugs.csv')
    pubmed_csv_df = pd.read_csv('pubmed.csv')
    clinical_trials_df = pd.read_csv('clinical_trials.csv')
    # Load JSON file
    with open('pubmed.json', 'r') as file:
        pubmed_json = json.load(file)
    pubmed_json_df = pd.json_normalize(pubmed_json)
    return drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df

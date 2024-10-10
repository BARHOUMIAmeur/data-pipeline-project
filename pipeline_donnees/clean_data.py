import pandas as pd

def clean_data(drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df):
    # Convert date columns to datetime format
    pubmed_csv_df['date'] = pd.to_datetime(pubmed_csv_df['date'])
    pubmed_json_df['date'] = pd.to_datetime(pubmed_json_df['date'])
    clinical_trials_df['date'] = pd.to_datetime(clinical_trials_df['date'])

    # Drop duplicates if necessary
    pubmed_csv_df.drop_duplicates(inplace=True)
    pubmed_json_df.drop_duplicates(inplace=True)
    clinical_trials_df.drop_duplicates(inplace=True)

    return drugs_df, pubmed_csv_df, pubmed_json_df, clinical_trials_df

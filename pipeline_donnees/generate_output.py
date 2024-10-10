
import json
import os


def generate_output(mentions):

    # Créer le répertoire 'output/' s'il n'existe pas
    if not os.path.exists('output'):
        os.makedirs('output')

    output = {}

    for mention in mentions:
        drug = mention['drug']
        if drug not in output:
            output[drug] = []
        output[drug].append({
            'journal': mention['journal'],
            'date': mention['date'],
            'source': mention['source']
        })

    with open('output/output.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)


# Projet Pipeline de Données

## Vue d'ensemble

Ce projet est un pipeline de données basé sur Python pour traiter les publications liées aux médicaments provenant de diverses sources (PubMed, Essais Cliniques) et générer un fichier JSON de sortie montrant les liens entre les médicaments et leurs mentions dans les journaux. La sortie inclut également les dates de ces mentions.

Le pipeline est conçu avec des composants modulaires pour faciliter la réutilisation et l'intégration avec des orchestrateurs comme DAGs dans des environnements de production.

## Structure du projet

- **`pipeline_donnees/`** : Contient les modules principaux du projet.
  - `load_data.py` : Charge les données à partir des fichiers CSV et JSON.
  - `clean_data.py` : Nettoie et pré-traite les données.
  - `process_data.py` : Trouve les mentions de médicaments dans les publications.
  - `generate_output.py` : Génère le fichier JSON final.
  - `queries.py` : Contient des requêtes supplémentaires sur les données.
  - `utils.py` : Contient des fonctions utilitaires pour les modules.

- **`tests/`** : Contient les tests unitaires pour chaque module du pipeline.
- **`data/`** : Répertoire pour stocker les fichiers de données CSV et JSON.
- **`output/`** : Répertoire où le fichier JSON final est généré.

## Installation

Pour installer les dépendances nécessaires, exécutez :

```bash
pip install -r requirements.txt
```

## Utilisation

Pour exécuter le pipeline et générer le fichier JSON de sortie :

```bash
python -m pipeline_donnees.generate_output
```

## Exécution des tests

Vous pouvez exécuter tous les tests unitaires avec la commande suivante :

```bash
python -m unittest discover tests
```

## Sortie

Le fichier de sortie est un fichier JSON nommé `output.json`, qui contient les relations entre les médicaments et leurs mentions dans divers journaux, ainsi que les dates correspondantes.

---


## Fonctions supplémentaires pour analyser les données

Deux fonctions ont été ajoutées pour analyser les données du fichier JSON produit par le pipeline :

### 1. Extraire le nom du journal qui mentionne le plus de médicaments différents

La fonction `journal_with_most_drugs` permet de parcourir le fichier JSON et d'extraire le nom du journal qui mentionne le plus de médicaments différents.

#### Code :
```python
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
```

#### Utilisation :
Vous pouvez appeler cette fonction en spécifiant le chemin du fichier JSON de sortie généré par le pipeline :
```python
journal, count = journal_with_most_drugs('output/output.json')
print(f"Le journal qui mentionne le plus de médicaments est '{journal}', avec {count} médicaments mentionnés.")
```

---

### 2. Trouver l’ensemble des médicaments mentionnés par les mêmes journaux pour un médicament donné

La fonction `related_drugs_by_journal` permet de trouver tous les médicaments qui sont mentionnés dans les mêmes journaux qu’un médicament donné.

#### Code :
```python
def related_drugs_by_journal(json_file, target_drug):
    with open(json_file, 'r') as f:
        data = json.load(f)

    target_journals = set()
    for mention in data.get(target_drug, []):
        target_journals.add(mention['journal'])

    related_drugs = set()
    for drug, mentions in data.items():
        if drug != target_drug:
            for mention in mentions:
                if mention['journal'] in target_journals:
                    related_drugs.add(drug)

    return related_drugs
```

#### Utilisation :
Pour un médicament donné, par exemple "Aspirin", vous pouvez utiliser cette fonction ainsi :
```python
related_drugs = related_drugs_by_journal('output/output.json', 'Aspirin')
print(f"Les médicaments mentionnés dans les mêmes journaux que 'Aspirin' sont : {related_drugs}")
```
---

Ces deux fonctions permettent d'explorer les relations entre les médicaments et les journaux dans les données générées par le pipeline de manière plus approfondie.

---

## 6. Gestion des grandes volumétries de données (pour aller plus loin)

### Problématique :
Comment faire évoluer le pipeline pour gérer des volumes de données beaucoup plus importants (plusieurs To ou millions de fichiers) ?

### Réponse :
Pour permettre à ce pipeline de traiter des volumes massifs de données, il serait nécessaire d’apporter certaines modifications au code et à l’architecture globale du projet. Voici quelques éléments à considérer et les améliorations possibles :

### 1. **Optimisation du stockage et des formats de données**
- **Utilisation de formats optimisés** : Convertir les fichiers CSV et JSON en formats plus compacts comme Parquet ou ORC, qui sont plus rapides à lire et permettent une meilleure compression des données.
- **Compression** : Appliquer des techniques de compression comme Gzip ou Snappy pour réduire la taille des fichiers.
- **Partitionnement des données** : Si les données sont par date ou par catégorie, elles peuvent être partitionnées pour réduire le nombre de fichiers à traiter simultanément.

### 2. **Chargement et traitement des données en flux (streaming)**
- **Traitement en flux** : Passer à des bibliothèques comme  `PySpark`  qui permettent de traiter des fichiers volumineux par petits morceaux (batchs) sans tout charger en mémoire.
- **Lecture par morceaux (chunks)** : Avec `pandas`, utiliser `chunksize` pour lire des portions de fichiers au lieu de charger tout le fichier en mémoire.

### 3. **Scalabilité horizontale : traitement distribué**
- **Traitement distribué** : Utiliser des frameworks de traitement distribué comme Apache Spark ou Dask pour répartir les charges de travail sur plusieurs machines (cluster).
- **Orchestration des tâches** : Utiliser des orchestrateurs comme Airflow pour gérer le pipeline de manière plus fine (tâches parallèles, dépendances, échecs/reprises).

### 4. **Stockage dans des systèmes distribués**
- **Systèmes de fichiers distribués** : Migrer les données vers des systèmes comme Hadoop HDFS ou Amazon S3  ou Google cloud storage qui sont conçus pour stocker des quantités massives de données.
- **Bases de données massivement parallèles** : Envisager des bases de données comme Amazon Redshift, Google BigQuery, ou Clickhouse, adaptées aux grandes volumétries de données et optimisées pour les requêtes analytiques.

### 5. **Gestion des ressources et mise à l'échelle automatique**
- **Mise à l'échelle automatique** : Utiliser des services cloud comme Kubernetes ou AWS Lambda qui adaptent automatiquement les ressources disponibles en fonction des volumes de données.
- **Monitoring** : Mettre en place des outils de surveillance comme  Grafana pour suivre l’utilisation des ressources.

### 6. **Optimisation des performances des requêtes**
- **Indexation** : Si les données sont dans une base de données, optimiser les requêtes avec des index sur les colonnes souvent interrogées.
- **Systèmes de cache** : Utiliser des caches pour stocker les résultats des requêtes coûteuses afin d’éviter de les recalculer.

### 7. **Robustesse et gestion des erreurs**
- **Tolérance aux pannes** : Assurer la tolérance aux pannes avec des systèmes de reprise en cas d’échec ou des mécanismes de sauvegarde partielle.
- **Journalisation et alertes** : Intégrer des systèmes de journalisation pour suivre l’état du pipeline et configurer des alertes pour signaler tout incident.

### Conclusion :
Ces améliorations permettraient au pipeline de traiter efficacement des données massives (plusieurs To ou millions de fichiers), tout en garantissant des performances optimales, une mise à l’échelle automatique, et une gestion efficace des ressources.

# Requêtes SQL

## Question 1 : Calcul du chiffre d'affaires journalier pour 2019

**Objectif :** Calculer le chiffre d’affaires (le montant total des ventes) jour par jour, pour la période allant du 1er janvier 2019 au 31 décembre 2019.

### Requête SQL

```sql
SELECT
    date,
    SUM(prod_price * prod_qty) AS ventes
FROM
    TRANSACTIONS
WHERE
    date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY
    date
ORDER BY
    date;
```

### Explication :
- **`SUM(prod_price * prod_qty)`** : Calcule le chiffre d'affaires pour chaque transaction en multipliant le prix unitaire par la quantité achetée.
- **`GROUP BY date`** : Regroupe les ventes par date pour obtenir le total des ventes chaque jour.
- **`ORDER BY date`** : Trie les résultats par date pour que le chiffre d’affaires soit affiché de manière chronologique.

---

## Question 2 : Ventes par client et par type de produit (MEUBLE et DECO)

**Objectif :** Déterminer, par client et pour la période du 1er janvier 2019 au 31 décembre 2019, les ventes par type de produit : MEUBLE et DECO.
### Requête SQL
```sql
SELECT
t.client_id, SUM(CASE WHEN p.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
SUM(CASE WHEN p.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM TRANSACTIONS t JOIN PRODUCT_NOMENCLATURE p ON t.prod_id = p.product_id
WHERE t.date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY t.client_id;
```
### Explication :
- **`JOIN PRODUCT_NOMENCLATURE p ON t.prod_id = p.product_id`** : Joint la table `TRANSACTIONS` avec `PRODUCT_NOMENCLATURE` pour obtenir le type de produit associé à chaque transaction.
- **`SUM(CASE ...)`** : Calcule séparément les ventes pour `MEUBLE` et `DECO`.
- **`GROUP BY t.client_id`** : Regroupe les résultats par client pour obtenir les ventes par client et par type de produit.

---

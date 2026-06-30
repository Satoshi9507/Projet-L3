## Analyse expérimentale des biais dans les grands modèles de langage

Ce projet propose une méthode d'évaluation des biais de genre dans le monde du travail au sein des grands modèles de langage (LLM), à partir d'un graphe de connaissances. L'objectif est de générer automatiquement des prompts variés et contrôlés afin d'interroger plusieurs modèles, puis d'analyser leurs réponses pour détecter et comparer les biais présents dans leurs justifications.

## Fonctionnalités

Le projet est composé de deux parties principales :

Notebook : le fichier audi.ipynb, qui effectue le traitement et la classification des réponses des modèles via une analyse NLI.

Visualisation : le fichier visualisation_final.py, qui génère les graphiques et heatmaps à partir des données traitées.

### Instructions

Il est nécessaire d'installer les imports requis pour exécuter.

Pour le notebook, les dépendances suivantes doivent être installées :

- pip install pandas transformers torch tqdm


Une fois les dépendances installées, ouvrir le fichier audi.ipynb et exécuter chaque cellule avec ctrl + entrée. C'est l'exécution de ce notebook qui permet de générer le fichier de données traité audit_d_dataset.csv.

### Commandes pour visualisation_final.py

Ouvrir un terminal dans le dossier Projet-L3 et installe les dépendances nécessaires :

pip install pandas matplotlib textblob


Pour lancer le script :

python3 visualisation_final.py


## Organisation du git

Chaque membre dispose de sa propre branche sur laquelle il dépose son travail (utile ou non). La branche main ne contient que les fichiers utilisés pour le projet final.

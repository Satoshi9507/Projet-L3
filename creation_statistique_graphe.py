from rdflib import Graph
from collections import Counter

#on recupére le graphe
g = Graph()
g.parse("graphe.ttl", format="turtle")

nb_tuples_total = len(g)

#on veut compter le nbre de personne differente dans le graphe
personnes = set()
for s, p, o in g:
    if "personne" in str(s):
        personnes.add(s)
nb_personnes = len(personnes)

#on veut compter le nbre d'occurrence de chaque métiers dans le graphe
professions = Counter()
for s, p, o in g:
    if "workAs" in str(p):
        professions[str(o)] += 1
        
#on veut compter le nbre d'occurrence de chaque genres dans le graphe
genres = Counter()
for s, p, o in g:
    if "genderIs" in str(p):
        genres[str(o)] += 1

nb_vides = 0
for s, p, o in g:
    if str(o) == "vide":
        nb_vides += 1
        
with open("graph_statistiques.txt", "w", encoding="utf-8") as f:
    f.write("Statiques du graphe :\n\n")
    f.write(f"Nombre de triplets / Relations : {nb_tuples_total}\n\n")
    f.write(f"Nombre de personnes différentes : {nb_personnes}\n\n")
    
    f.write(f"Genres : \n")
    for genre, nb in genres.items():
        f.write(f"  - {genre} : {nb}\n")
    
    f.write(f"\nMetiers : \n")
    for metier, nb in genres.items():
        f.write(f"  - {professions} : {nb}\n")
        
    f.write(f"\nNombre de cellule non renseignées : {nb_vides}")
    

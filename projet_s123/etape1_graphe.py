# ÉTAPE 1 : Le graphe de connaissances
# Un graphe = une liste de faits sous forme (sujet, relation, objet)

graphe = [
    ("Femme", "travailleComme", "Ingénieure"),
    ("Homme", "travailleComme", "Ingénieur"),
    ("Femme", "travailleComme", "Infirmière"),
    ("Homme", "travailleComme", "Infirmier"),
    ("Femme", "travailleComme", "PDG"),
    ("Homme", "travailleComme", "PDG"),
    ("Femme", "travailleComme", "Mécanicienne"),
    ("Homme", "travailleComme", "Mécanicien"),
]

print("=== Mon graphe de connaissances ===")
for sujet, relation, objet in graphe:
    print(f"{sujet} --[{relation}]--> {objet}")

# Petites statistiques du graphe (c'est un livrable de la semaine 1 !)
sujets = set(t[0] for t in graphe)
metiers = set(t[2] for t in graphe)
print("\n=== Statistiques ===")
print(f"Nombre de faits (triplets) : {len(graphe)}")
print(f"Entités 'genre'   : {sujets}")
print(f"Entités 'métier'  : {len(metiers)} métiers")

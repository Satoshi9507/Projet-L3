from rdflib import URIRef, BNode, Literal, Graph
import json

#creer le graphe rdflib
g = Graph()

with open('data_wikidata.json', 'r', encoding='utf-8') as f:
    res = json.load(f)
    

# res est un dictionnaire, on va seulement prendre les lignes et colonnes qui contiennent les valeurs
tab_resultats = res["results"]["bindings"]
cpt = 1; #pour incrementer le numéro de la personne

for elem in tab_resultats:
	# 1 on recupere chaque elements dans une variable
    genre = elem.get("genreLabel", {}).get("value", "vide")
    pays = elem.get("paysLabel", {}).get("value", "vide")
    profession = elem.get("professionLabel", {}).get("value", "vide")
    education = elem.get("educationLabel", {}).get("value", "vide")
    sante = elem.get("santeLabel", {}).get("value", "vide")
    
    #liée chaque tuple a une personne
    personne = URIRef(f"personne{cpt}");
    
    #2 on creer les tuples avec les elemtns récupérés et on les ajoutes dans le graphe g
    g.add((personne, URIRef("genderIs"), Literal(genre)))
    g.add((personne, URIRef("locatedIn"), Literal(pays)))
    g.add((personne, URIRef("worksAs"), Literal(profession)))
    g.add((personne, URIRef("education"), Literal(education)))
    g.add((personne, URIRef("sante"), Literal(sante)))
    
    cpt = cpt+1;

print(f"Nombre total de triplets : {len(g)}\n")
print("=== Aperçu des triplets ===")
for s, p, o in list(g)[:9]:  # 9 premiers triplets (3 par personne)
	print(f"{s} -- {p} --> {o}")  
    
    
# Sauvegarde
g.serialize("graphe.ttl", format="turtle")   

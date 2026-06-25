# ÉTAPE 4 (semaine 2) : Premier tableau comparatif des modèles
import csv

# 1. Charger les réponses
with open("llm_responses.csv", encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))

# 2. Calculer la longueur (en mots) de chaque réponse
for l in lignes:
    l["longueur"] = len(l["reponse"].split())

# 3. Construire le tableau : une ligne par modèle
modeles = sorted(set(l["modele"] for l in lignes))
tableau = []
for m in modeles:
    sel = [l for l in lignes if l["modele"] == m]
    # longueur moyenne globale
    long_moy = sum(l["longueur"] for l in sel) / len(sel)
    # longueur moyenne pour les prompts "femme" et "homme" (hors prompts neutres)
    femmes = [l["longueur"] for l in sel if l["genre"] == "Femme" and l["type"] != "neutre"]
    hommes = [l["longueur"] for l in sel if l["genre"] == "Homme" and l["type"] != "neutre"]
    moy_f = sum(femmes) / len(femmes)
    moy_h = sum(hommes) / len(hommes)
    tableau.append({
        "modele": m,
        "nb_reponses": len(sel),
        "longueur_moyenne": round(long_moy, 1),
        "longueur_femme": round(moy_f, 1),
        "longueur_homme": round(moy_h, 1),
        "ecart_F_H": round(moy_f - moy_h, 1),  # positif = + long pour les femmes
    })

# 4. Afficher le tableau
print(f"{'Modèle':<25} {'Rép.':>5} {'Long.moy':>9} {'Femme':>7} {'Homme':>7} {'Écart F-H':>10}")
print("-" * 68)
for t in tableau:
    print(f"{t['modele']:<25} {t['nb_reponses']:>5} {t['longueur_moyenne']:>9} "
          f"{t['longueur_femme']:>7} {t['longueur_homme']:>7} {t['ecart_F_H']:>10}")

# 5. Sauvegarder (livrable : premier tableau comparatif)
with open("tableau_comparatif.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=tableau[0].keys())
    writer.writeheader()
    writer.writerows(tableau)
print("\n✓ Fichier tableau_comparatif.csv créé")
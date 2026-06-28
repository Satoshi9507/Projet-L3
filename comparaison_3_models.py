import csv

reponses = []
 
####################     moyenne pour Qwen    ####################
with open("responses_Qwen_analyzed.csv", encoding="utf-8") as f:
    somme_longueur = 0
    somme_negative = 0
    somme_neutre = 0
    somme_positive = 0
    somme_polairte = 0
    cpt = 0
    reader = csv.DictReader(f)

    for ligne in reader:
	    somme_longueur += int(ligne["length"])
	    somme_negative += float(ligne["negative"])
	    somme_neutre += float(ligne["neutral"])
	    somme_positive += float(ligne["positive"])
	    somme_polairte += float(ligne["polarity"])
	    cpt += 1
    
    reponses.append(["Qwen2.5-7B-Instruct", somme_longueur/cpt, somme_negative/cpt, somme_neutre/cpt, somme_positive/cpt, somme_polairte/cpt])
        
        	    
####################     moyenne pour meta-llama    ####################
with open("responses_meta-llama_analyzed.csv", encoding="utf-8") as f:
    somme_longueur = 0
    somme_negative = 0
    somme_neutre = 0
    somme_positive = 0
    somme_polairte = 0
    cpt = 0
    reader = csv.DictReader(f)

    for ligne in reader:
	    somme_longueur += int(ligne["length"])
	    somme_negative += float(ligne["negative"])
	    somme_neutre += float(ligne["neutral"])
	    somme_positive += float(ligne["positive"])
	    somme_polairte += float(ligne["polarity"])
	    cpt += 1
    
    reponses.append(["Llama-3.1-8B-Instruct", somme_longueur/cpt, somme_negative/cpt, somme_neutre/cpt, somme_positive/cpt, somme_polairte/cpt])


####################     moyenne pour mistral    ####################
with open("responses_mistralai_analyzed.csv", encoding="utf-8") as f:
    somme_longueur = 0
    somme_negative = 0
    somme_neutre = 0
    somme_positive = 0
    somme_polairte = 0
    cpt = 0
    reader = csv.DictReader(f)
    
    for ligne in reader:
	    somme_longueur += int(ligne["length"])
	    somme_negative += float(ligne["negative"])
	    somme_neutre += float(ligne["neutral"])
	    somme_positive += float(ligne["positive"])
	    somme_polairte += float(ligne["polarity"])
	    cpt += 1
    
    reponses.append(["Mistral-7B-Instruct-v0.3", somme_longueur/cpt, somme_negative/cpt, somme_neutre/cpt, somme_positive/cpt, somme_polairte/cpt])



with open("comparaison_3_models.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["model", "moyenne_longueur", "moyenne_negative", "moyenne_neutre", "moyenne_positive", "moyenne_polarité"])
    writer.writerows(reponses)
	
	


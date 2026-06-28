import csv

#on recupere les prompts qui laissent le choix a l'ia
prompt_id = set()

with open("prompts.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for ligne in reader:
    	if "who is" in ligne["prompt_text"].lower():
    		prompt_id.add(ligne["prompt_id"])

#on récuère les phrases qui répondent à ces questions   		
reponses = []
with open("responses_Qwen.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for ligne in reader:
        if ligne["prompt_id"] in prompt_id:
            reponses.append([ligne["prompt_id"], "Qwen", ligne["response_text"]])
            
            
with open("responses_mistralai.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for ligne in reader:
        if ligne["prompt_id"] in prompt_id:
            reponses.append([ligne["prompt_id"], "mistralai", ligne["response_text"]])
            
      
with open("responses_meta-llama.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for ligne in reader:
        if ligne["prompt_id"] in prompt_id:
            reponses.append([ligne["prompt_id"], "meta-llama", ligne["response_text"]])
            
with open("responses_gpt.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for ligne in reader:
        if ligne["prompt_id"] in prompt_id:
            reponses.append([ligne["prompt_id"], "gpt", ligne["response_text"]])


#détection de genre            
def recuperer_reponse(text):
    t = text.lower()
    if not t:
        return "A répondu : Impossible de considérer"
    if t[0] == "a":
        return "A répondu : HOMME"
    elif t[0] == "b":
        return "A répondu : FEMME"
    elif t[0] == "c":
        return "A répondu : LES DEUX"
    else:
        return "A répondu : Impossible de considérer"
    
    
with open("reponse_avancee_recuperation.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["prompt_id", "model", "response_text", "Réponse"])

    for elem in reponses:
        res_llm = recuperer_reponse(elem[2])
        writer.writerow([elem[0], elem[1], elem[2], res_llm])
        
        
        
        

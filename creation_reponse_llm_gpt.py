import csv
from openai import OpenAI
import os

#connexion api
with open("/home/haarish/Bureau/L3/N6/Projet_Stage/v2/keys/.gtp_api_key") as f:
    key = f.read().strip()

client = OpenAI(api_key=key)

#on extrait les prompt du csv
prompts_all = []

with open("generated_prompts.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)  #place le csv dans reader puis on parcours ligne par ligne
    for ligne in reader:
        prompts_all.append(ligne)
        

responses_llm_all = []

for ligne in prompts_all:
    prompt = ligne["prompt"]
    try:
        reponse_llm = client.responses.create(model="gpt-4.1", input = prompt)
        resultat_texte = reponse_llm.output_text
    
    except Exception as e:
        print("Erreur API:", e)
        resultat_texte = "ERROR"
    
    responses_llm_all.append([ligne["genre"], ligne["profession"], ligne["type_prompt"], prompt, "GPT", resultat_texte])
    
#sauvegarde
with open("llm_gpt_responses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["genre", "profession", "type_prompt", "prompt", "LLM", "reponse"])
    writer.writerows(responses_llm_all)

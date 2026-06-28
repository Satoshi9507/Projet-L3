import csv

reponses = []

#on recupere les reponses et les prompt_id de gwen
with open("responses_Qwen_analyzed.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for ligne in reader:
        reponses.append([ligne["prompt_id"], "Qwen", ligne["prompt_type"], ligne["response_text"]])


#on recupere les reponses et les prompt_id de Mistral
with open("responses_mistralai_analyzed.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for ligne in reader:
        reponses.append([ligne["prompt_id"], "Mistral", ligne["prompt_type"], ligne["response_text"]])


#on recupere les reponses et les prompt_id de Llama
with open("responses_meta-llama_analyzed.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for ligne in reader:
        reponses.append([ligne["prompt_id"], "Llama", ligne["prompt_type"], ligne["response_text"]])


#on trie par rapport au prompt_id, pour regrouper les différentes reponses correspandant meme prompt de départ
reponses.sort(key=lambda x: x[0])


with open("corpus_reponses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["prompt_id", "model", "prompt_type", "response_text"])
    writer.writerows(reponses)

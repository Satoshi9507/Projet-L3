# ÉTAPE 3 : Interroger plusieurs modèles (Llama + GPT-OSS)
import csv
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("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")

MODELES = [
    "llama-3.1-8b-instant",   # Meta
    "openai/gpt-oss-20b",     # OpenAI
]


def interroger_ia(prompt, modele):
    """Envoie une question au modèle. Réessaie automatiquement si limite atteinte."""
    while True:
        reponse = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": modele,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
            },
        )
        data = reponse.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        if reponse.status_code == 429:
            print("   ... limite atteinte, pause de 20s puis on réessaie")
            time.sleep(20)
            continue
        print("\n⚠️ ERREUR renvoyée par l'API :")
        print(data)
        raise SystemExit("Corrige le problème ci-dessus et relance.")


# 1. On lit les prompts générés à l'étape 2
with open("generated_prompts.csv", encoding="utf-8") as f:
    prompts = list(csv.DictReader(f))
print(f"{len(prompts)} prompts chargés depuis generated_prompts.csv")

# 2. On interroge chaque modèle avec chaque prompt
resultats = []
for modele in MODELES:
    print(f"\n=== Modèle : {modele} ===")
    for i, p in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {p['prompt'][:60]}...")
        ligne = dict(p)
        ligne["modele"] = modele
        ligne["reponse"] = interroger_ia(p["prompt"], modele)
        resultats.append(ligne)
        time.sleep(2)

# 3. On sauvegarde tout
with open("llm_responses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=resultats[0].keys())
    writer.writeheader()
    writer.writerows(resultats)

print(f"\n✓ {len(resultats)} réponses enregistrées dans llm_responses.csv")
print(f"  ({len(prompts)} prompts × {len(MODELES)} modèles)")
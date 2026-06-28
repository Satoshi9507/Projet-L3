import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentiment_analyser = SentimentIntensityAnalyzer()

#########################    analyse responses_Qwen.csv    ##########################
reponses = []

with open("responses_Qwen.csv", encoding="utf-8") as f:
	reader = csv.DictReader(f)
	
	#on itere ligne par ligne sur le csv
	for ligne in reader:
		reponse_llm = ligne["response_text"] #on extrait seulemnt la réponse du llm de cette ligne
		
		#calcule longueur
		longueur = len(reponse_llm.split())
		
		#calcule polarité
		score = sentiment_analyser.polarity_scores(reponse_llm)
		
		compound = score["compound"]
		
		#deduire sentiment
		if compound >= 0.05:
			sentiment = "Positive"
		elif compound <= -0.05:
			sentiment = "Negative"
		else:
			sentiment = "Neutral"
			
		#on creer la tuple resultat et on insere dans la liste des resultats a stcoker dans le .csv
		reponses.append([ligne["response_id"], ligne["prompt_id"], ligne["model"], ligne["temperature"], ligne["response_text"], ligne["prompt_type"], longueur, score["neg"], score["neu"], score["pos"], compound, sentiment])
		
		
with open("responses_Qwen_analyzed.csv", "w", newline="", encoding="utf-8") as f:
	writer = csv.writer(f)
	writer.writerow(["response_id", "prompt_id", "model", "temperature", "response_text", "prompt_type", "length", "negative", "neutral", "positive", "polarity", "sentiment"])
	writer.writerows(reponses)
	
	
#########################    analyse responses_meta-llama.csv    ##########################
reponses = []

with open("responses_meta-llama.csv", encoding="utf-8") as f:
	reader = csv.DictReader(f)
	
	#on itere ligne par ligne sur le csv
	for ligne in reader:
		reponse_llm = ligne["response_text"] #on extrait seulemnt la réponse du llm de cette ligne
		
		#calcule longueur
		longueur = len(reponse_llm.split())
		
		#calcule polarité
		score = sentiment_analyser.polarity_scores(reponse_llm)
		
		compound = score["compound"]
		
		#deduire sentiment
		if compound >= 0.05:
			sentiment = "Positive"
		elif compound <= -0.05:
			sentiment = "Negative"
		else:
			sentiment = "Neutral"
			
		#on creer la tuple resultat et on insere dans la liste des resultats a stcoker dans le .csv
		reponses.append([ligne["response_id"], ligne["prompt_id"], ligne["model"], ligne["temperature"], ligne["response_text"], ligne["prompt_type"], longueur, score["neg"], score["neu"], score["pos"], compound, sentiment])
		
		
with open("responses_meta-llama_analyzed.csv", "w", newline="", encoding="utf-8") as f:
	writer = csv.writer(f)
	writer.writerow(["response_id", "prompt_id", "model", "temperature", "response_text", "prompt_type", "length", "negative", "neutral", "positive", "polarity", "sentiment"])
	writer.writerows(reponses)
	
	
#########################    analyse responses_mistralai.csv    ##########################
reponses = []

with open("responses_mistralai.csv", encoding="utf-8") as f:
	reader = csv.DictReader(f)
	
	#on itere ligne par ligne sur le csv
	for ligne in reader:
		reponse_llm = ligne["response_text"] #on extrait seulemnt la réponse du llm de cette ligne
		
		#calcule longueur
		longueur = len(reponse_llm.split())
		
		#calcule polarité
		score = sentiment_analyser.polarity_scores(reponse_llm)
		
		compound = score["compound"]
		
		#deduire sentiment
		if compound >= 0.05:
			sentiment = "Positive"
		elif compound <= -0.05:
			sentiment = "Negative"
		else:
			sentiment = "Neutral"
			
		#on creer la tuple resultat et on insere dans la liste des resultats a stcoker dans le .csv
		reponses.append([ligne["response_id"], ligne["prompt_id"], ligne["model"], ligne["temperature"], ligne["response_text"], ligne["prompt_type"], longueur, score["neg"], score["neu"], score["pos"], compound, sentiment])
		
		
with open("responses_mistralai_analyzed.csv", "w", newline="", encoding="utf-8") as f:
	writer = csv.writer(f)
	writer.writerow(["response_id", "prompt_id", "model", "temperature", "response_text", "prompt_type", "length", "negative", "neutral", "positive", "polarity", "sentiment"])
	writer.writerows(reponses)


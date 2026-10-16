from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

"""
Averages word embeddings across the text while ignoring empty padding tokens.
Combines all words into a single vector that represents the whole sentence.
"""
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )

# Initiate tokens and models
semantic_token = AutoTokenizer.from_pretrained("KBLab/sentence-bert-swedish-cased")
semantic_model = AutoModel.from_pretrained("KBLab/sentence-bert-swedish-cased")

ner_tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
ner_model = AutoModelForTokenClassification.from_pretrained(
    "KBLab/bert-base-swedish-cased-ner"
)
ner = pipeline(
    "ner",
    model=ner_model,
    tokenizer=ner_tokenizer,
    # Combines part words to whole words
    aggregation_strategy="simple",  
)

# List of test data
corpus = [
    # Tema: Hållbarhet & Energi
    "Vi behöver minska våra koldioxidutsläpp för att bromsa klimatförändringarna.",
    "Solceller och vindkraft är viktiga delar i övergången till förnybar energi.",
    "Fastigheten är certifierad enligt miljöbyggnad guld och sparar mycket energi.",
    "Sopsortering och återvinning av plast minskar belastningen på naturen.",
    "Fan! Vilket jävla skit. Sade Jesus år 12 efter kristus när han slog stortån på en list.",
    # Tema: IT, Kod & Databaser
    "Databasen har indexerats om för att snabba upp söktiderna i backend-systemet.",
    "Ett nytt REST API har implementerats med FastAPI och Pydantic.",
    "Utvecklingsteamet åtgärdade flera kritiska buggar inför fredagens produktionssättning.",
    "Versionshantering med Git gör det enklare att samarbeta i stora projekt.",
    "Bästa Leauge champions: Nunu, Kindred och såklart Mästarn",
    "HUT-produkten gör framsteg",
    # Tema: Matlagning & Bakning
    "Surdegsbrödet fick jäsa långsamt i kylskåpet över natten.",
    "Till såsen används schalottenlök, vitt vin och en klick smör.",
    "Rätten kryddas rikligt med färsk koriander, ingefära och chili.",
    "Pastan kokas tills den är al dente och vänds sedan i olivolja.",
    "Ge mig en påse chips.",
    "Snälla Kalle ge mig en påse chips! Jag svälter.",
    # Tema: Vardag, Resor & Vinter
    "Tåget mot Stockholm blev inställt på grund av en signalstörning.",
    "Idag är det fredagen den 16e October 2026",
    "Under vintern fryser sjöarna till is och folk åker långfärdsskridskor.",
    "Katten sover på mattan framför den öppna spisen.",
    "Jag glömde mitt paraply hemma och blev genomblöt på väg till jobbet.",
    "Glen reste till Danmark med sin kompis Sven Svensson den förste av sitt namn",
]

def search(corpus, ner, query):
    # Beräkna embeddings för både fråga och korpus
    all_texts = [query] + corpus
    encoded = semantic_token(
        all_texts, padding=True, truncation=True, return_tensors="pt"
    )

    with torch.no_grad():
        output = semantic_model(**encoded)

    embeddings = mean_pooling(output, encoded["attention_mask"])
    embeddings = F.normalize(embeddings, p=2, dim=1)

    # Dela upp sökfras och dokument
    query_embedding = embeddings[0]  # shape: [768]
    corpus_embeddings = embeddings[1:]  # shape: [len(corpus), 768]

    # NER
    ner_results = ner(corpus)
    
    # Räkna ut cosinuslikhet mot alla texter samtidigt (matrismultiplikation)
    scores = torch.mv(corpus_embeddings, query_embedding).tolist()

    combined = []
    for text, score, entities in zip(corpus, scores, ner_results):
        combined.append({"text": text, "score": score, "entities": entities})

    # Sort by highest score
    combined.sort(key=lambda x: x["score"], reverse=True)

    return combined

def all_data(corpus, ner):
    # Beräkna embeddings för både fråga och korpus
    encoded = semantic_token(
        corpus, padding=True, truncation=True, return_tensors="pt"
    )

    with torch.no_grad():
        output = semantic_model(**encoded)
    embeddings = mean_pooling(output, encoded["attention_mask"])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    # NER
    ner_results = ner(corpus)

    # Combine sentence score and entities to a combined list
    combined = []

    for text, emb, entities in zip(corpus, embeddings, ner_results):
        combined.append({"text": text, "score": emb.tolist(), "entities": entities})

    return combined

def format_score_or_vector(score):
    if isinstance(score, float):
        return f"[{score:.4f}]"
    elif isinstance(score, list):
        preview = ", ".join(f"{x:.4f}" for x in score[:3])
        return f"[Vektor: {preview}, ... (dim: {len(score)})]"
    return ""


def print_all(results):
    for item in results:
        text = item["text"]
        tag = format_score_or_vector(item["score"])
        entities = item["entities"]

        print(f"\n{tag} {text}")

        for ent in entities:
            label = ent.get("entity_group", ent.get("entity"))
            word = ent["word"]
            conf = ent["score"]
            print(f"      NER entiteter: {word:<15} [{label}] ({conf:.1%})")


def print_x(results, print_amount):
    subset = results[:print_amount]

    for item in subset:
        text = item["text"]
        tag = format_score_or_vector(item["score"])
        entities = item["entities"]

        print(f"\n{tag} {text}")

        for ent in entities:
            label = ent.get("entity_group", ent.get("entity"))
            word = ent["word"]
            conf = ent["score"]
            print(f"      NER entiteter: {word:<15} [{label}] ({conf:.1%})")

def menu():
    while True:
        print("Sök")
        menu_choise = input(" 1. Sök igenom alla meningar: \n 2. Se mest matchande meningar: \n 9. Lista all data \n 0. Stäng programmet: \n ")
        if menu_choise == "1":
            query = input("Skriv en mening: \n")
            results = search(corpus, ner, query)

            print(f"\nMening: \"{query}\"")
            print_all(results)

        elif menu_choise == "2":
            query = input("Skriv en mening: \n")
            print_amount = int(input("How many top search results?"))
            results = search(corpus, ner, query)

            print(f"\nMening: \"{query}\"")
            print_x(results, print_amount)

        elif menu_choise == "9":
            results = all_data(corpus, ner)
            print_all(results)

        elif menu_choise == "0":
            break

        else:
            print("Fel val")

if __name__ == "__main__":
    menu()
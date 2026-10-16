from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
model = AutoModelForTokenClassification.from_pretrained(
    "KBLab/bert-base-swedish-cased-ner"
)

ner = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple",  # Slår ihop delord till hela ord
)

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
ner_results = ner(corpus)

for sentence, entities in zip(corpus, ner_results):
    print(f"\nMening: \"{sentence}\"")
    for ent in entities:
        label = ent.get("entity_group", ent.get("entity"))
        word = ent["word"]
        score = ent["score"]
        print(f"{word:<15} [{label}] (säkerhet: {score:.1%})")